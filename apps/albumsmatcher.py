"""albumsmatcher.py - data overhalen van Clementine naar Albums
"""
import pathlib
import sys
import collections
import json
import shutil
# import logging
import contextlib
import itertools
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import apps.albums_dml as dmla
import apps.clementine_dml as dmlc
HERE = pathlib.Path(__file__).parent.parent.absolute()  # os.path.abspath(os.path.dirname(__file__))
FNAME = pathlib.Path(HERE / 'albumsmatcher.json')
F_NEXT = pathlib.Path(HERE / 'icons' / 'go-bottom.png')
F_PREV = pathlib.Path(HERE / 'icons' / 'go-top.png')
F_DOWN = pathlib.Path(HERE / 'icons' / 'go-down.png')
F_UP = pathlib.Path(HERE / 'icons' / 'go-up.png')
from apps.texts import checkpage_messages, workflows
# logging.basicConfig(filename='/tmp/albumsmatcher.log', level=logging.DEBUG,
#                     format='%(asctime)s %(funcName)s %(message)s')
# log = logging.info


class MainFrame(qtw.QMainWindow):
    """Het hoofdscherm van deze applicatie is een container voor de drie specifieke schermen
    """
    def __init__(self, parent=None, app=None):
        if app:
            self.app = parent_app = app
        else:
            self.app = qtw.QApplication(sys.argv)
            parent_app = None
        self.next_icon = gui.QIcon(str(F_NEXT))
        self.prev_icon = gui.QIcon(str(F_PREV))
        self.down_icon = gui.QIcon(str(F_DOWN))
        self.up_icon = gui.QIcon(str(F_UP))
        self.title = "AlbumsMatcher"
        super().__init__()  # moet je niet parent meegeven?
        self.setWindowTitle(self.title)
        self.move(300, 50)
        self.resize(600, 650)
        self.current_data = None
        self.nb = qtw.QTabWidget(self)
        self.nb.currentChanged.connect(self.page_changed)

        frm = qtw.QFrame()
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.nb)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton("E&xit", parent)
        btn.clicked.connect(self.exit)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)
        frm.setLayout(vbox)
        self.setCentralWidget(frm)

        act = qtw.QAction('Exit', self)
        act.triggered.connect(self.exit)
        act.setShortcut('Ctrl+Q')
        self.addAction(act)

        self.current = -1
        self.not_again = False
        self.artist_map, self.albums_map = self.check_for_data()
        self.pages = self.setup_tabwidget()
        self.nb.setCurrentIndex(0)
        self.show()
        ## self.nb.currentWidget().setFocus()
        self.go(parent_app)

    def go(self, app_from_parent):
        "if standalone, start the event loop"
        if not app_from_parent:
            sys.exit(self.app.exec_())

    def check_for_data(self):
        """retrieve saved data if it exists
        """
        artist_map = {}    # map clementine artist name to albums artist id
        albums_map = {}    # map clementine artist name to dict that maps
                           # clementine album names to albums album ids
        appdata = load_appdata()
        if appdata:
            artist_map, albums_map = appdata
        return artist_map, albums_map

    def setup_tabwidget(self):
        "define the pages and attach them to the main window"
        pages = {}  # collections.OrderedDict()
        for ix, item in enumerate([('artists', CompareArtists(self)),
                                   ('albums', CompareAlbums(self)),
                                   ('tracks', CompareTracks(self))]):
            pages[ix] = item
            item[1].first_time = True
            item[1]._parent = self
            self.nb.addTab(item[1], item[0].title())
        return pages

    def page_changed(self):
        """pagina aanpassen nadat een andere gekozen is
        """
        if self.current >= 0:
            if self.not_again:
                self.not_again = False
                return
            ok = self.check_oldpage(self.current)
            if not ok:
                self.not_again = True
                self.nb.setCurrentIndex(self.current)
                return
        self.current = self.nb.currentIndex()
        go = self.nb.currentWidget()
        if go.first_time:
            go.first_time = False
            go.create_widgets()
            go.create_actions()
        msg = go.refresh_screen(self.current_data)
        if msg:
            qtw.QMessageBox.information(self, self.title, msg)
            self.current = 0
            self.nb.setCurrentIndex(self.current)
            go.refresh_screen(self.current_data)

    def check_oldpage(self, pageno):
        "check if page can be left"
        if self.pages[pageno][1].modified:
            # qtw.QMessageBox.information(self, self.title, checkpage_messages[pageno])
            # return False
            ok = qtw.QMessageBox.question(self, self.title,
                                          f'{checkpage_messages[pageno]} - save now?',
                                          qtw.QMessageBox.Yes | qtw.QMessageBox.No |
                                          qtw.QMessageBox.Cancel,
                                          qtw.QMessageBox.No)
            if ok == qtw.QMessageBox.Cancel:
                return False
            if ok == qtw.QMessageBox.Yes:
                self.pages[pageno][1].save_all()
        return True

    def exit(self):
        """shutdown application
        """
        if self.check_oldpage(self.current):
            ## save_appdata([self.artist_map, self.albums_map])
            self.close()


