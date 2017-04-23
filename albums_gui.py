# simple music database frontend
import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import albums_dml as dmla
import banshee_settings as config

class Start(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.db = dmla.db
        self.studio_searchtype = self.live_searchtype = 1
        self.studio_artistid = self.live_artistid = 0
        self.studio_search_arg = self.live_search_arg = ''
        self.studio_sorttype = self.live_sorttype = 1
        self.next = ''
        self.create_widgets()
        self.show()

    def create_widgets(self):

        gbox = qtw.QGridLayout()

        row = 0
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        hbox.addWidget(qtw.QLabel('Studio Albums', self))
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Selecteer:', self))
        gbox.addLayout(hbox, row, 0)

        self.ask_studio_search = qtw.QComboBox(self)
        self.ask_studio_search.addItems([
            'Niet zoeken, alles tonen',
            'Zoek op Uitvoerende',
            'Zoek op tekst in titel',
            'Zoek op tekst in producer',
            'Zoek op tekst in credits',
            'Zoek op tekst in bezetting',
            ])
        self.ask_studio_search.setMaximumWidth(200)
        self.ask_studio_search.setMinimumWidth(200)
        self.ask_studio_search.setCurrentIndex(self.studio_searchtype)
        gbox.addWidget(self.ask_studio_search, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Kies Uitvoerende:', self))
        self.ask_studio_artist = qtw.QComboBox(self)
        self.ask_studio_artist.addItem('--- Maak een selectie ---')
        self.ask_studio_artist.addItems(self.get_all_artists())
        self.ask_studio_artist.setMaximumWidth(200)
        self.ask_studio_artist.setMinimumWidth(200)
        self.ask_studio_artist.setCurrentIndex(self.studio_artistid)
        hbox.addWidget(self.ask_studio_artist)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Zoektekst voor 3-6:', self))
        self.studio_zoektekst = qtw.QLineEdit(self)
        self.studio_zoektekst.setMaximumWidth(200)
        self.studio_zoektekst.setMinimumWidth(200)
        self.studio_zoektekst.setText(self.studio_search_arg)
        hbox.addWidget(self.studio_zoektekst)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        gbox.addWidget(qtw.QLabel('Sorteer op:', self), row, 0)
        self.ask_studio_sort = qtw.QComboBox(self)
        self.ask_studio_sort.addItems(('Uitvoerende', 'Titel', 'Jaar', 'Niets'))
        self.ask_studio_sort.setMaximumWidth(200)
        self.ask_studio_sort.setMinimumWidth(200)
        self.ask_studio_sort.setCurrentIndex(self.studio_sorttype)
        gbox.addWidget(self.ask_studio_sort, row, 1)

        row+= 1
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
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        hbox.addWidget(qtw.QLabel('Live Concerten', self))
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Selecteer:', self))
        gbox.addLayout(hbox, row, 0)

        self.ask_live_search = qtw.QComboBox(self)
        self.ask_live_search.addItems([
            'Niet zoeken, alles tonen',
            'Zoek op Uitvoerende',
            'Zoek op tekst in locatie',
            'Zoek op tekst in datum',
            ## 'Zoek op tekst in credits',
            'Zoek op tekst in bezetting',
            ])
        self.ask_live_search.setMaximumWidth(200)
        self.ask_live_search.setMinimumWidth(200)
        self.ask_live_search.setCurrentIndex(self.live_searchtype)
        gbox.addWidget(self.ask_live_search, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Kies Uitvoerende:', self))
        self.ask_live_artist = qtw.QComboBox(self)
        self.ask_live_artist.addItem('--- Maak een selectie ---')
        self.ask_live_artist.addItems(self.get_all_artists())
        self.ask_live_artist.setMaximumWidth(200)
        self.ask_live_artist.setMinimumWidth(200)
        self.ask_live_artist.setCurrentIndex(self.live_artistid)
        hbox.addWidget(self.ask_live_artist)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Zoektekst voor 3-5:', self))
        self.live_zoektekst = qtw.QLineEdit(self)
        self.live_zoektekst.setMaximumWidth(200)
        self.live_zoektekst.setMinimumWidth(200)
        self.live_zoektekst.setText(self.live_search_arg)
        hbox.addWidget(self.live_zoektekst)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        gbox.addWidget(qtw.QLabel('Sorteer op:', self), row, 0)

        self.ask_live_sort = qtw.QComboBox(self)
        self.ask_live_sort.addItems(('Uitvoerende', 'Locatie', 'Datum', 'Niets'))
        self.ask_live_sort.setMaximumWidth(200)
        self.ask_live_sort.setMinimumWidth(200)
        self.ask_live_sort.setCurrentIndex(self.live_sorttype)
        gbox.addWidget(self.ask_live_sort, row, 1)

        row+= 1
        hbox = qtw.QHBoxLayout()
        self.live_go = qtw.QPushButton('Selectie uitvoeren', self)
        self.live_new = qtw.QPushButton('Nieuw album opvoeren', self)
        self.live_go.clicked.connect(self.select_concert)
        self.live_new.clicked.connect(self.new_concert)
        hbox.addWidget(self.live_go)
        hbox.addWidget(self.live_new)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row+= 1
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        hbox.addWidget(qtw.QLabel('Uitvoerende Artiesten', self))
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row+= 1
        hbox = qtw.QHBoxLayout()
        self.artist_go = qtw.QPushButton('Lijst tonen/wijzigen', self)
        self.artist_new = qtw.QPushButton('Nieuwe opvoeren', self)
        hbox.addWidget(self.artist_go)
        hbox.addWidget(self.artist_new)
        self.artist_go.clicked.connect(self.view_artists)
        self.artist_new.clicked.connect(self.new_artist)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row+= 1
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row+= 1
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        quit_button = qtw.QPushButton("E&xit", self)
        quit_button.clicked.connect(self.exit)
        hbox.addWidget(quit_button)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        self.setLayout(gbox)

    def select_album(self, *args):
        "get selection type and argument for studio album"
        # -> selectiescherm
        self.studio_searchtype = self.ask_studio_search.currentIndex()
        self.studio_sorttype = self.ask_studio_sort.currentIndex()
        self.studio_artistid = self.ask_studio_artist.currentIndex()
        self.studio_search_arg = self.studio_zoektekst.text()
        self.albumtype = 'studio'
        self.do_select()

    def new_album(self, *args):
        "add a studio album to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.albumtype = 'studio'
        self.do_new()

    def select_concert(self, *args):
        "get selection type and argument for live concert"
        # -> selectiescherm
        self.live_searchtype = self.ask_live_search.currentIndex()
        self.live_sorttype = self.ask_live_sort.currentIndex()
        self.live_artistid = self.ask_live_artist.currentIndex()
        self.live_search_arg = self.live_zoektekst.text()
        self.albumtype = 'live'
        self.do_select()

    def new_concert(self, *args):
        "add a live concert to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.albumtype = 'live'
        self.do_new()

    def view_artists(self, *args):
        "go to artists screen"
        # -> "selectie"scherm in wijzig modus
        self.albumtype = 'artist'
        self.do_select()

    def new_artist(self, *args):
        "add an artist to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.albumtype = 'artist'
        self.do_new()

    def do_select(self):
        if self.albumtype == 'studio':
            self.studio_searchtype
            self.studio_sorttype
            self.studio_artistid
            self.studio_search_arg
        elif self.albumtype == 'live':
            self.live_searchtype
            self.live_sorttype
            self.live_artistid
            self.live_search_arg
        elif self.albumtype == 'artist':
            pass

    def do_new(self):
        if self.albumtype == 'studio':
            pass
        elif self.albumtype == 'live':
            pass
        elif self.albumtype == 'artist':
            pass

    def get_all_artists(self):
        data = dmla.list_artists(self.db)
        self.artist_names = [' '.join((x["first_name"], x['last_name'])).lstrip()
            for x in data]
        self.artist_ids = [x["id"] for x in data]
        return self.artist_names

    def get_artist(self, index):
        """get the selected artist's ID and build a list of albums"""
        if self.initializing: return
        if index != 0:
            data = dmla.list_albums(self.db, self.artist_ids[index - 1])
            self.album_names = [x["name"] for x in data]
            self.album_ids = [x["id"] for x in data]
        self.initializing = True
        self.ask_album.clear()
        self.ask_album.addItems([''] + self.album_names)
        self.initializing = False
        self.tracks_list.clear()

    def get_album(self, index):
        """get the selected album's ID and build a list of tracks"""
        if self.initializing: return
        if index == 0:
            self.tracknames = []
        elif self.dbname == 'albums':
            data = dmla.list_tracks(self.db, self.album_ids[index - 1])
            self.tracknames = [x["name"] for x in data]
            self.trackids = [x["volgnr"] for x in data]
        elif self.dbname == 'banshee':
            data = dmlb.list_tracks(self.db, self.album_ids[index - 1])
            self.tracknames = [x["Title"] for x in data]
            self.trackids = [x["TrackNumber"] for x in data]
        elif self.dbname == 'clementine':
            data = dmlc.list_tracks(self.db, self.artist, self.album_ids[index - 1])
            self.trackids = self.tracknames = [x["title"] for x in data]
        self.tracks_list.clear()
        self.tracks_list.addItems(self.tracknames)

    def exit(self, *args):
        self.close()


class Select(qtw.QWidget):
    """
    Lijst studio albums - selectie: .... gesorteerd op ...
    Snel naar dezelfde selectie voor een andere artiest: <selector>
    <link:> of naar een soortgelijke selectie voor concertopnamen van deze artiest

    Kies een album uit de lijst:
        <link:> artiest - album
        ...

    Of <link:> voer een nieuw album op bij deze selectie </link>
    """

class Detail(qtw.QWidget):
    """
    """

app = qtw.QApplication(sys.argv)
main = Start()
sys.exit(app.exec_())

