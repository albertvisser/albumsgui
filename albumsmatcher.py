"""albumsmatcher.py - data overhalen van Clementine naar Albums
"""
import sys
import collections
import json
import shutil
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import albums_dml as dmla
import clementine_dml as dmlc
from banshee_settings import databases
DB_A = databases['albums']
DB_C = databases['clementine']
FNAME = 'albumsmatcher.json'


def save_appdata(appdata):
    """save application data to json file
    """
    try:
        shutil.copyfile(FNAME, FNAME + '.bak')
    except FileNotFoundError:
        pass
    with open(FNAME, 'w') as _out:
        json.dump(appdata, _out)


def load_appdata():
    """load application data from json file
    """
    try:
        _in = open(FNAME)
    except FileNotFoundError:
        return
    with _in:
        appdata = json.load(_in)
    return appdata


def read_artists():
    """get the list of artists from the database
    """
    list_a = [(x.first_name, x.last_name, str(x.id)) for x in dmla.list_artists()]
    list_c = [x['artist'] for x in dmlc.list_artists(DB_C)]
    return list_a, list_c


def update_artists(artists_list):
    """add new artists to the database
    """
    highest_key = max([x.id for x in dmla.list_artists()])
    new_artists = [(0, x[1], x[2]) for x in artists_list if int(x[0]) > highest_key]
    ## print(new_artists)
    dmla.update_artists(new_artists)


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
        self.clementine_artists = tree

        tree = qtw.QTreeWidget(self)
        tree.setColumnCount(3)
        hdr = tree.header()
        hdr.setStretchLastSection(False)
        tree.setColumnWidth(0, 80)
        tree.setColumnWidth(2, 50)
        hdr.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        tree.setHeaderLabels(['First Name', 'Last Name', 'Id'])
        self.albums_artists = tree

        b_help = qtw.QPushButton('&Help', self)
        b_help.clicked.connect(self.help)
        b_find = qtw.QPushButton('&Check Artist', self)
        b_find.clicked.connect(self.find_artist)
        ## b_copy = qtw.QPushButton('&Copy Selected', self)
        ## b_copy.clicked.connect(self.copy_artist)

        b_add = qtw.QPushButton('&New Artist', self)
        b_add.clicked.connect(self.add_artist)
        b_save = qtw.QPushButton('&Save All', self)
        b_save.clicked.connect(self.save_all)

        hbox0 = qtw.QHBoxLayout()
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.clementine_artists)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(b_help)
        hbox.addWidget(b_find)
        ## hbox.addWidget(b_copy)
        hbox.addStretch()
        vbox.addLayout(hbox)
        hbox0.addLayout(vbox)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.albums_artists)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(b_add)
        hbox.addWidget(b_save)
        hbox.addStretch()
        vbox.addLayout(hbox)
        hbox0.addLayout(vbox)

        self.setLayout(hbox0)

    def create_actions(self):
        """keyboard shortcuts
        """
        actions = (
            ('Help', self.help, ['F1', 'Ctrl+H']),
            ('Focus', self.clementine_artists.setFocus, ['Ctrl-L']),
            ('Find', self.find_artist, ['Ctrl+Return', 'Ctrl+F']),
            ('Add', self.add_artist, ['Ctrl+A', 'Ctrl++']),
            ('Save', self.save_all, ['Ctrl+S']))
        for text, callback, keys in actions:
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcuts(keys)
            self.addAction(act)

    def refresh_screen(self):
        """update screen contents
        """
        self.modified = False
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
        self.clementine_artists.setFocus()

    def find_artist(self):
        """search artist in other list

        if not found, try without the first word
        if found, show dialog to confirm match
        """
        item = self.clementine_artists.currentItem()
        if not item:
            return
        search = item.text(0)
        try:
            found = self.lookup[search]
        except KeyError:
            found = False
        if found:
            ## fname, lname = self.finda[found]
            ## name = ', '.join((lname, fname)) if fname else lname
            a_item = self.albums_artists.findItems(found, core.Qt.MatchFixedString,
                                                   2)[0]
            ## self.albums_artists.setCurrentItem(a_item)
            ## self.albums_artists.scrollToItem(a_item)
            ## self.artist_map[search] = found
            ## item.setText(1, 'X')
            ## self.select_next()
            self.update_item(a_item, item)
        else:
            self.artist_buffer = item
            self.add_artist()

    def update_item(self, new_item, from_item):
        """remember changes and make them visible
        """
        self.albums_artists.setCurrentItem(new_item)
        self.albums_artists.scrollToItem(new_item)
        self.artist_map[from_item.text(0)] = new_item.text(2)
        from_item.setText(1, 'X')
        self.modified = True
        next = self.clementine_artists.itemBelow(
            self.clementine_artists.currentItem())
        if next:
            self.clementine_artists.setCurrentItem(next)

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
            qtw.QMessageBox.information(self, self.appname, "Artist doesn't "
                                        "exist on the Clementine side")
            return

        a_item = None
        results = self.albums_artists.findItems(lname, core.Qt.MatchFixedString, 1)
        data = [', '.join((x.text(1), x.text(0))).strip().strip(',')
                for x in results]
        if results:
            selected, ok = qtw.QInputDialog.getItem(self, self.appname,
                                                    'Select Artist', data,
                                                    editable=False)
            if ok:
                a_item = results[data.index(selected)]
        if not a_item:
            self.max_artist += 1
            a_item = qtw.QTreeWidgetItem([fname, lname, str(self.max_artist)])
            self.albums_artists.addTopLevelItem(a_item)
        ## self.albums_artists.setCurrentItem(a_item)
        ## self.albums_artists.scrollToItem(a_item)
        ## self.artist_map[from_item.text(0)] = new_item.text(2)
        ## item.setText(1, 'X')
        ## self.select_next()
        self.update_item(a_item, item)

    def save_all(self):
        """save changes (additions) to Albums database
        """
        data = []
        for i in range(self.albums_artists.topLevelItemCount()):
            item = self.albums_artists.topLevelItem(i)
            data.append((int(item.text(2)), item.text(0), item.text(1)))
        update_artists(data)
        self._parent.artist_map = {x: 'X' for x, y in self.artist_map.items() if y}
        self._parent.artist_map.update({x: '' for x, y in self.artist_map.items()
                                        if not y})
        self.refresh_screen()

    def help(self):
        """explain intended workflow
        """
        workflow = '\n'.join((
            "Intended workflow:",
            "",
            "",
            "Select an artist in the left-hand side column and use the "
            "`Check Artist` button to see if it's present on the right-hand side.",
            "",
            "If it is, the relation between the two will be remembered. You can tell",
            "by the `X` appearing in the Match column.",
            "",
            "If it isn't, the artist name is put in a buffer so one can push the "
            "`Add Artist` button to call up the Add Artist dialog where the "
            "buffered name will be shown in the `last name` field.",
            "",
            "To add the artist to the collection, complete the entries and press "
            "`Save`. After confirmation, this will make the name appear in the list "
            "on the right-hand side and establish the relation (again, indicated "
            "in the Match column).",
            "",
            "To save the entire list to the Albums database, press `Save All`. The "
            "relations will also be saved, they are needed to keep track of artists "
            "that have already been matched.",
            ""))
        qtw.QMessageBox.information(self, self._parent.title, workflow)