class CompareArtists(qtw.QWidget):
    """artiesten uit Clementine naast artiesten uit Albums zetten
    """
    def create_widgets(self):
        """setup screen
        """
        ## frm = qtw.QSplitter(self)
        self.appname = self._parent.title
        tree = qtw.QTreeWidget(self)
        tree.setColumnCount(2)
        hdr = tree.header()
        hdr.setStretchLastSection(False)
        hdr.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        tree.setColumnWidth(1, 50)
        tree.setHeaderLabels(['Artist', 'Match'])
        tree.setMouseTracking(True)
        tree.itemEntered.connect(popuptext)
        tree.itemDoubleClicked.connect(self.select_and_go)
        self.clementine_artists = tree

        tree = qtw.QTreeWidget(self)
        tree.setColumnCount(3)
        hdr = tree.header()
        hdr.setStretchLastSection(False)
        tree.setColumnWidth(0, 80)
        tree.setColumnWidth(2, 50)
        hdr.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        tree.setHeaderLabels(['First Name', 'Last Name', 'Id'])
        tree.setMouseTracking(True)
        tree.itemEntered.connect(popuptext)
        tree.currentItemChanged.connect(self.check_deletable)
        self.albums_artists = tree

        b_help = qtw.QPushButton('&Help', self)
        b_help.clicked.connect(self.help)
        b_next = qtw.QPushButton(self)
        b_next.setIcon(self._parent.next_icon)
        b_next.setIconSize(core.QSize(12, 12))
        # b_next.setIconSize(12, 12)
        b_next.setToolTip('Go to next unmatched artist')
        b_next.clicked.connect(self.focus_next)
        b_prev = qtw.QPushButton(self)
        b_prev.setIcon(self._parent.prev_icon)
        b_prev.setIconSize(core.QSize(12, 12))
        # b_prev.setIconSize(12, 12)
        b_prev.setToolTip('Go to previous unmatched artist')
        b_prev.clicked.connect(self.focus_prev)
        b_find = qtw.QPushButton('&Check Artist', self)
        b_find.clicked.connect(self.find_artist)
        ## b_copy = qtw.QPushButton('&Copy Selected', self)
        ## b_copy.clicked.connect(self.copy_artist)

        ## b_add = qtw.QPushButton('&New Artist', self)
        ## b_add.clicked.connect(self.add_artist)
        self.delete_button = qtw.QPushButton('&Delete', self)
        self.delete_button.clicked.connect(self.delete_artist)
        self.delete_button.setEnabled(False)
        self.save_button = qtw.QPushButton('&Save All', self)
        self.save_button.clicked.connect(self.save_all)

        hbox0 = qtw.QHBoxLayout()
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.clementine_artists)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(b_help)
        hbox.addWidget(b_next)
        hbox.addWidget(b_prev)
        hbox.addWidget(b_find)
        ## hbox.addWidget(b_copy)
        hbox.addStretch()
        vbox.addLayout(hbox)
        hbox0.addLayout(vbox)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.albums_artists)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        ## hbox.addWidget(b_add)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.save_button)
        hbox.addStretch()
        vbox.addLayout(hbox)
        hbox0.addLayout(vbox)

        self.setLayout(hbox0)

    def create_actions(self):
        """keyboard shortcuts
        """
        for text, callback, keys in (('Help', self.help, ['F1', 'Ctrl+H']),
                                     ('Focus', self.clementine_artists.setFocus, ['Ctrl+L']),
                                     ('Find', self.find_artist, ['Ctrl+Return', 'Ctrl+F']),
                                     ('Go', self.select_and_go, ['Ctrl+Shift+Return']),
                                     ('Next', self.focus_next, ['Ctrl+N']),
                                     ('Prev', self.focus_prev, ['Ctrl+P']),
                                     ('Delete', self.delete_artist, ['Ctrl+D', 'Del']),
                                     ('Save', self.save_all, ['Ctrl+S'])):
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcuts(keys)
            self.addAction(act)

    def refresh_screen(self, artist=None):
        """update screen contents
        """
        self.set_modified(False)
        self.new_artists = []
        self.new_matches = {}
        self.artist_list_a, self.artist_list_c = read_artists()
        self.lookup = {' '.join((x, y)).strip(): z for x, y, z in self.artist_list_a}
        self.finda = {z: (x, y) for x, y, z in self.artist_list_a}
        self.artist_map = self._parent.artist_map or {x: ''
                                                      for x in self.artist_list_c}
        self.max_artist = max([int(x[2]) for x in self.artist_list_a])
        self.clementine_artists.clear()
        for item in self.artist_list_c:
            if item:
                new = qtw.QTreeWidgetItem([item, self.artist_map[item]])
                self.clementine_artists.addTopLevelItem(new)
        self.albums_artists.clear()
        for item in self.artist_list_a:
            new = qtw.QTreeWidgetItem(item)
            self.albums_artists.addTopLevelItem(new)
        self.artist_buffer = ''
        self.focus_artist(artist)

    def set_modified(self, value):
        """set flag and enable/disable button if appropriate
        """
        self.modified = value
        self.save_button.setEnabled(value)

    def focus_artist(self, artist=None):
        """select given artist or first unhandled one in left-hand side list
        """
        self.clementine_artists.setFocus()
        if artist:
            findstr = artist
            column = 0
        else:
            findstr = ''
            column = 1
        test = self.clementine_artists.findItems(findstr, core.Qt.MatchFixedString, column)
        if test:
            item = test[0]
        else:
            # item = self.clementine_albums.topLevelItem(0)  # verkeerde widget??
            item = self.clementine_artists.topLevelItem(0)
        self.clementine_artists.setCurrentItem(item)

    def focus_next(self):
        """select next unhandled artist in left-hand side list
        """
        self.focus_item()

    def focus_prev(self):
        """select previous unhandled artist in left-hand side list
        """
        self.focus_item(forward=False)

    def focus_item(self, forward=True):
        """select unhandled artist in left-hand side list
        """
        self.clementine_artists.setFocus()
        current = self.clementine_artists.currentIndex()
        test = self.clementine_artists.findItems('', core.Qt.MatchFixedString, 1)
        if test:
            if not forward:
                test = reversed(test)
            for item in test:
                index = self.clementine_artists.indexFromItem(item)
                if forward and index.row() > current.row():
                    break
                if not forward and index.row() < current.row():
                    break
                item = None
        else:
            item = None
        if item:
            self.clementine_artists.setCurrentItem(item)
            self.clementine_artists.setCurrentIndex(
                self.clementine_artists.indexFromItem(item))
        else:
            qtw.QMessageBox.information(self, self._parent.title, 'No more unmatched items this way')

    def check_deletable(self):
        """if selected (right-hand side) artist is not yet saved, activate
        delete button
        """
        item = self.albums_artists.currentItem()
        self.delete_button.setEnabled(item in self.new_artists)

    def select_and_go(self):
        """Go to tab 2 and select artist
        """
        item = self.clementine_artists.currentItem()
        if not item:
            return
        search = item.text(0)
        if not self.artist_map[search]:
            qtw.QMessageBox.information(self, self.appname,
                                        "Not possible - artist hasn't been matched yet")
            return
        self._parent.current_data = search
        self._parent.nb.setCurrentIndex(1)

    def find_artist(self):
        """search artist in other list

        if not found, try without the first word
        if found, show dialog to confirm match
        """
        item = self.clementine_artists.currentItem()
        if not item:
            return
        self.artist_buffer = item
        search = item.text(0)
        self._parent.current_data = search
        if self.artist_map[search]:  # [item.text(0)]:
            ok = qtw.QMessageBox.question(self, self.appname,
                                          'Artist already has a match - do you want to reassign?',
                                          qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                          qtw.QMessageBox.No)
            if ok == qtw.QMessageBox.No:
                return
            self.artist_map[search] = ''  # [item.text(0)] = ''
        found = self.determine_search_arg_and_find(search)
        if found:
            find = self.albums_artists.findItems(found, core.Qt.MatchFixedString, 2)
            artists, results = self.filter_matched(find)
            a_item = None
            selected, ok = qtw.QInputDialog.getItem(self, self.appname, 'Select Artist', artists,
                                                    editable=False)
            if ok:
                a_item = results[artists.index(selected)]
                self.update_item(a_item, item)
                return

        self.add_artist()  # geen match -> lege match toevoegen

    def determine_search_arg_and_find(self, search):
        """if not found on entire name, try again for last name only
        names may be slightly different so maybe there is more fuzzy logic to apply
        """
        try:
            found = self.lookup[search]
        except KeyError:
            test = search.split(None, 1)
            if len(test) == 1:
                found = False
            else:
                search = test[1]
                try:
                    found = self.lookup[search]
                except KeyError:
                    found = False
        return found

    def filter_matched(self, find):
        "only keep unmatched artists in search result"
        artists = []
        results = []
        for a_item in find:
            if a_item.text(2) in self.artist_map.values():
                continue
            results.append(a_item)
            artists.append(build_artist_name(a_item.text(0), a_item.text(1)))
        return artists, results

    def update_item(self, new_item, from_item):
        """remember changes and make them visible
        """
        self.albums_artists.setCurrentItem(new_item)
        self.albums_artists.scrollToItem(new_item)
        self.artist_map[from_item.text(0)] = new_item.text(2)
        self.new_matches[new_item.text(2)] = from_item.text(0)
        from_item.setText(1, 'X')
        self.set_modified(True)
        nxt = self.clementine_artists.itemBelow(self.clementine_artists.currentItem())
        if nxt:
            self.clementine_artists.setCurrentItem(nxt)

    def copy_artist(self):
        """copy the selected artists's name
        """
        self.artist_buffer = self.clementine_artists.currentItem()

    def add_artist(self):
        """if present, enter the copied artist's name into the last name field
        """
        item = self.artist_buffer
        artistname = item.text(0) if item else ''
        dlg = NewArtistDialog(self, artistname).exec_()
        if dlg != qtw.QDialog.Accepted:
            return
        fname, lname = self.data
        if not item:
            result = self.clementine_artists.findItems(' '.join((fname, lname)),
                                                       core.Qt.MatchFixedString, 0)
            if result:
                item = result[0]
        if not item:
            qtw.QMessageBox.information(self, self.appname,
                                        "Artist doesn't exist on the Clementine side")
            return

        a_item = None
        results = self.albums_artists.findItems(lname, core.Qt.MatchFixedString, 1)
        data = [build_artist_name(x.text(0), x.text(1)) for x in results]
        if results:
            selected, ok = qtw.QInputDialog.getItem(self, self.appname, 'Select Artist', data,
                                                    editable=False)
            if ok:
                a_item = results[data.index(selected)]
        if not a_item:
            self.max_artist += 1
            a_item = qtw.QTreeWidgetItem([fname, lname, str(self.max_artist)])
            self.albums_artists.addTopLevelItem(a_item)
            self.new_artists.append(a_item)
        self.update_item(a_item, item)

    def delete_artist(self):
        """remove artist data from view
        """
        item = self.albums_artists.currentItem()
        if item is None:
            return
        name = build_artist_name(item.text(0), item.text(1))
        ok = qtw.QMessageBox.question(self, self.appname, f'Ok to delete artist `{name}`?',
                                      qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel,
                                      qtw.QMessageBox.Ok)
        if ok != qtw.QMessageBox.Ok:
            return
        ix = self.albums_artists.currentIndex().row()
        self.albums_artists.takeTopLevelItem(ix)
        self.new_artists.remove(item)
        a_itemkey = item.text(2)
        try:
            name = self.new_matches.pop(a_itemkey)
        except KeyError:
            name = ''
        if name and self.artist_map[name] == a_itemkey:
            self.artist_map[name] = ''
            results = self.clementine_artists.findItems(name, core.Qt.MatchFixedString, 0)
            results[0].setText(1, '')
        self.set_modified(bool(self.new_matches))

    def save_all(self):
        """save changes (additions) to Albums database
        """
        data = []
        for i in range(self.albums_artists.topLevelItemCount()):
            item = self.albums_artists.topLevelItem(i)
            data.append((int(item.text(2)), item.text(0), item.text(1)))
        new_keys = update_artists(data)
        for key, value in new_keys.items():
            self.artist_map[key] = str(value)
        self._parent.artist_map = self.artist_map
        self._parent.artist_map.update({x: '' for x, y in self.artist_map.items() if not y})
        save_appdata([self._parent.artist_map, self._parent.albums_map])
        self.refresh_screen(self.clementine_artists.currentItem().text(0))

    def help(self):
        """explain intended workflow
        """
        qtw.QMessageBox.information(self, self._parent.title, workflows['cmpart'])


