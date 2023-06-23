"""PyQT version of albums webapp
"""
import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import apps.albums_dml as dmla
import apps.albumsmatcher
"""
s_keuzes = (("alles", "1. Niet zoeken, alles tonen"),
            ("artiest", "2. Uitvoerende: ", "dflt"),
            ("titel", "3. Tekst in Titel"),
            ("producer", "4. Tekst in Producer"),
            ("credits", "5. Tekst in Credits"),
            ("bezetting", "6. Tekst in Bezetting"))
s_sorts = (("artiest", "Uitvoerende"),
           ("titel", "Titel"),
           ("jaar", "Jaar", "dflt"),
           ("geen", "Niets"))
l_keuzes = (("alles", "1. Niet zoeken, alles tonen"),
            ("artiest", "2. Uitvoerende: ", "dflt"),
            ("locatie", "3. Tekst in Locatie"),
            ("datum", "4. Tekst in Datum"),
            ("bezetting", "5. Tekst in Bezetting"))
l_sorts = (("artiest", "Uitvoerende"),
           ("locatie", "Locatie/datum", "dflt"),
           ("geen", "Niets"))
"""
# these should actually also be in the Albums database - or at least importable from dmla
TYPETXT = {'studio': 'album', 'live': 'concert'}
# SELTXT = {'studio': ['Niet zoeken, alles tonen',
#                      'Zoek op Uitvoerende',
#                      'Zoek op tekst in titel',
#                      'Zoek op tekst in producer',
#                      'Zoek op tekst in credits',
#                      'Zoek op tekst in bezetting'],
#           'live': ['Niet zoeken, alles tonen',
#                    'Zoek op Uitvoerende',
#                    'Zoek op tekst in locatie',
#                    'Zoek op tekst in datum',
#                    'Zoek op tekst in bezetting']}
SELTXT = {'studio': [dmla.s_keuzes[0][1][3:]] + [f'Zoek op {x[1][3:]}' for x in dmla.s_keuzes[1:]],
          'live': [dmla.l_keuzes[0][1][3:]] + [f'Zoek op {x[1][3:]}' for x in dmla.l_keuzes[1:]]}
# SELCOL = {'studio': ['', 'artist', 'titel', 'producer', 'credits', 'bezetting'],
#           'live': ['', 'artist', 'locatie', 'datum', 'bezetting']}
SELCOL = {'studio': [[''] + [x[0] for x in dmla.s_keuzes[1:]]],
          'live': [[''] + [x[0] for x in dmla.l_keuzes[1:]]]}
SORTTXT = {'studio': ['Niet sorteren', 'Uitvoerende', 'Titel', 'Jaar'],
           'live': ['Niet sorteren', 'Uitvoerende', 'Locatie', 'Datum']}
SORTCOL = {'studio': ['', 'artist', 'titel', 'jaar'],
           'live': ['', 'artist', 'locatie', 'datum']}
RECTYPES = ('Cassette',       # dmla.my.o_soort
            'CD: Enkel',
            'CD: Dubbel',
            'Vinyl: 1LP',
            'Vinyl: 2LP',
            'Vinyl: 3LP',
            'Vinyl: single',
            'Vinyl: 12" single',
            'Tape',
            'MP3 directory',
            'Banshee music player',
            'Clementine music player')


class MainFrame(qtw.QMainWindow):
    """Het idee hierachter is om bij elke schermwijziging
    het centralwidget opnieuw in te stellen
    """
    def __init__(self):
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.move(300, 50)
        ## self.resize(400, 600)
        self.artist = None
        self.album = None
        self.albumtype = ''
        self.searchtype = 1
        self.search_arg = ''
        self.sorttype = ''
        self.old_seltype = 0
        self.albumdata = {}
        self.end = False
        self.albums = []
        self.windows = []
        self.show()
        self.do_start()
        sys.exit(self.app.exec_())

    def get_all_artists(self):
        """refresh list of artist convenience variables
        """
        self.all_artists = get_artist_list()
        self.artists = self.all_artists
        self.artist_names = [x.get_name() for x in self.artists]
        self.artist_ids = [x.id for x in self.artists]

    def do_start(self):
        """show initial sceen
        """
        self.artist_filter = ''
        self.get_all_artists()
        go = Start(self)
        self.windows.append(go)
        go.create_widgets()
        go.refresh_screen()
        self.setCentralWidget(go)

    def do_select(self):
        """show selection screen
        """
        if self.albumtype == 'artist':
            go = Artists(self)
        else:
            if self.searchtype == 1:
                self.albums = get_albums_by_artist(self.albumtype, self.artist.id,
                                                   self.sorttype)
            else:
                self.albums = get_albums_by_text(self.albumtype, self.searchtype,
                                                 self.search_arg, self.sorttype)
            go = Select(self)
        self.windows.append(go)
        go.create_widgets()
        go.refresh_screen()
        self.setCentralWidget(go)

    def do_new(self, keep_sel=False):
        """show screen for adding a new album or artist
        """
        if self.albumtype == 'artist':
            if NewArtistDialog(self).exec_() == qtw.QDialog.Accepted:
                self.get_all_artists()
                self.do_select()
        else:
            self.albumdata = get_album(0, self.albumtype)
            self.do_edit_alg(new=True, keep_sel=keep_sel)

    def do_detail(self):
        """show albums details
        """
        if self.albumtype == 'artist':
            go = Artists(self)
        else:
            self.albumdata = get_album(self.album.id, self.albumtype)
            go = Detail(self)
        self.windows.append(go)
        go.create_widgets()
        go.refresh_screen()
        self.setCentralWidget(go)

    def do_edit_alg(self, new=False, keep_sel=False):
        """edit album details
        """
        go = EditDetails(self)
        self.windows.append(go)
        go.create_widgets()
        if new:
            go.new_data(keep_sel)
        go.refresh_screen()
        self.setCentralWidget(go)

    def do_edit_trk(self):
        """edit track list
        """
        go = EditTracks(self)
        self.windows.append(go)
        go.create_widgets()
        go.refresh_screen()
        self.setCentralWidget(go)

    def do_edit_rec(self):
        """edit recordings list
        """
        go = EditRecordings(self)
        self.windows.append(go)
        go.create_widgets()
        go.refresh_screen()
        self.setCentralWidget(go)

    def start_import_tool(self):
        """get albums from music library
        """
        albumsmatcher.MainFrame(app=self.app)