class NewArtistDialog(qtw.QDialog):
    """show dialog for adding a new artist
    """
    def __init__(self, parent, name=''):
        super().__init__(parent)
        self.setWindowTitle(self.parent().appname + ' - add artist')
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
            qtw.QMessageBox.information(self, 'AlbumsMatcher', "Enter at least one"
                                        " name or press `Cancel`")
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

    def create_actions(self):
        """keyboard shortcuts
        """
        actions = ()
        for text, callback, keys in actions:
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcuts(keys)
            self.addAction(act)

    def refresh_screen(self):
        """update screen contents
        """
        self.modified = False


class CompareTracks(qtw.QWidget):
    """tracks uit Clementine naast tracks uit Albums zetten
    """
    def create_widgets(self):
        """setup screen
        """
        self.appname = self._parent.title

    def create_actions(self):
        """keyboard shortcuts
        """
        actions = ()
        for text, callback, keys in actions:
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcuts(keys)
            self.addAction(act)

    def refresh_screen(self):
        """update screen contents
        """
        self.modified = False


class MainFrame(qtw.QMainWindow):
    """Het idee hierachter is om bij elke schermwijziging
    het centralwidget opnieuw in te stellen
    Voor deze applicatie is een TabWidget misschien beter op z'n plaats?
    """
    def __init__(self, parent=None):
        self.app = qtw.QApplication(sys.argv)
        self.title = "AlbumsMatcher"
        super().__init__()
        self.setWindowTitle(self.title)
        self.move(300, 50)
        self.resize(600, 650)
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
        appdata = load_appdata()
        if appdata:
            self.artist_map = appdata[0]
        else:
            self.artist_map = {}
        self.pages = collections.OrderedDict()
        for ix, item in enumerate([('artists', CompareArtists(self)),
                                   ('albums', CompareAlbums(self)),
                                   ('tracks', CompareTracks(self))]):
            self.pages[ix] = item
            item[1].first_time = True
            item[1]._parent = self
            self.nb.addTab(item[1], item[0].title())
        self.nb.setCurrentIndex(0)
        self.show()
        self.nb.currentWidget().setFocus()
        sys.exit(self.app.exec_())

    def page_changed(self):
        """pagina aanpassen nadat een andere gekozen is
        """
        ## print('changing page from', self.current, 'to', self.nb.currentIndex())
        if self.current >= 0:
            if self.not_again:
                self.not_again = False
                return
            else:
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
        go.refresh_screen()

    def check_oldpage(self, pageno):
        "check if page can be left"
        print('check leaving page', pageno)
        messages = {0: 'Artist matches have not been saved',
                    1: 'Album matches have not been saved',
                    2: 'Track matches have not been saved'}
        if self.pages[pageno][1].modified:
            qtw.QMessageBox.information(self, self.title, messages[pageno])
            return False
        return True

    def exit(self):
        """shutdown application
        """
        if self.check_oldpage(self.current):
            appdata = [self.artist_map]
            save_appdata(appdata)
            self.close()

if __name__ == '__main__':
    MainFrame()