class NewArtistDialog(qtw.QDialog):
    """show dialog for adding a new artist
    """
    def __init__(self, parent, name=''):
        super().__init__(parent)
        self.setWindowTitle(parent.appname + ' - add artist')
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('First name:', self), 0, 0)
        self.first_name = qtw.QLineEdit(self)
        self.first_name.setMinimumWidth(200)
        self.first_name.setMaximumWidth(200)
        gbox.addWidget(self.first_name, 0, 1)
        gbox.addWidget(qtw.QLabel('Last name:', self), 1, 0)
        self.last_name = qtw.QLineEdit(name, self)
        self.last_name.setMinimumWidth(200)
        self.last_name.setMaximumWidth(200)
        gbox.addWidget(self.last_name, 1, 1)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.reject)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Update', self)
        btn.clicked.connect(self.update)
        btn.setDefault(True)
        hbox.addWidget(btn)
        hbox.addStretch()
        gbox.addLayout(hbox, 2, 0, 1, 2)
        self.setLayout(gbox)
        self.last_name.setFocus()

    def update(self):
        """when finished: propagate changes to parent
        """
        fname = self.first_name.text()
        lname = self.last_name.text()
        if not fname and not lname:
            qtw.QMessageBox.information(self, 'AlbumsMatcher',
                                        "Enter at least one name or press `Cancel`")
            return
        self.parent().data = (fname, lname)
        self.accept()