class Start(qtw.QWidget):
    """show initial screen asking what to do
    """
    def create_widgets(self):
        """setup screen
        """
        gbox = qtw.QGridLayout()

        row = 0
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Studio Albums', self))
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Selecteer:', self))
        gbox.addLayout(hbox, row, 0)

        self.ask_studio_search = qtw.QComboBox(self)
        self.ask_studio_search.addItems(SELTXT['studio'])
        self.ask_studio_search.setMaximumWidth(200)
        self.ask_studio_search.setMinimumWidth(200)
        gbox.addWidget(self.ask_studio_search, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Kies Uitvoerende:', self))
        self.ask_studio_artist = qtw.QComboBox(self)
        self.ask_studio_artist.addItem('--- Maak een selectie ---')
        self.ask_studio_artist.setMaximumWidth(200)
        self.ask_studio_artist.setMinimumWidth(200)
        hbox.addWidget(self.ask_studio_artist)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Zoektekst voor 3-6:', self))
        self.studio_zoektekst = qtw.QLineEdit(self)
        self.studio_zoektekst.setMaximumWidth(200)
        self.studio_zoektekst.setMinimumWidth(200)
        hbox.addWidget(self.studio_zoektekst)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        gbox.addWidget(qtw.QLabel('Sorteer op:', self), row, 0)
        self.ask_studio_sort = qtw.QComboBox(self)
        self.ask_studio_sort.addItems(SORTTXT['studio'])
        self.ask_studio_sort.setMaximumWidth(200)
        self.ask_studio_sort.setMinimumWidth(200)
        gbox.addWidget(self.ask_studio_sort, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        self.studio_go = qtw.QPushButton('Selectie uitvoeren', self)
        self.studio_new = qtw.QPushButton('Nieuw album opvoeren', self)
        self.studio_go.clicked.connect(self.select_album)
        self.studio_new.clicked.connect(self.new_album)
        hbox.addWidget(self.studio_go)
        hbox.addWidget(self.studio_new)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)
        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Live Concerten', self))
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Selecteer:', self))
        gbox.addLayout(hbox, row, 0)

        self.ask_live_search = qtw.QComboBox(self)
        self.ask_live_search.addItems(SELTXT['live'])
        self.ask_live_search.setMaximumWidth(200)
        self.ask_live_search.setMinimumWidth(200)
        gbox.addWidget(self.ask_live_search, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Kies Uitvoerende:', self))
        self.ask_live_artist = qtw.QComboBox(self)
        self.ask_live_artist.addItem('--- Maak een selectie ---')
        self.ask_live_artist.setMaximumWidth(200)
        self.ask_live_artist.setMinimumWidth(200)
        hbox.addWidget(self.ask_live_artist)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Zoektekst voor 3-5:', self))
        self.live_zoektekst = qtw.QLineEdit(self)
        self.live_zoektekst.setMaximumWidth(200)
        self.live_zoektekst.setMinimumWidth(200)
        hbox.addWidget(self.live_zoektekst)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        gbox.addWidget(qtw.QLabel('Sorteer op:', self), row, 0)

        self.ask_live_sort = qtw.QComboBox(self)
        self.ask_live_sort.addItems(SORTTXT['live'])
        self.ask_live_sort.setMaximumWidth(200)
        self.ask_live_sort.setMinimumWidth(200)
        gbox.addWidget(self.ask_live_sort, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        self.live_go = qtw.QPushButton('Selectie uitvoeren', self)
        self.live_new = qtw.QPushButton('Nieuw album opvoeren', self)
        self.live_go.clicked.connect(self.select_concert)
        self.live_new.clicked.connect(self.new_concert)
        hbox.addWidget(self.live_go)
        hbox.addWidget(self.live_new)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)
        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Uitvoerende Artiesten', self))
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        self.artist_go = qtw.QPushButton('Lijst tonen/wijzigen', self)
        self.artist_new = qtw.QPushButton('Nieuwe opvoeren', self)
        hbox.addWidget(self.artist_go)
        hbox.addWidget(self.artist_new)
        self.artist_go.clicked.connect(self.view_artists)
        self.artist_new.clicked.connect(self.new_artist)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        btn = qtw.QPushButton('&Import Data', self)
        btn.clicked.connect(self.parent().start_import_tool)
        gbox.addLayout(exitbutton(self, self.exit, btn), row, 0, 1, 3)

        self.setLayout(gbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.ask_studio_artist.addItems(self.parent().artist_names)
        self.ask_live_artist.addItems(self.parent().artist_names)
        if self.parent().albumtype == 'studio':
            widgets = [self.ask_studio_search, self.ask_studio_artist,
                       self.studio_zoektekst, self.ask_studio_sort]
        elif self.parent().albumtype == 'live':
            widgets = [self.ask_live_search, self.ask_live_artist,
                       self.live_zoektekst, self.ask_live_sort]
        else:
            # set defaults
            self.ask_studio_search.setCurrentIndex(self.parent().searchtype)
            self.ask_studio_sort.setCurrentIndex(3)
            self.ask_live_search.setCurrentIndex(self.parent().searchtype)
            self.ask_live_sort.setCurrentIndex(2)
            return
        widgets[0].setCurrentIndex(self.parent().searchtype)
        if self.parent().searchtype == 1:
            if self.parent().artist:  # .id:
                ## chosen = self.parent().ids.index(self.parent().artistid)
                chosen = self.parent().artist_ids.index(self.parent().artist.id)
                widgets[1].setCurrentIndex(chosen + 1)
        if self.parent().searchtype < 2:
            widgets[2].clear()
        else:
            widgets[2].setText(self.parent().search_arg)
        widgets[3].setCurrentText(self.parent().sorttype)

    def select_album(self):
        "get selection type and argument for studio album"
        self._select('studio', self.ask_studio_search, self.ask_studio_artist,
                     self.studio_zoektekst, self.ask_studio_sort)

    def select_concert(self):
        "get selection type and argument for live concert"
        self._select('live', self.ask_live_search, self.ask_live_artist,
                     self.live_zoektekst, self.ask_live_sort)

    def _select(self, albumtype, typewin, actwin, argwin, sortwin):
        "get selection type and argument"
        text = ''
        self.parent().searchtype = typewin.currentIndex()
        if self.parent().searchtype == 1:
            chosen = actwin.currentIndex()
            if chosen:
                self.parent().artist = self.parent().artists[chosen - 1]
                self.parent().search_arg = self.parent().artist
            else:
                text = "Selecteer een uitvoerende"
        elif self.parent().searchtype > 0:
            self.parent().search_arg = argwin.text()
            if not self.parent().search_arg:
                text = "Geef een zoekargument op"
        if text:
            qtw.QMessageBox.information(self, 'Albums', text)
            return
        self.parent().albumtype = albumtype
        self.parent().sorttype = sortwin.currentText()
        self.parent().do_select()

    def new_album(self):
        "add a studio album to the collection"
        self._new('studio')

    def new_concert(self):
        "add a live concert to the collection"
        self._new('live')

    def _new(self, albumtype):
        "add an album to the collection"
        self.parent().albumtype = albumtype
        self.parent().do_new()

    def view_artists(self):
        "go to artists screen"
        self.parent().albumtype = 'artist'
        self.parent().do_select()

    def new_artist(self):
        "add an artist to the collection"
        self.parent().albumtype = 'artist'
        self.parent().do_new()

    def exit(self):
        """shutdown application"""
        self.parent().close()


class Select(qtw.QWidget):
    """show a selection of albums or concerts
    """
    def create_widgets(self):
        """setup screen
        """
        vbox = qtw.QVBoxLayout()
        vbox.addLayout(newline(self))

        hbox = qtw.QHBoxLayout()
        self.heading = qtw.QLabel("", self)
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)

        labeltxt = 'Snel naar dezelfde selectie voor '
        labeltxt2 = 'naar een soortgelijke selectie voor '
        if self.parent().searchtype == 1:
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel(labeltxt + 'een andere artiest:', self))
            self.ask_artist = qtw.QComboBox(self)
            self.ask_artist.addItem('--- Maak een selectie ---')
            self.ask_artist.addItems(self.parent().artist_names)
            self.ask_artist.setMaximumWidth(200)
            self.ask_artist.setMinimumWidth(200)
            hbox.addWidget(self.ask_artist)
            self.change_artist = qtw.QPushButton('Go', self)
            self.change_artist.setMaximumWidth(40)
            self.change_artist.clicked.connect(self.other_artist)
            hbox.addWidget(self.change_artist)
            hbox.addStretch()
            vbox.addLayout(hbox)
            labeltxt = 'of ' + labeltxt2
        else:
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel(labeltxt + 'een andere waarde:', self))
            self.ask_zoekarg = qtw.QLineEdit(self)
            self.ask_zoekarg.setMaximumWidth(200)
            self.ask_zoekarg.setMinimumWidth(200)
            hbox.addWidget(self.ask_zoekarg)
            self.change_zoekarg = qtw.QPushButton('Go', self)
            self.change_zoekarg.setMaximumWidth(40)
            self.change_zoekarg.clicked.connect(self.other_search)
            hbox.addWidget(self.change_zoekarg)
            hbox.addStretch()
            vbox.addLayout(hbox)
            labeltxt = 'of ' + labeltxt2

        if not (self.parent().albumtype == 'studio'
                and self.parent().searchtype in (3, 4)):
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel(labeltxt, self))
            self.change_type = qtw.QPushButton('', self)
            self.change_type.clicked.connect(self.other_albumtype)
            hbox.addWidget(self.change_type)
            ## hbox.addWidget(qtw.QLabel(' van deze artiest', self))
            hbox.addStretch()
            vbox.addLayout(hbox)

        vbox.addLayout(newline(self))

        hbox = qtw.QHBoxLayout()
        self.kiestekst = qtw.QLabel('Kies een item uit de lijst:', self)
        hbox.addWidget(self.kiestekst)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.go_buttons = []
        self.frm = qtw.QFrame(self)
        vbox2 = qtw.QVBoxLayout()
        for album in self.parent().albums:
            name = str(album)
            hbox = qtw.QHBoxLayout()
            ## hbox.addSpacing(40)
            hbox.addWidget(qtw.QLabel(name, self))
            hbox.addStretch()
            btn = qtw.QPushButton('Go', self)
            btn.setMaximumWidth(40)
            btn.clicked.connect(self.todetail)
            hbox.addWidget(btn)
            hbox.addSpacing(40)
            self.go_buttons.append(btn)
            vbox2.addLayout(hbox)
        self.frm.setLayout(vbox2)
        scrl = qtw.QScrollArea()
        scrl.setWidget(self.frm)
        vbox.addWidget(scrl)

        ## vbox.addStretch()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Of', self))
        self.add_new = qtw.QPushButton('voer een nieuw item op bij deze selectie',
                                       self)
        self.add_new.clicked.connect(self.add_new_to_sel)
        hbox.addWidget(self.add_new)
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addLayout(newline(self))
        vbox.addLayout(button_strip(self, 'Start'))
        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        soort = {'studio': 'albums', 'live': 'concerten'}
        if self.parent().searchtype == 1:
            searchtext = 'Artist = {}'.format(self.parent().artist.get_name())
        else:
            if self.parent().searchtype:
                searchtext = '{} contains "{}"'.format(
                    SELCOL[self.parent().albumtype][self.parent().searchtype],
                    self.parent().search_arg)
            else:
                searchtext = 'geen selectie'
        self.heading.setText('Lijst {} {} - selectie: {} gesorteerd op {}'.format(
            self.parent().albumtype, soort[self.parent().albumtype],
            searchtext, self.parent().sorttype))
        if self.parent().albumtype == 'studio':
            if self.parent().searchtype not in (3, 4):
                self.change_type.setText('concertopnamen')
            itemtype = 'album'
        else:
            self.change_type.setText('studio albums')
            itemtype = 'concert'
        self.kiestekst.setText('Kies een {} uit de lijst:'.format(itemtype))
        self.add_new.setText('voer een nieuw {} op bij deze selectie'.format(
            itemtype))

    def other_artist(self):
        """read self.ask_artist for artist and change self.parent().artistid
        """
        chosen = self.ask_artist.currentIndex()
        if chosen:
            self.parent().search_arg = self.parent().artist_ids[chosen - 1]
            if self.parent().searchtype == 1:
                self.parent().artist = self.parent().artists[chosen - 1]
            self.parent().do_select()

    def other_search(self):
        """read self.ask_zoekarg and change self.parent().search_arg
        """
        test = self.ask_zoekarg.text()
        if test:
            self.parent().search_arg = test
            self.parent().do_select()

    def other_albumtype(self):
        """determine other type of selection and change accordingly, also change
        self.parent().albumtype
        """
        if self.parent().albumtype == 'studio':
            self.parent().albumtype = 'live'
            if self.parent().searchtype == 5:
                self.parent().searchtype = 4
            elif self.parent().searchtype == 2 and self.parent().old_seltype:
                self.parent().searchtype = self.parent().old_seltype
        else:
            self.parent().albumtype = 'studio'
            if self.parent().searchtype == 4:
                self.parent().searchtype = 5
            elif self.parent().searchtype in (2, 3):
                self.parent().old_seltype = self.parent().searchtype
                if self.parent().searchtype == 3:
                    self.parent().searchtype = 2
        self.parent().do_select()

    def todetail(self):
        """determine which button was clicked and change accordingly
        """
        for ix, btn in enumerate(self.go_buttons):
            if self.sender() == btn:
                self.parent().album = self.parent().albums[ix]
                break
        if not self.parent().album:
            print('waaat')
        self.parent().do_detail()

    def add_new_to_sel(self):
        """prefill selection in new album field(s)
        """
        self.parent().do_new(keep_sel=True)

    def exit(self):
        """shutdown application"""
        self.parent().close()