class CompareAlbums(qtw.QWidget):
    """albums uit Clementine naast albums uit Albums zetten
    """
    def create_widgets(self):
        """setup screen
        """
        self.appname = self._parent.title
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Selecteer een uitvoerende:', self))
        self.artist_list = qtw.QComboBox(self)
        self.artist_list.currentIndexChanged.connect(self.get_albums)
        ## self.last_handled = None
        self.albums_to_save = collections.defaultdict(list)
        self.albums_to_update = collections.defaultdict(list)
        hbox.addWidget(self.artist_list)
        btn = qtw.QPushButton(self)
        btn.setIcon(self._parent.down_icon)
        btn.setIconSize(core.QSize(20, 20))
        btn.setToolTip('Select next artist in list')
        btn.clicked.connect(self.next_artist)
        hbox.addWidget(btn)
        self.next_artist_button = btn
        btn = qtw.QPushButton(self)
        btn.setIcon(self._parent.up_icon)
        btn.setIconSize(core.QSize(20, 20))
        btn.setToolTip('Select previous artist in list')
        btn.clicked.connect(self.prev_artist)
        hbox.addWidget(btn)
        self.prev_artist_button = btn
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        vbox2 = qtw.QVBoxLayout()
        tree = qtw.QTreeWidget(self)
        tree.setColumnCount(2)
        hdr = tree.header()
        hdr.setStretchLastSection(False)
        tree.setColumnWidth(1, 60)
        hdr.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        tree.setHeaderLabels(['Album Name in Clementine', 'Match'])
        tree.setMouseTracking(True)
        tree.itemEntered.connect(popuptext)
        self.clementine_albums = tree
        vbox2.addWidget(self.clementine_albums)
        hbox2 = qtw.QHBoxLayout()
        hbox2.addStretch()
        b_help = qtw.QPushButton('&Help', self)
        b_help.clicked.connect(self.help)
        b_find = qtw.QPushButton('&Check Album', self)
        b_find.clicked.connect(self.find_album)
        hbox2.addWidget(b_help)
        hbox2.addWidget(b_find)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        hbox.addLayout(vbox2)
        vbox2 = qtw.QVBoxLayout()
        tree = qtw.QTreeWidget(self)
        tree.setColumnCount(3)
        hdr = tree.header()
        hdr.setStretchLastSection(False)
        tree.setColumnWidth(1, 60)
        tree.setColumnWidth(2, 60)
        hdr.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        tree.setHeaderLabels(['Album Name in Albums', 'Year', 'Id'])
        tree.setMouseTracking(True)
        tree.itemEntered.connect(popuptext)
        self.albums_albums = tree
        vbox2.addWidget(self.albums_albums)
        hbox2 = qtw.QHBoxLayout()
        hbox2.addStretch()
        self.save_button = qtw.QPushButton('&Save All', self)
        self.save_button.clicked.connect(self.save_all)
        hbox2.addWidget(self.save_button)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def create_actions(self):
        """keyboard shortcuts
        """
        for text, callback, keys in (('Help', self.help, ['F1', 'Ctrl+H']),
                                     ('Select', self.artist_list.setFocus, ['Ctrl+Home']),
                                     ('Focus', self.focus_albums, ['Ctrl+L']),
                                     ('Next', self.next_artist, ['Ctrl+N']),
                                     ('Prev', self.prev_artist, ['Ctrl+P']),
                                     ('Find', self.find_album, ['Ctrl+Return', 'Ctrl+F']),
                                     ('Save', self.save_all, ['Ctrl+S'])):
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcuts(keys)
            self.addAction(act)

    def refresh_screen(self, artist=None):
        """update screen contents
        """
        self.set_modified(False)
        self.artist_map = self._parent.artist_map
        self.albums_map = collections.defaultdict(dict)
        self.albums_map.update(self._parent.albums_map)
        # is dit een terechte aanname: x['artist'] is altijd een key in de artist_map van de parent
        if self._parent.artist_map:
            self.c_artists = [x['artist'] for x in dmlc.list_artists()
                              if self._parent.artist_map[x['artist']]]
        else:
            return "Please match some artists first"
        self.artist_list.clear()
        self.artist_list.addItems(self.c_artists)
        for ix in range(self.clementine_albums.topLevelItemCount()):
            item = self.clementine_albums.topLevelItem(ix)
            if item.text(1) == 'X':
                # gaat dit nooit mis?
                a_item = self.albums_map[self.c_artist][item.text(0)][1]
                item.setText(1, str(a_item))
        if artist:
            try:
                self.artist_list.setCurrentIndex(artist)
            except TypeError:
                try:
                    indx = self.c_artists.index(artist)
                except ValueError:
                    return "This artist has not been matched yet"
                self.artist_list.setCurrentIndex(indx)
        self.update_navigation_buttons()
        return ''

    def set_modified(self, value):
        """set flag and enable/disable button where appropriate
        """
        self.modified = value
        self.save_button.setEnabled(value)

    def update_navigation_buttons(self):
        """enable/disable buttons where appropriate
        """
        test = self.artist_list.currentIndex()  # .row()
        self.prev_artist_button.setEnabled(True)
        self.next_artist_button.setEnabled(True)
        if test == 0:
            self.prev_artist_button.setEnabled(False)
        if test == len(self.c_artists) - 1:
            self.next_artist_button.setEnabled(False)
        self.focus_albums()

    def get_albums(self):
        """get lists of albums for the selected artist
        and show them in the treewidgets
        """
        if self.artist_list.count() == 0:   # this happens when the panel is reshown
            return                          # after another panel was shown
        self.c_artist = self.artist_list.currentText()
        ## self.last_handled = self.artist_list.currentIndex()
        # remember first handled item for currency communication over panels
        self._parent.current_data = self.c_artist
        self.a_artist = self.artist_map[self.c_artist]
        a_albums, c_albums = read_artist_albums(self.a_artist, self.c_artist)
        for name, year, id, *rest in self.albums_to_save[self.c_artist]:
            a_albums.append((name, year, str(id)))
        self.clementine_albums.clear()
        for item, year in c_albums:
            new = qtw.QTreeWidgetItem([item])
            new.setData(0, core.Qt.UserRole, year)
            try:
                new.setText(1, str(self.albums_map[self.c_artist][item][1]))
            except KeyError:
                pass
            self.clementine_albums.addTopLevelItem(new)
        self.albums_albums.clear()
        self.lookup = collections.defaultdict(list)
        for item in a_albums:
            new = qtw.QTreeWidgetItem([x.replace('None', '') for x in item])  # kan dit als a_albums
            self.albums_albums.addTopLevelItem(new)                           # 3-tuples bevat?
            self.lookup[item[0]].append(item[2])
        self.tracks = collections.defaultdict(list)

    def focus_albums(self):
        """select first unhandled album in left-hand side list
        """
        self.clementine_albums.setFocus()
        for ix in range(self.clementine_albums.topLevelItemCount()):
            item = self.clementine_albums.topLevelItem(ix)
            if not item.text(1):
                break
        else:
            item = self.clementine_albums.topLevelItem(0)
        self.clementine_albums.setCurrentItem(item)

    def next_artist(self):
        """select next artist in dropdown
        """
        test = self.artist_list.currentIndex() + 1
        if test < self.artist_list.count():
            self.artist_list.setCurrentIndex(test)
            self.update_navigation_buttons()

    def prev_artist(self):
        """select previous artist in dropdown
        """
        test = self.artist_list.currentIndex() - 1
        if test >= 0:
            self.artist_list.setCurrentIndex(test)
            self.update_navigation_buttons()

    def find_album(self):
        """search album in other list

        if found, show dialog to confirm match
        if you have to confirm anyway, why not select right away?
        """
        item = self.clementine_albums.currentItem()
        if not item:
            self.focus_albums()
            item = self.clementine_albums.currentItem()
        if item.text(0) in self.albums_map[self.c_artist]:
            ok = qtw.QMessageBox.question(self, self.appname,
                                          'Album already has a match - do you want to reassign?',
                                          qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                          qtw.QMessageBox.Yes)
            if ok == qtw.QMessageBox.No:
                return
            self.albums_map[self.c_artist].pop(item.text(0))
        # select albums for self.a_artist and remove the ones that are already matched
        album_list = []
        for album in dmla.list_albums_by_artist('', self.a_artist, 'Titel'):
            test = self.check_if_new_album(album)
            if test:
                album_list.append(test)
        if album_list:
            albums = [x[0] for x in album_list]
            selected, ok = qtw.QInputDialog.getItem(self, self.appname, 'Select Album',
                                                    albums, editable=False)
            if ok:
                self.prepare_album_for_update(item, album_list[albums.index(selected)])
                return
        self.add_album()

    def check_if_new_album(self, album):
        "if album data not already present, return them. Otherwise return None"
        for a_item in self.albums_map[self.c_artist].values():
            if a_item[1] == album.id:
                return None
        return build_album_name(album), album.id

    def prepare_album_for_update(self, c_item, selected_album):
        "actions for an album selected from the list"
        a_item = self.albums_albums.findItems(str(selected_album[1]), core.Qt.MatchFixedString, 2)[0]
        c_year = str(c_item.data(0, core.Qt.UserRole))
        if c_year:
            a_year = a_item.text(1)
            if c_year != a_year:
                ask = f"Clementine year ({c_year}) differs from Albums year ({a_year})"
                ok = qtw.QMessageBox.question(self, self.appname, f"{ask}, replace?",
                                              qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                              qtw.QMessageBox.Yes)
                if ok == qtw.QMessageBox.Yes:
                    a_item.setText(1, c_year)
        self.albums_to_update[self.c_artist].append((a_item.text(0), a_item.text(1),
                                                     int(a_item.text(2)), False, []))
        self.update_item(a_item, c_item)

    def add_album(self):
        """actions for an album not yet present in the list

        if present, enter the copied album's name into name field
        better yet, show all albums for the matched artist and choose one
        which means, we have to remember the selected artist, not the name
        """
        item = self.clementine_albums.currentItem()
        albumname = item.text(0) if item else ''
        year = item.data(0, core.Qt.UserRole) if item else ''
        dlg = NewAlbumDialog(self, albumname, year).exec_()
        if dlg != qtw.QDialog.Accepted:
            return
        name, year, is_live = self.data
        if not item:
            result = self.clementine_albums.findItems(name, core.Qt.MatchFixedString, 0)
            if result:
                item = result[0]
        if not item:
            qtw.QMessageBox.information(self, self.appname,
                                        "Album doesn't exist on the Clementine side")
            return
        a_item = None
        results = self.albums_albums.findItems(name, core.Qt.MatchFixedString, 0)
        if results:
            data = [build_album_name(x) for x in results]
            selected, ok = qtw.QInputDialog.getItem(self, self.appname, 'Select Album', data,
                                                    editable=False)
            if ok:
                a_item = results[data.index(selected)]
        if not a_item:
            self.prepare_album_for_saving(item, name, year, is_live)
        self.update_item(a_item, item)

    def prepare_album_for_saving(self, c_item, name, year, is_live):
        "actions for an album that wasn't in the list yet"
        a_item = qtw.QTreeWidgetItem([name, year, '0'])
        self.albums_albums.addTopLevelItem(a_item)
        tracklist = dmlc.list_tracks_for_album(self.c_artist, c_item.text(0))
        num = itertools.count(1)
        tracks = [(next(num), x['title']) for x in tracklist if x['track'] > -1]
        self.albums_to_save[self.c_artist].append((name, year, 'X', is_live, tracks))

    def update_item(self, new_item, from_item):
        """remember changes and make them visible
        """
        self.albums_albums.setCurrentItem(new_item)
        self.albums_albums.scrollToItem(new_item)
        self.albums_map[self.c_artist][from_item.text(0)] = (build_album_name(new_item),
                                                             int(new_item.text(2)))
        ## log('self.albums_map: %s', self.albums_map)
        from_item.setText(1, 'X')
        self.set_modified(True)
        nxt = self.clementine_albums.itemBelow(
            self.clementine_albums.currentItem())
        if nxt:
            self.clementine_albums.setCurrentItem(nxt)

    def save_all(self):
        """save changes (additions) to Albums database
        """
        data = []
        for key, albums in self.albums_to_update.items():
            self.albums_to_save[key] += albums
        with wait_cursor(self._parent):
            for artist, albumdata in self.albums_to_save.items():
                if not albumdata:
                    continue
                artistid = self.artist_map[artist]
                data = []
                for name, year, key, is_live, tracks in albumdata:
                    if key == 'X':
                        key = 0
                    data.append((key, name, year, is_live, tracks))
                albums = dmla.update_albums_by_artist(artistid, data)
                albums_map_lookup = {build_album_name(x): x.id for x in albums}
                for c_name, value in self.albums_map[artist].items():
                    a_name, id = value
                    try:
                        test = albums_map_lookup[a_name]
                    except KeyError:
                        continue
                    if id != test:
                        self.albums_map[artist][c_name] = (a_name, test)
        self.albums_to_save.clear()
        self.albums_to_update.clear()
        self._parent.albums_map = self.albums_map
        self._parent.albums_map.update({x: {} for x, y in self.albums_map.items()
                                        if not y})
        ## self.last_handled = None
        save_appdata([self._parent.artist_map, self._parent.albums_map])
        self.refresh_screen(self.artist_list.currentIndex())

    def help(self):
        """explain intended workflow
        """
        qtw.QMessageBox.information(self, self._parent.title, workflows['cmpalb'])


class NewAlbumDialog(qtw.QDialog):
    """show dialog for adding a new album
    """
    def __init__(self, parent, name='', year=''):
        super().__init__(parent)
        self.setWindowTitle(parent.appname + ' - add album')
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('Album title:', self), 0, 0)
        self.first_name = qtw.QLineEdit(name, self)
        self.first_name.setMinimumWidth(200)
        self.first_name.setMaximumWidth(200)
        gbox.addWidget(self.first_name, 0, 1)
        gbox.addWidget(qtw.QLabel('Release year:', self), 1, 0)
        self.last_name = qtw.QLineEdit(str(year), self)
        self.last_name.setMinimumWidth(100)
        self.last_name.setMaximumWidth(100)
        gbox.addWidget(self.last_name, 1, 1)
        hbox = qtw.QHBoxLayout()
        self.is_concert = qtw.QCheckBox('Concertregistratie', self)
        hbox.addStretch()
        hbox.addWidget(self.is_concert)
        hbox.addStretch()
        gbox.addLayout(hbox, 2, 0, 1, 2)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.reject)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Update', self)
        btn.clicked.connect(self.update)
        btn.setDefault(True)
        hbox.addWidget(btn)
        hbox.addStretch()
        gbox.addLayout(hbox, 3, 0, 1, 2)
        self.setLayout(gbox)
        self.last_name.setFocus()

    def update(self):
        """when finished: propagate changes to parent
        """
        name = self.first_name.text()
        year = self.last_name.text()
        is_live = self.is_concert.isChecked()
        if not name:
            qtw.QMessageBox.information(self, 'AlbumsMatcher',
                                        "Enter at least the name or press `Cancel`")
            return
        self.parent().data = (name, year, is_live)
        self.accept()