class Detail(qtw.QWidget):
    """show information about a specific album or concert
    """
    def create_widgets(self):
        """setup screen
        """
        gbox = qtw.QGridLayout()
        row = 0
        self.heading = qtw.QLabel('', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        self.quickchange = qtw.QLabel('Snel naar een ander item in deze selectie:', self)
        hbox.addWidget(self.quickchange)
        self.ask_album = qtw.QComboBox(self)
        self.ask_album.addItem('--- selecteer titel ---')
        self.ask_album.addItems([x.name for x in self.parent().albums])
        self.ask_album.setMaximumWidth(200)
        self.ask_album.setMinimumWidth(200)
        hbox.addWidget(self.ask_album)
        self.change_album = qtw.QPushButton('Go', self)
        self.change_album.setMaximumWidth(40)
        self.change_album.clicked.connect(self.other_album)
        hbox.addWidget(self.change_album)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        self.subheading = qtw.QLabel('Detailgegevens:', self)
        hbox.addWidget(self.subheading)
        self.chmode_alg = qtw.QPushButton('wijzigen', self)
        self.chmode_alg.clicked.connect(self.edit_alg)
        hbox.addWidget(self.chmode_alg)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        self.detailwins = []

        frm = qtw.QFrame(self)
        gbox2 = qtw.QGridLayout()
        row2 = -1
        for caption, text in self.parent().albumdata['details']:
            row2 += 1
            hbox = qtw.QHBoxLayout()
            hbox.addSpacing(20)
            hbox.addWidget(qtw.QLabel(caption, self))
            gbox2.addLayout(hbox, row2, 0, 1, 1)
            win = qtw.QLabel(text, self)
            gbox2.addWidget(win, row2, 1, 1, 2)
        frm.setLayout(gbox2)
        scrl = qtw.QScrollArea()
        scrl.setWidget(frm)
        row += 1
        gbox.addWidget(scrl, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Tracks:', self))
        self.chmode_trk = qtw.QPushButton('wijzigen', self)
        self.chmode_trk.clicked.connect(self.edit_trk)
        hbox.addWidget(self.chmode_trk)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        self.trackwins = []

        row += 1
        frm = qtw.QFrame(self)
        vbox2 = qtw.QVBoxLayout()
        for trackindex, data in sorted(self.parent().albumdata['tracks'].items()):
            trackname, author, cred = data
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>8}.'.format(trackindex), self))
            tracktext = '{} ({})'.format(trackname, author) if author else trackname
            win = qtw.QLabel(tracktext, self)
            hbox.addWidget(win)
            hbox.addStretch()
            vbox2.addLayout(hbox)
            if cred:
                vbox2.addWidget(qtw.QLabel(cred, self))
        frm.setLayout(vbox2)
        scrl = qtw.QScrollArea()
        scrl.setWidget(frm)
        gbox.addWidget(scrl, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Opnames:', self))
        self.chmode_rec = qtw.QPushButton('wijzigen', self)
        self.chmode_rec.clicked.connect(self.edit_rec)
        hbox.addWidget(self.chmode_rec)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        self.recwins = []

        row += 1
        frm = qtw.QFrame(self)
        vbox2 = qtw.QVBoxLayout()
        for opnindex, opname in enumerate(self.parent().albumdata['opnames']):
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>8}.'.format(opnindex + 1), self))
            win = qtw.QLabel(' '.join(opname), self)
            hbox.addWidget(win)
            hbox.addStretch()
            vbox2.addLayout(hbox)
        frm.setLayout(vbox2)
        scrl = qtw.QScrollArea()
        scrl.setWidget(frm)
        gbox.addWidget(scrl, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        gbox.addLayout(button_strip(self, 'Select', 'Start'), row, 0, 1, 3)

        row += 1
        gbox.addLayout(exitbutton(self, self.exit), row, 0, 1, 3)

        self.setLayout(gbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.heading.setText(build_heading(self, readonly=True))
        self.quickchange.setText('Snel naar een ander {} in deze selectie:'.format(
            TYPETXT[self.parent().albumtype]))
        self.subheading.setText("{}gegevens:".format(
            TYPETXT[self.parent().albumtype].title()))

    def other_album(self):
        """Determine which other album to show and do so
        """
        test = self.ask_album.currentIndex()
        if test:
            self.parent().album = self.parent().albums[test - 1]
            self.parent().do_detail()

    def edit_alg(self):
        "Go to Edit Details screen"
        self.parent().do_edit_alg()

    def edit_trk(self):
        "Go to Edit Tracks screen"
        self.parent().do_edit_trk()

    def edit_rec(self):
        "Go to Edit Recordings screen"
        self.parent().do_edit_rec()

    def exit(self):
        """shutdown application"""
        self.parent().close()


class EditDetails(qtw.QWidget):
    """show album details in editable form
    """
    def create_widgets(self):
        """setup screen
        """
        self.new_album = self.keep_sel = False
        self.first_time = True
        gbox = qtw.QGridLayout()
        row = 0
        self.heading = qtw.QLabel('', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        data = [('Uitvoerende:', self.parent().albumdata['artist']),
                ['Albumtitel:', self.parent().albumdata['titel']]]
        if self.parent().albumtype == 'live':
            data[1][0] = 'Locatie/datum:'
        data += self.parent().albumdata['details']
        self.screendata = []
        for caption, text in data:
            row += 1
            hbox = qtw.QHBoxLayout()
            hbox.addSpacing(20)
            lbl = qtw.QLabel(caption, self)
            if caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
                vbox = qtw.QVBoxLayout()
                vbox.addWidget(lbl)
                vbox.addStretch()
                hbox.addLayout(vbox)
            else:
                hbox.addWidget(lbl)
            gbox.addLayout(hbox, row, 0, 1, 1)
            if caption == 'Uitvoerende:':
                win = qtw.QComboBox(self)
                win.addItem('--- Maak een selectie ---')
                listdata = self.parent().artist_names
                win.addItems(listdata)
                if text:
                    win.setCurrentIndex(listdata.index(text.get_name()) + 1)
            elif caption == 'Label/jaar:':
                hbox2 = qtw.QHBoxLayout()
                text = text.split(', ')
                if len(text) == 1:
                    text.append('')
                win_l = qtw.QLineEdit(text[0], self)
                win_l.setMaximumWidth(200)
                win_l.setMinimumWidth(200)
                hbox2.addWidget(win_l)
                win_y = qtw.QLineEdit(text[1], self)
                win_y.setMaximumWidth(80)
                win_y.setMinimumWidth(80)
                hbox2.addWidget(win_y)
                hbox2.addStretch()
            elif caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
                win = qtw.QTextEdit(text, self)
            else:
                win = qtw.QLineEdit(text, self)
            if caption == 'Label/jaar:':
                gbox.addLayout(hbox2, row, 1, 1, 2)
                self.screendata.append((lbl, win_l, win_y))
            else:
                gbox.addWidget(win, row, 1, 1, 2)
                self.screendata.append((lbl, win))

        row += 1
        vbox = qtw.QVBoxLayout()
        vbox.addStretch()
        gbox.addLayout(vbox, row, 0, 1, 3)

        row += 1
        buttons = ['Cancel', 'Go', 'GoBack', 'Select', 'Start']
        if not self.parent().album:
            buttons.remove('Cancel')
            if not self.parent().search_arg:
                buttons.remove('Select')
        self.bbox = button_strip(self, *buttons)
        gbox.addLayout(self.bbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(exitbutton(self, self.exit), row, 0, 1, 3)

        self.setLayout(gbox)

    def new_data(self, keep_sel=False):
        """Prepare to show empty screen for entering new album
        """
        self.keep_sel = keep_sel
        self.new_album = True
        self.albumnaam = ''
        self.album_names = []
        self.tracknames = []
        self.recordings = []
        self.edit_det = True
        self.edit_trk = self.edit_rec = False

        if not keep_sel:
            return
        # prefill field(s) based on the selection we're in
        # loop over screendata fields to select the field to prefill
        for lbl, win in self.screendata[:2]:
            caption = lbl.text()
            if self.parent().searchtype == 1 and caption == 'Uitvoerende:':
                ## win.setCurrentIndex([x for x in self.parent().artists].index(
                    ## self.parent().artist) + 1)
                win.setCurrentIndex(self.parent().artist_ids.index(
                    self.parent().search_arg.id) + 1)
            elif self.parent().searchtype == 2:
                if self.parent().albumtype == 'studio' and caption == 'Albumtitel:':
                    win.setText(self.parent().search_arg)
                elif self.parent().albumtype == 'live' and caption == 'Locatie/datum:':
                    win.setText(self.parent().search_arg)
            elif self.parent().searchtype == 3:
                if self.parent().albumtype == 'studio' and caption == 'Produced by:':
                    win.setText(self.parent().search_arg)
                elif self.parent().albumtype == 'live' and caption == 'Locatie/datum:':
                    win.setText(self.parent().search_arg)
            elif self.parent().searchtype == 4:
                if self.parent().albumtype == 'studio' and caption == 'Credits:':
                    win.setText(self.parent().search_arg)
                elif self.parent().albumtype == 'live' and caption == 'Bezetting:':
                    win.setText(self.parent().search_arg)
            elif self.parent().searchtype == 5:
                if self.parent().albumtype == 'studio' and caption == 'Bezetting:':
                    win.setText(self.parent().search_arg)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.heading.setText(build_heading(self))
        if not self.first_time:
            for i in range(self.bbox.count()):
                btn = self.bbox.itemAt(i).widget()
                if btn:  # try:
                    test = btn.text()
                else:  # except AttributeError:
                    continue
                if test == "Uitvoeren en terug":
                    btn.setText("Naar Details")
                    btn.clicked.connect(self.parent().do_detail)
                    break

    def submit(self, goback=False):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """
        def replace_details(caption, value):
            "replace value for a given entry"
            changed = False
            for ix, item in enumerate(self.parent().albumdata['details']):
                if item[0] == caption:
                    if value != item[1]:
                        self.parent().albumdata['details'][ix] = (caption, value)
                        changed = True
                    break
            return changed
        is_changed = False
        for fields in self.screendata:
            lbl, win = fields[:2]
            caption = lbl.text()
            if caption == 'Uitvoerende:':
                test = win.currentText()
                ix = win.currentIndex() - 1
                if test != self.parent().albumdata['artist']:
                    self.parent().albumdata['artist'] = self.parent().artists[ix]
                    self.parent().artist = self.parent().albumdata['artist']
                    is_changed = True
            elif caption in ('Albumtitel:', 'Locatie/datum:'):
                test = win.text()
                if test != self.parent().albumdata['titel']:
                    self.parent().albumdata['titel'] = test
                    is_changed = True
            elif caption == 'Label/jaar:':
                win_l, win_y = fields[1:]
                test = replace_details(
                    caption, ', '.join((win_l.text(), win_y.text())))
                if test:
                    is_changed = True
            elif caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
                test = replace_details(caption, win.toPlainText())
                if test:
                    is_changed = True
            else:
                test = replace_details(caption, win.text())
                if test:
                    is_changed = True

        if is_changed:
            albumid = 0 if self.new_album else self.parent().album.id
            album, ok = dmla.update_album_details(albumid, self.parent().albumdata)
            # eigenlijk wil ik hier de nieuwe waarden teruggeven om ze op het scherm te zetten
            # zodat je kunt zien wat er daadwerkelijk in de database zit / is bijgewerkt
            if ok:
                if not goback:
                    if self.new_album:
                        self.add_another()
                    else:
                        qtw.QMessageBox.information(self, 'Albums',
                                                    'Details updated')
            else:
                qtw.QMessageBox.information(self, 'Albums',
                                            'Something went wrong, please try again')
                return
            self.parent().album = album
            if self.new_album:
                self.parent().albums.append(album)
                self.new_album = False
            # eigenlijk zou je hierna de data opnieuw moeten ophalen en het scherm opnieuw
            # opbouwen - wat nu alleen gebeurt als je naar het detailscherm gaat
        else:
            qtw.QMessageBox.information(self, 'Albums', 'Nothing changed')

        if self.first_time:
            self.first_time = False
            self.refresh_screen()

    def add_another(self):
        """Show message with possibility to continue adding items
        """
        message = qtw.QMessageBox(qtw.QMessageBox.Information, 'Albums', "Album "
                                  "added", buttons=qtw.QMessageBox.Ok, parent=self)
        message.setDefaultButton(qtw.QMessageBox.Ok)
        message.setEscapeButton(qtw.QMessageBox.Ok)
        next = message.addButton('&Add Another', qtw.QMessageBox.AcceptRole)
        message.exec_()
        if message.clickedButton() == next:
            self.parent().do_new(keep_sel=self.keep_sel)

    def submit_and_back(self):
        """return to previous (details) screen after completion
        """
        self.submit(goback=True)
        if self.first_time:
            if self.keep_sel:
                self.parent().do_select()
            else:
                self.parent().do_start()
        else:
            self.parent().do_detail()

    def exit(self):
        """shutdown application"""
        self.parent().close()


class EditTracks(qtw.QWidget):
    """show list of tracks in editable form
    """
    def create_widgets(self):
        """setup screen
        """
        self.first_time = True
        vbox = qtw.QVBoxLayout()
        row = 0
        self.heading = qtw.QLabel('tracks', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)

        row += 1
        vbox.addLayout(newline(self))

        frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout()
        self.line = 1
        hbox2 = qtw.QHBoxLayout()
        lbl = qtw.QLabel('Title\nCredits', self)
        lbl.setMinimumWidth(304)
        lbl.setMaximumWidth(304)
        hbox2.addWidget(lbl)
        hbox2.addWidget(qtw.QLabel('Author\n', self))
        self.gbox.addLayout(hbox2, self.line, 1)
        self.widgets = []
        for trackindex, data in sorted(self.parent().albumdata['tracks'].items()):
            ## trackname, author, cred = data
            ## self.add_track_fields(trackindex, trackname, author, text)
            self.add_track_fields(trackindex, *data)

        self.tracks = len(self.parent().albumdata['tracks'])
        self.vbox2.addLayout(self.gbox)
        self.vbox2.addStretch()
        frm.setLayout(self.vbox2)
        ## frm.setLayout(self.gbox)
        self.scrl = qtw.QScrollArea()
        self.scrl.setWidget(frm)
        self.scrl.setWidgetResizable(True)
        vbox.addWidget(self.scrl)

        hbox = qtw.QHBoxLayout()
        self.add_new = qtw.QPushButton('Nieuw track', self)
        self.add_new.clicked.connect(self.add_new_item)
        hbox.addWidget(self.add_new)
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addLayout(newline(self))
        buttons = ['Cancel', 'Go', 'GoBack', 'Select', 'Start']
        if not self.parent().album:
            buttons.remove('Cancel')
            if not self.parent().search_arg:
                buttons.remove('Select')
        self.bbox = button_strip(self, *buttons)
        vbox.addLayout(self.bbox)

        vbox.addLayout(exitbutton(self, self.exit))
        self.setLayout(vbox)

    def add_track_fields(self, trackindex, trackname='', author='', text=''):
        """Build line in edit area with track data (or not)
        """
        line = self.line + 1
        widgets = []
        self.gbox.addWidget(qtw.QLabel('{:>8}.'.format(trackindex), self), line, 0)
        hbox = qtw.QHBoxLayout()
        win = qtw.QLineEdit(trackname, self)
        win.setMaximumWidth(300)
        win.setMinimumWidth(300)
        hbox.addWidget(win)
        widgets.append(win)
        win = qtw.QLineEdit(author, self)
        win.setMaximumWidth(200)
        win.setMinimumWidth(200)
        hbox.addWidget(win)
        widgets.append(win)
        self.gbox.addLayout(hbox, line, 1)
        line += 1
        win = qtw.QTextEdit(text, self)
        win.setMaximumWidth(508)
        win.setMinimumWidth(508)
        win.setMaximumHeight(38)
        win.setMinimumHeight(38)
        self.gbox.addWidget(win, line, 1)
        widgets.append(win)
        self.widgets.append(widgets)
        self.line = line

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.heading.setText(build_heading(self))

    def add_new_item(self):
        """Create new line to enter new track
        """
        self.tracks += 1
        self.add_track_fields(self.tracks)
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 68)
        vbar.setValue(vbar.maximum())

    def submit(self, skip_confirm=False):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """
        tracks = []
        for ix, wins in enumerate(self.widgets):
            screen = (wins[0].text(), wins[1].text(), wins[2].toPlainText())
            ix += 1
            try:
                data = self.parent().albumdata['tracks'][ix]
            except KeyError:
                tracks.append((ix, screen))
                continue
            changed = False
            for i, item in enumerate(data):
                if screen[i] != item:
                    changed = True
            if changed:
                item = screen
                self.parent().albumdata['tracks'][ix] = item
                tracks.append((ix, item))

        if tracks:
            ok = dmla.update_album_tracks(self.parent().album.id, tracks)
            if not skip_confirm:
                if ok:
                    qtw.QMessageBox.information(self, 'Albums', 'Tracks updated')
                else:
                    qtw.QMessageBox.information(self, 'Albums', 'Something'
                                                ' went wrong, please try again')
            # eigenlijk zou je hierna de data opnieuw moeten ophalen en het scherm opnieuw
            # opbouwen - wat nu alleen gebeurt als je naar het detailscherm gaat
        else:
            qtw.QMessageBox.information(self, 'Albums', 'Nothing changed')

        if self.first_time:
            self.first_time = False
            self.refresh_screen()

    def submit_and_back(self):
        """return to details screen after completion
        """
        self.submit(skip_confirm=True)
        self.parent().do_detail()

    def exit(self):
        """shutdown application"""
        self.parent().close()


class EditRecordings(qtw.QWidget):
    """show list of recordings in editable form
    """
    def create_widgets(self):
        """setup screen
        """
        self.first_time = True
        vbox = qtw.QVBoxLayout()
        self.heading = qtw.QLabel('opnames', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)

        vbox.addLayout(newline(self))

        self.recwins = []

        frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        self.vbox2.addStretch()
        for opnindex, opname in enumerate(self.parent().albumdata['opnames']):
            self.add_rec_fields(opnindex, opname)

        self.recs = len(self.parent().albumdata['opnames'])
        frm.setLayout(self.vbox2)
        self.scrl = qtw.QScrollArea()
        self.scrl.setWidget(frm)
        self.scrl.setWidgetResizable(True)
        vbox.addWidget(self.scrl)

        hbox = qtw.QHBoxLayout()
        self.add_new = qtw.QPushButton('Nieuwe opname', self)
        self.add_new.clicked.connect(self.add_new_item)
        hbox.addWidget(self.add_new)
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addLayout(newline(self))

        buttons = ['Cancel', 'Go', 'GoBack', 'Select', 'Start']
        if not self.parent().album:
            buttons.remove('Cancel')
            if not self.parent().search_arg:
                buttons.remove('Select')
        self.bbox = button_strip(self, *buttons)
        vbox.addLayout(self.bbox)

        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def add_rec_fields(self, opnindex, opname=None):
        """Build line in edit area with recording data (or not)"""
        if opname:
            opnsoort, opntext = opname
            opnsoort = RECTYPES.index(opnsoort) + 1
        else:
            opnsoort, opntext = 0, ''
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('{:>8}.'.format(opnindex + 1), self))
        cb = qtw.QComboBox(self)
        cb.addItem('--- Maak een selectie ---')
        cb.addItems(RECTYPES)
        if opname:
            cb.setCurrentIndex(opnsoort)
        hbox.addWidget(cb)

        txt = qtw.QLineEdit(opntext, self)
        txt.setMaximumWidth(200)
        txt.setMinimumWidth(200)
        hbox.addWidget(txt)
        hbox.addStretch()
        self.vbox2.insertLayout(self.vbox2.count() - 1, hbox)
        self.recwins.append((cb, txt))

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.heading.setText(build_heading(self))

    def add_new_item(self):
        """Create empty line to enter new recording data
        """
        self.recs += 1
        self.add_rec_fields(self.recs)
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 36)
        vbar.setValue(vbar.maximum())

    def submit(self, skip_confirm=False):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """
        recordings = []
        for ix, wins in enumerate(self.recwins):
            screen = (wins[0].currentText(), wins[1].text())
            ## ix += 1
            try:
                data = self.parent().albumdata['opnames'][ix]
            except IndexError:
                recordings.append((ix, screen))
                continue
            changed = False
            for i, item in enumerate(data):
                if screen[i] != item:
                    changed = True
            if changed:
                item = screen
                self.parent().albumdata['opnames'][ix] = item
                recordings.append((ix, item))

        if recordings:
            ok = dmla.update_album_recordings(self.parent().album.id, recordings)
            if not skip_confirm:
                if ok:
                    qtw.QMessageBox.information(self, 'Albums', 'Recordings updated')
                else:
                    qtw.QMessageBox.information(self, 'Albums', 'Something '
                                                'went wrong, please try again')
            # eigenlijk zou je hierna de data opnieuw moeten ophalen en het scherm opnieuw
            # opbouwen - wat nu alleen gebeurt als je naar het detailscherm gaat
        else:
            if not skip_confirm:
                qtw.QMessageBox.information(self, 'Albums', 'Nothing changed')

        if self.first_time:
            self.first_time = False
            self.refresh_screen()

    def submit_and_back(self):
        """Return to details screen after completion
        """
        self.submit(skip_confirm=True)
        self.parent().do_detail()

    def exit(self):
        """shutdown application"""
        self.parent().close()


class Artists(qtw.QWidget):
    """show list of artists
    """
    def create_widgets(self):
        """setup screen
        """
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        self.heading = qtw.QLabel('Artiestenlijst - gefilterd op', self)
        hbox.addWidget(self.heading)
        self.ask_filter = qtw.QLineEdit(self.parent().artist_filter, self)
        self.artist_list = self.parent().artists
        hbox.addWidget(self.ask_filter)
        self.set_filter = qtw.QPushButton('&Go', self)
        self.set_filter.clicked.connect(self.filter)
        hbox.addWidget(self.set_filter)
        vbox.addLayout(hbox)
        vbox.addLayout(newline(self))

        self.fields = []
        self.frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        self.last_artistid = 0
        for artist in self.artist_list:
            test = artist.id
            if test > self.last_artistid:
                self.last_artistid = test
            self.add_artist_line(test, artist.first_name, artist.last_name)
        self.vbox2.addStretch()
        self.frm.setLayout(self.vbox2)
        self.scrl = qtw.QScrollArea()
        self.scrl.setWidget(self.frm)
        self.scrl.setWidgetResizable(True)
        vbox.addWidget(self.scrl)

        vbox.addLayout(button_strip(self, 'Edit', 'New', 'Start'))
        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def filter(self):
        """callback for Filter button
        """
        filter = self.ask_filter.text()
        if filter:
            self.parent().artists = dmla.list_artists(filter)
        else:
            self.parent().artists = self.parent().all_artists
        self.parent().artist_filter = filter
        self.parent().do_select()

    def add_artist_line(self, itemid, first_name='', last_name=''):
        """Create line in edit area with artist data (or not)
        """
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('{:>3}.'.format(itemid), self))
        win_f = qtw.QLineEdit(first_name, self)
        hbox.addWidget(win_f)
        win_l = qtw.QLineEdit(last_name, self)
        win_l.setMaximumWidth(300)
        win_l.setMinimumWidth(300)
        hbox.addWidget(win_l)
        self.vbox2.addLayout(hbox)
        self.fields.append((win_f, win_l))

    def refresh_screen(self):
        """bring screen up-to-date
        """
        pass

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """
        self.parent().app.changeOverrideCursor(gui.QCursor(core.Qt.WaitCursor))
        changes = []
        changed = False
        for ix, wins in enumerate(self.fields):
            new = False
            if ix < len(self.parent().artists):
                fname, lname = wins[0].text(), wins[1].text()
                artist = self.parent().artists[ix]
                if fname != artist.first_name or lname != artist.last_name:
                    changed = True
                    changes.append((artist.id, wins[0].text(), wins[1].text()))
            else:
                new = True
                changes.append((0, wins[0].text(), wins[1].text()))
        if changed or new:
            dmla.update_artists(changes)
        else:
            qtw.QMessageBox.information(self, 'Albums', 'Nothing changed')
        self.parent().app.restoreOverrideCursor()
        self.parent().get_all_artists()
        self.parent().do_select()

    def new(self):
        """open empty line to add new artist
        """
        self.last_artistid += 1
        self.add_artist_line(self.last_artistid)
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 34)
        vbar.setValue(vbar.maximum())

    def exit(self):
        """shutdown application"""
        self.parent().close()


class NewArtistDialog(qtw.QDialog):
    """show dialog for adding a new artist
    """
    def __init__(self, parent):
        super().__init__(parent)
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('First name:', self), 0, 0)
        self.first_name = qtw.QLineEdit(self)
        gbox.addWidget(self.first_name, 0, 1)
        gbox.addWidget(qtw.QLabel('Last name:', self), 1, 0)
        self.last_name = qtw.QLineEdit(self)
        gbox.addWidget(self.last_name, 1, 1)
        gbox.addWidget(qtw.QLabel('Names wil be shown sorted on last name'), 2, 0, 1, 2)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('Cancel', self)
        btn.clicked.connect(self.reject)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('Update', self)
        btn.clicked.connect(self.update)
        hbox.addWidget(btn)
        hbox.addStretch()
        gbox.addLayout(hbox, 3, 0, 1, 2)
        self.setLayout(gbox)

    def update(self):
        """when finished: propagate changes to database
        """
        # wijzigingen doorvoeren in de database
        data = dmla.my.Act.objects.create()
        data.first_name = self.first_name.text()
        data.last_name = self.last_name.text()
        data.save()
        self.accept()


def get_artist_list():
    """get artist data from the database
    """
    return [x for x in dmla.list_artists()]


def get_albums_by_artist(albumtype, search_for, sort_on):
    """get the selected artist's ID and build a list of albums
    """
    return [x for x in dmla.list_albums_by_artist(albumtype, search_for, sort_on)]


def get_albums_by_text(albumtype, search_type, search_for, sort_on):
    """get the selected artist's ID and build a list of albums
    """
    if albumtype == 'studio':
        search_on = {0: '*', 2: 'name', 3: 'produced_by', 4: 'credits',
                       5: 'bezetting'}[search_type]
    elif albumtype == 'live':
        search_on = {0: '*', 2: 'name', 3: 'name', 4: 'produced_by',
                       5: 'bezetting'}[search_type]
    return [x for x in dmla.list_albums_by_search(albumtype, search_on, search_for, sort_on)]


def get_album(album_id, albumtype):
    """get the selected album's data
    """
    result = {'titel': '',
              'artist': '',
              # 'artistid': '',
              'artist_name': '',
              'details': [('Label/jaar:', ''),
                          ('Produced by:', ''),
                          ('Credits:', ''),
                          ('Bezetting:', ''),
                          ('Tevens met:', '')],
              'tracks': {},
              'opnames': []}
    if album_id:
        album = dmla.list_album_details(album_id)
        result['titel'] = album.name
        result['artist'] = album.artist
        # result['artistid'] = album.artist.id
        result['artist_name'] = album.artist.get_name()
        text = album.label
        if album.release_year:
            if text:
                text += ', '
            text += str(album.release_year)
        result['details'] = [('Label/jaar:', text),
                             ('Produced by:', album.produced_by),
                             ('Credits:', album.credits),
                             ('Bezetting:', album.bezetting),
                             ('Tevens met:', album.additional)]
        if album:
            result['tracks'] = {x.volgnr: (x.name, x.written_by, x.credits)
                                for x in dmla.list_tracks(album_id)}
            result['opnames'] = [(x.type, x.oms) for x in
                                 dmla.list_recordings(album_id)]
    if albumtype == 'live':
        result['details'].pop(0)
    return result


def build_heading(win, readonly=False):
    """Generate heading text for screen
    """
    typetext = TYPETXT[win.parent().albumtype]
    actname = win.parent().albumdata['artist']
    album = win.parent().albumdata['titel']
    if not actname or not album:
        text = f'Opvoeren nieuw {typetext}'
    else:
        wintext = win.heading.text()
        newtext = ''
        for text in ('tracks', 'opnames'):
            if wintext == text:
                newtext = f': {wintext}'
                break
            elif wintext.endswith(text):
                newtext = f': {text}'
                break
        text = 'G' if readonly else 'Wijzigen g'
        text = f'{text}egevens van {typetext} {actname} - {album}{newtext}'
    return text


def newline(parent):
    """create a horizontal line in the GUI
    """
    hbox = qtw.QHBoxLayout()
    frm = qtw.QFrame(parent)
    frm.setFrameShape(qtw.QFrame.HLine)
    hbox.addWidget(frm)
    return hbox


def button_strip(parent, *buttons):
    """create a strip containing buttons for the supplied actions
    """
    hbox = qtw.QHBoxLayout()
    hbox.addStretch()
    if 'Cancel' in buttons:
        btn = qtw.QPushButton("Afbreken", parent)
        btn.clicked.connect(parent.parent().do_detail)
        hbox.addWidget(btn)
    if 'Go' in buttons:
        btn = qtw.QPushButton("Uitvoeren", parent)
        btn.clicked.connect(parent.submit)
        hbox.addWidget(btn)
    if 'GoBack' in buttons:
        btn = qtw.QPushButton("Uitvoeren en terug", parent)
        btn.clicked.connect(parent.submit_and_back)
        hbox.addWidget(btn)
    if 'Edit' in buttons:
        btn = qtw.QPushButton("Wijzigingen doorvoeren", parent)
        btn.clicked.connect(parent.submit)
        hbox.addWidget(btn)
    if 'New' in buttons:
        btn = qtw.QPushButton("Nieuwe opvoeren", parent)
        btn.clicked.connect(parent.new)
        hbox.addWidget(btn)
    if 'Select' in buttons:
        btn = qtw.QPushButton("Terug naar Selectie", parent)
        btn.clicked.connect(parent.parent().do_select)
        hbox.addWidget(btn)
    if 'Start' in buttons:
        btn = qtw.QPushButton("Terug naar Startscherm", parent)
        btn.clicked.connect(parent.parent().do_start)
        hbox.addWidget(btn)
    hbox.addStretch()
    return hbox


def exitbutton(parent, callback, extrawidget=None):
    """create exit button that activates callback
    since it's always the same one, maybe passing it in is not necessary?
    it was originally intended to just close the current screen
    """
    hbox = qtw.QHBoxLayout()
    hbox.addStretch()
    if extrawidget:
        hbox.addWidget(extrawidget)
    btn = qtw.QPushButton("E&xit", parent)
    btn.clicked.connect(callback)
    hbox.addWidget(btn)
    hbox.addStretch()
    return hbox