class CompareTracks(qtw.QWidget):
    """tracks uit Clementine naast tracks uit Albums zetten
    """
    def create_widgets(self):
        """setup screen
        """
        self.appname = self._parent.title
        self.artist_index = self.album_index = 0

        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('Selecteer een uitvoerende:', self), 0, 0)
        self.artists_list = qtw.QComboBox(self)
        self.artists_list.currentIndexChanged.connect(self.get_albums)
        hbox.addWidget(self.artists_list)
        btn = qtw.QPushButton(self)
        btn.setIcon(self._parent.down_icon)
        btn.setIconSize(core.QSize(20, 20))
        btn.setToolTip('Select next artist in list')
        btn.clicked.connect(self.next_artist)
        self.next_artist_button = btn
        hbox.addWidget(btn)
        btn = qtw.QPushButton(self)
        btn.setIcon(self._parent.up_icon)
        btn.setIconSize(core.QSize(20, 20))
        btn.setToolTip('Select previous artist in list')
        btn.clicked.connect(self.prev_artist)
        self.prev_artist_button = btn
        hbox.addWidget(btn)
        hbox.addStretch()
        gbox.addLayout(hbox, 0, 1)

        hbox = qtw.QHBoxLayout()
        gbox.addWidget(qtw.QLabel('Selecteer een album:', self), 1, 0)
        self.albums_list = qtw.QComboBox(self)
        self.albums_list.setMinimumWidth(300)
        self.albums_list.currentIndexChanged.connect(self.get_tracks)
        hbox.addWidget(self.albums_list)
        btn = qtw.QPushButton(self)
        btn.setIcon(self._parent.down_icon)
        btn.setIconSize(core.QSize(20, 20))
        btn.setToolTip('Select next album in list')
        btn.clicked.connect(self.next_album)
        self.next_album_button = btn
        hbox.addWidget(btn)
        btn = qtw.QPushButton(self)
        btn.setIcon(self._parent.up_icon)
        btn.setIconSize(core.QSize(20, 20))
        btn.setToolTip('Select previous album in list')
        btn.clicked.connect(self.prev_album)
        self.prev_album_button = btn
        hbox.addWidget(btn)
        hbox.addStretch()
        gbox.addLayout(hbox, 1, 1)
        vbox.addLayout(gbox)

        hbox = qtw.QHBoxLayout()
        vbox2 = qtw.QVBoxLayout()
        tree = qtw.QTreeWidget(self)
        tree.setColumnCount(1)
        tree.setHeaderLabels(['Track Name in Clementine'])
        tree.setMouseTracking(True)
        tree.itemEntered.connect(popuptext)
        self.clementine_tracks = tree
        vbox2.addWidget(self.clementine_tracks)
        hbox2 = qtw.QHBoxLayout()
        hbox2.addStretch()
        b_help = qtw.QPushButton('&Help', self)
        b_help.clicked.connect(self.help)
        hbox2.addWidget(b_help)
        self.b_copy = qtw.QPushButton('&Copy Tracks', self)
        self.b_copy.clicked.connect(self.copy_tracks)
        hbox2.addWidget(self.b_copy)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        hbox.addLayout(vbox2)
        vbox2 = qtw.QVBoxLayout()

        tree = qtw.QTreeWidget(self)
        tree.setColumnCount(1)
        tree.setHeaderLabels(['Track Name in Albums'])
        tree.setMouseTracking(True)
        tree.itemEntered.connect(popuptext)
        self.albums_tracks = tree
        vbox2.addWidget(self.albums_tracks)
        hbox2 = qtw.QHBoxLayout()
        hbox2.addStretch()
        b_unlink = qtw.QPushButton('&Unlink Album', self)
        b_unlink.clicked.connect(self.unlink)
        hbox2.addWidget(b_unlink)
        self.b_save = qtw.QPushButton('&Save Unlinked', self)
        self.b_save.clicked.connect(self.save_all)
        hbox2.addWidget(self.b_save)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def create_actions(self):
        """keyboard shortcuts
        """
        for text, callback, keys in (('Help', self.help, ['F1', 'Ctrl+H']),
                                     ('Select_Artist', self.artists_list.setFocus, ['Ctrl+Home']),
                                     ('Select_Album', self.albums_list.setFocus, ['Ctrl+A']),
                                     ('Next_Artist', self.next_artist, ['Ctrl+N']),
                                     ('Prev_Artist', self.prev_artist, ['Ctrl+P']),
                                     ('Next_Album', self.next_album, ['Ctrl+Shift+N']),
                                     ('Prev_Album', self.prev_album, ['Ctrl+Shift+P']),
                                     ('Copy', self.copy_tracks, ['Ctrl+C']),
                                     ('Unlink', self.unlink, ['Ctrl+U']),
                                     ('Save', self.save_all, ['Ctrl+S'])):
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcuts(keys)
            self.addAction(act)

    def refresh_screen(self, artist=None, album=None, modifyoff=True):
        """update screen contents
        """
        if modifyoff:
            self.modified = False
        self.b_save.setEnabled(self.modified)
        self.artist_map = self._parent.artist_map
        self.albums_map = collections.defaultdict(dict)
        self.albums_map.update(self._parent.albums_map)
        if self._parent.artist_map:
            self.c_artists = [x['artist'] for x in dmlc.list_artists()
                              if self._parent.artist_map[x['artist']]]
        else:
            return "Please match some artists and albums first"
        self.artists_list.clear()
        self.artists_list.addItems(self.c_artists)
        if artist:
            try:
                self.artists_list.setCurrentIndex(artist)
            except TypeError:
                try:
                    indx = self.c_artists.index(artist)
                except ValueError:
                    # qtw.QMessageBox.information(self, self._parent.title, "This "
                    #                            "artist has not been matched yet")
                    return "This artist has not been matched yet"
                self.artists_list.setCurrentIndex(indx)
        if album:
            self.albums_list.setCurrentIndex(album)
        return ''

    def get_albums(self):
        """get list of matched albums for the selected artist
        and show it in the other combobox
        """
        self.artist = self.artists_list.currentText()
        self.c_albums = [x['album'] for x in dmlc.list_albums(self.artist)
                         if [x['album'] in self.albums_map[self.artist]]]
        self.albums_list.clear()
        self.albums_list.addItems(self.c_albums)
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """enable/disable buttons where appropriate
        """
        test = self.artists_list.currentIndex()  # .row()
        self.prev_artist_button.setEnabled(True)
        self.next_artist_button.setEnabled(True)
        if test == 0:
            self.prev_artist_button.setEnabled(False)
        if test == len(self.c_artists) - 1:
            self.next_artist_button.setEnabled(False)
        test = self.albums_list.currentIndex()  # .row()
        self.prev_album_button.setEnabled(True)
        self.next_album_button.setEnabled(True)
        if test == 0:
            self.prev_album_button.setEnabled(False)
        if test == len(self.c_albums) - 1:
            self.next_album_button.setEnabled(False)

    def get_tracks(self):
        """get lists of tracks for the matched albums
        and show them in the treewidgets
        """  # shouldn't this return like other methods, i.e. with messages instead of giving them?
        self.c_album = self.albums_list.currentText()
        self.clementine_tracks.clear()
        self.albums_tracks.clear()
        if self.artists_list.count() == 0:  # this happens when the panel is reshown
            return                          # after another panel was shown
        if self.albums_list.count() == 0:   # this happens during screen buildup
            return                          # when only the first combobox is filled
        if not self.albums_map[self.artist]:
            qtw.QMessageBox.information(self, self._parent.title,
                                        "No (matched) albums for this artist")
            return
        try:
            self.a_album = self.albums_map[self.artist][self.c_album][1]
        except KeyError:
            qtw.QMessageBox.information(self, self._parent.title,
                                        "This album has not been matched yet")
            return
        a_tracks, c_tracks = read_album_tracks(self.a_album, self.artist, self.c_album)
        for item in c_tracks:
            new = qtw.QTreeWidgetItem([item])
            self.clementine_tracks.addTopLevelItem(new)
        for item in a_tracks:
            new = qtw.QTreeWidgetItem([item])
            self.albums_tracks.addTopLevelItem(new)
        reimport_possible = False
        if len(c_tracks) != len(a_tracks):
            reimport_possible = True
        else:
            for ix, item in enumerate(a_tracks):
                try:
                    # conditie deel 1:  a begint met volledige c
                    # conditie deel 2:  eerste letter van c is volledige a - waarom dan startswith?
                    # eigenlijk is de vraag: wat betekent dit precies ('not' is heel verwarrend)
                    if not (item.startswith(c_tracks[ix][0]) or c_tracks[ix][0].startswith(item)):
                        reimport_possible = True
                except IndexError:
                    # kan dit (nog) wel als ik eerst op lengte vergelijk? lukt niet in unittest
                    reimport_possible = True
        self.b_copy.setEnabled(reimport_possible)

    def next_artist(self):
        """select next artist in dropdown
        """
        test = self.artists_list.currentIndex() + 1
        if test < self.artists_list.count():
            self.artists_list.setCurrentIndex(test)
            self.update_navigation_buttons()

    def prev_artist(self):
        """select previous artist in dropdown
        """
        test = self.artists_list.currentIndex() - 1
        if test >= 0:
            self.artists_list.setCurrentIndex(test)
            self.update_navigation_buttons()

    def next_album(self):
        """select next album in dropdown
        """
        test = self.albums_list.currentIndex() + 1
        if test < self.albums_list.count():
            self.albums_list.setCurrentIndex(test)
            self.update_navigation_buttons()

    def prev_album(self):
        """select previous album in dropdown
        """
        test = self.albums_list.currentIndex() - 1
        if test >= 0:
            self.albums_list.setCurrentIndex(test)
            self.update_navigation_buttons()

    def copy_tracks(self):
        """copy tracks of already related albums to the Albums database
        """
        tracks = []
        for ix in range(self.clementine_tracks.topLevelItemCount()):
            item = self.clementine_tracks.topLevelItem(ix)
            tracks.append((ix + 1, item.text(0)))
        if tracks:
            with wait_cursor(self._parent):
                dmla.update_album_tracknames(self.a_album, tracks)
            self.refresh_screen(self.artists_list.currentIndex(), self.albums_list.currentIndex())

    def unlink(self):
        """remove "Clementine recording" from album
        """
        album_id = self.albums_map[self.artist][self.c_album][1]
        # clear entry in self.albums_map[artist]
        self.albums_map[self.artist].pop(self.c_album)
        # remove Albums recording only if no more references to the album exist
        still_present = False
        for item in self.albums_map[self.artist].values():
            if item[1] == album_id:
                still_present = True
        if not still_present:
            dmla.unlink_album(self.a_album)
        self.modified = True
        self.refresh_screen(self.artists_list.currentIndex(), self.albums_list.currentIndex(),
                            modifyoff=False)

    def save_all(self):
        """save changes (additions) to Albums database
        """
        self._parent.albums_map = self.albums_map
        self._parent.albums_map.update({x: {} for x, y in self.albums_map.items() if not y})
        save_appdata([self._parent.artist_map, self._parent.albums_map])
        self.refresh_screen(self.artists_list.currentIndex(), self.albums_list.currentIndex())

    def help(self):
        """explain intended workflow
        """
        qtw.QMessageBox.information(self, self._parent.title, workflows['cmptrk'])


def build_artist_name(first, last):
    """Build full artist name
    """
    name = ', '.join((last, first)) if first else last
    ## return ', '.join((first, last)).strip(',').strip()
    return name


def build_album_name(album):
    """combine album name and release year
    first try as if it's an Album album, otherwise treat as tree item
    """
    try:
        name, year = album.name, album.release_year
    except AttributeError:
        name, year = album.text(0), album.text(1)
    if year:
        name += f' ({year})'
    return name


def save_appdata(appdata):
    """save application data to json file
    """
    try:
        shutil.copyfile(str(FNAME), str(FNAME) + '.bak')
    except FileNotFoundError:
        pass
    with FNAME.open('w') as _out:
        json.dump(appdata, _out)


def load_appdata():
    """load application data from json file
    """
    try:
        with FNAME.open() as _in:
            appdata = json.load(_in)
    except FileNotFoundError:
        return None
    return appdata


def read_artists():
    """get the list of artists from the database
    """
    list_a = [(x.first_name, x.last_name, str(x.id)) for x in dmla.list_artists()]
    list_c = [x['artist'] for x in dmlc.list_artists()]
    return list_a, list_c


def update_artists(artists_list):
    """add new artists to the database
    returns changed keys of already existing artists?
    """
    highest_key = max([x.id for x in dmla.list_artists()])
    new_artists = [(0, x[1], x[2]) for x in artists_list if int(x[0]) > highest_key]
    results = dmla.update_artists(new_artists)
    keys = {(x.first_name, x.last_name): x.id for x in results}
    new_keys = {}
    for item in new_artists:                             # waarvoor is dit ook weer? zie docstring?
        a_name = (item[1], item[2])
        c_name = ' '.join((item[1], item[2])).strip()    # waarom strip() niet ook bij a_name?
        if a_name in keys:
            new_keys[c_name] = keys[a_name]
    return new_keys


def read_artist_albums(id, name):
    """get lists of albums for artist
    """
    list_a = [(x.name, str(x.release_year), str(x.id))
              for x in dmla.list_albums_by_artist('', id, 'Jaar')]
    list_c = [(x['album'], x['year']) for x in dmlc.list_albums(name)]
    return list_a, list_c


def read_album_tracks(id, artist_name, album_name):
    """get lists of tracks for albums
    """
    list_a = [x.name for x in dmla.list_tracks(id)]
    list_c = [x['title'] for x in dmlc.list_tracks_for_album(artist_name, album_name)
              if x['track'] != -1]
    return list_a, list_c


def popuptext(item, colno):
    """show complete text of description if moused over
    """
    if item.text(2):
        if colno == 1:
            item.setToolTip(colno, item.text(colno))
    elif colno == 0:
        item.setToolTip(colno, item.text(colno))


@contextlib.contextmanager
def wait_cursor(win):
    """change cursor before and after executing some function
    """
    win.app.setOverrideCursor(gui.QCursor(core.Qt.WaitCursor))
    yield
    win.app.restoreOverrideCursor()
