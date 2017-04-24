# simple music database frontend
import sys
import types
import collections
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import albums_dml as dmla

class AppData(types.SimpleNamespace):
    end = False

def get_all_artists():
    data = dmla.list_artists(dmla.db)
    artist_names = [' '.join((x["first_name"], x['last_name'])).lstrip()
        for x in data]
    artist_ids = [x["id"] for x in data]
    return artist_names, artist_ids

def get_albums_by_artist(search_for, sort_on):
    """get the selected artist's ID and build a list of albums"""
    if search_type != 2 or search_for != 0:
        return [], []
    data = dmla.list_albums(dmla.db, search_for, sort_on)
    album_names = [x["name"] for x in data]
    album_ids = [x["id"] for x in data]
    return album_names, album_ids

def get_albums_by_text(search_type, search_for, sort_on):
    """get the selected artist's ID and build a list of albums"""
    if search_type == 2 or search_for != 0:
        return [], []
    data = dmla.list_albums(dmla.db, column, search_for, sort_on)
    album_names = [x["name"] for x in data]
    album_ids = [x["id"] for x in data]
    return album_names, album_ids

def get_album(album_id):
    """get the selected album's ID and build a list of tracks"""
    data = dmla.list_tracks(dmla.db, album_id)
    tracknames = [x["name"] for x in data]
    trackids = [x["volgnr"] for x in data]
    return tracknames, trackids


class Start(qtw.QWidget):

    def __init__(self):
        super().__init__()
        ## self.db = dmla.db
        self.appdata = AppData()
        ## self.appdata.end = False
        self.appdata.studio_searchtype = self.appdata.live_searchtype = 1
        self.appdata.studio_artistid = self.appdata.live_artistid = 0
        self.appdata.studio_search_arg = self.appdata.live_search_arg = ''
        self.appdata.studio_sorttype = self.appdata.live_sorttype = 1
        ## self.create_widgets()
        ## self.show()

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
        gbox.addWidget(self.ask_studio_search, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Kies Uitvoerende:', self))
        self.ask_studio_artist = qtw.QComboBox(self)
        self.ask_studio_artist.addItem('--- Maak een selectie ---')
        self.ask_studio_artist.addItems(get_all_artists()[0])
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
        self.ask_studio_sort.addItems(('Uitvoerende', 'Titel', 'Jaar', 'Niets'))
        self.ask_studio_sort.setMaximumWidth(200)
        self.ask_studio_sort.setMinimumWidth(200)
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
        gbox.addWidget(self.ask_live_search, row, 1)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Kies Uitvoerende:', self))
        self.ask_live_artist = qtw.QComboBox(self)
        self.ask_live_artist.addItem('--- Maak een selectie ---')
        self.ask_live_artist.addItems(get_all_artists()[0])
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
        self.ask_live_sort.addItems(('Uitvoerende', 'Locatie', 'Datum', 'Niets'))
        self.ask_live_sort.setMaximumWidth(200)
        self.ask_live_sort.setMinimumWidth(200)
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

    def refresh_screen(self):
        self.ask_studio_search.setCurrentIndex(self.appdata.studio_searchtype)
        self.ask_studio_artist.setCurrentIndex(self.appdata.studio_artistid)
        self.ask_studio_sort.setCurrentIndex(self.appdata.studio_sorttype)
        self.studio_zoektekst.setText(self.appdata.studio_search_arg)
        self.ask_live_search.setCurrentIndex(self.appdata.live_searchtype)
        self.ask_live_artist.setCurrentIndex(self.appdata.live_artistid)
        self.ask_live_sort.setCurrentIndex(self.appdata.live_sorttype)
        self.live_zoektekst.setText(self.appdata.live_search_arg)

    def select_album(self, *args):
        "get selection type and argument for studio album"
        # -> selectiescherm
        self.appdata.searchtype = self.ask_studio_search.currentIndex()
        self.appdata.sorttype = self.ask_studio_sort.currentIndex()
        self.appdata.artistid = self.ask_studio_artist.currentIndex()
        self.appdata.search_arg = self.studio_zoektekst.text()
        if self.appdata.searchtype == 1:
            self.appdata.search_arg = self.appdata.artistid
        self.appdata.albumtype = 'studio'
        self.do_select()

    def new_album(self, *args):
        "add a studio album to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.appdata.albumtype = 'studio'
        self.do_new()

    def select_concert(self, *args):
        "get selection type and argument for live concert"
        # -> selectiescherm
        self.appdata.searchtype = self.ask_live_search.currentIndex()
        self.appdata.sorttype = self.ask_live_sort.currentIndex()
        self.appdata.artistid = self.ask_live_artist.currentIndex()
        self.appdata.search_arg = self.live_zoektekst.text()
        if self.appdata.searchtype == 1:
            self.appdata.search_arg = self.appdata.artistid
        self.appdata.albumtype = 'live'
        self.do_select()

    def new_concert(self, *args):
        "add a live concert to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.appdata.albumtype = 'live'
        self.do_new()

    def view_artists(self, *args):
        "go to artists screen"
        # -> "selectie"scherm in wijzig modus
        self.appdata.albumtype = 'artist'
        self.do_select()

    def new_artist(self, *args):
        "add an artist to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.appdata.albumtype = 'artist'
        self.do_new()

    def do_select(self):
        if self.appdata.albumtype == 'artist':
            go = Artists(self)
        else:
            go = Select(self)
        go.appdata = self.appdata
        go.create_widgets()
        go.show()
        print('now showing selection screen')
        go.setWindowModality(core.Qt.ApplicationModal)
        if self.appdata.end:
            self.exit()
        else:
            self.refresh_screen()
        print('whatever happened to the selection screen?')

    def do_new(self):
        if self.appdata.albumtype == 'artist':
            go = Artists(self)
        else:
            go = Detail(self)
        go.appdata = self.appdata
        go.new_data()
        go.create_widgets()
        go.setWindowModality(core.Qt.ApplicationModal)
        go.show()
        if self.appdata.end:
            self.exit()
        else:
            self.refresh_screen()

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

    def __init__(self):
        super().__init__()
        ## self.albumtype = albumtype
        ## self.searchtype = search
        ## if search == 2:
            ## self.artistid = search_for
        ## self.search_arg = search_for
        ## self.sorttype = sort
        ## self.create_widgets()
        ## self.show()

    def create_widgets(self):

        gbox = qtw.QGridLayout()
        row = 0
        soort = {'studio': 'albums', 'live': 'concerten'}
        text = 'Lijst {} {} - selectie: {} gesorteerd op {}'.format(
            self.appdata.albumtype, soort[self.appdata.albumtype],
            self.appdata.search_arg, self.appdata.sorttype)
        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(text, self))
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Snel naar dezelfde selectie voor een andere '
            'artiest:', self))
        self.ask_artist = qtw.QComboBox(self)
        self.ask_artist.addItem('--- Maak een selectie ---')
        self.ask_artist.addItems(get_all_artists()[0])
        self.ask_artist.setMaximumWidth(200)
        self.ask_artist.setMinimumWidth(200)
        hbox.addWidget(self.ask_artist)
        self.change_artist = qtw.QPushButton('Go', self)
        self.change_artist.setMaximumWidth(40)
        hbox.addWidget(self.change_artist)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('of naar een soortgelijke selectie voor ', self))
        text = ('concertopnamen' if self.appdata.albumtype == 'studio' else
            'studio albums')
        self.change_type = qtw.QPushButton('{} van deze artiest'.format(text), self)
        hbox.addWidget(self.change_type)
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
        text = 'album' if self.appdata.albumtype == 'studio' else 'concert'
        hbox.addWidget(qtw.QLabel('Kies een {} uit de lijst:'.format(text), self))
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        ## if search == 2:
            ## album_names, album_ids = get_albums_by_artist(search_for, sort_on)
        ## else:
            ## album_names, album_ids = get_albums_by_text(search_type, search_for,
                ## sort_on)
        album_names, album_ids = [
            'Hello Sailor - Goodbye from the boys',
            'Amazing Snorkesteijn - The Amazing Snorkesteijn',
            "Grover Beurk - It's the end of an era, or isn't it? Oh well",
            'No Nonsense - Just Kidding'
            ], [1, 2, 3, 4]
        self.go_buttons = []
        for name in album_names:
            row += 1
            hbox = qtw.QHBoxLayout()
            hbox.addSpacing(40)
            hbox.addWidget(qtw.QLabel(name, self))
            hbox.addStretch()
            btn = qtw.QPushButton('Go', self)
            btn.setMaximumWidth(40)
            hbox.addWidget(btn)
            hbox.addSpacing(40)
            self.go_buttons.append(btn)
            gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Of', self))
        self.add_new = qtw.QPushButton('voer een nieuw {} op bij deze selectie'
            ''.format(text), self)
        hbox.addWidget(self.add_new)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
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

    def exit(self, *args):
        self.close()



class Detail(qtw.QWidget):
    """
    """

    def __init__(self):

        super().__init__()
        ## self.albumtype = albumtype
        ## self.searchtype = search
        ## if search == 2:
            ## self.artistid = search_for
        ## self.search_arg = search_for
        ## self.sorttype = sort
        ## self.edit_det = self.edit_trk = self.edit_rec = True
        ## self.select_data()
        ## self.create_widgets()
        ## self.show()

    def new_data(self):
        self.albumnaam = ''
        self.album_names = []
        if self.appdata.albumtype == 'studio':
            self.details = collections.OrderedDict((
                ('Label/jaar:', ''),
                ('Produced by:', ''),
                ('Credits:', ''),
                ('Bezetting:', ''),
                ('Tevens met:', '')))
        else:
            self.details = collections.OrderedDict((
                ('Produced by:', ''),
                ('Credits:', ''),
                ('Bezetting:', ''),
                ('Tevens met:', '')))
        self.tracknames = []
        self.recordings = []
        self.edit_det = True
        self.edit_trk = self.edit_rec = False

    def select_data(self):

        self.albumnaam = ('Worstenbroodje & Co - Overal en Nergens (Zultkop records,'
            ' het jaar 0)')
        ## if search == 2:
            ## album_names, album_ids = get_albums_by_artist(search_for, sort_on)
        ## else:
            ## album_names, album_ids = get_albums_by_text(search_type, search_for,
                ## sort_on)
        self.album_names = ['Hij was een smokkelaar', 'Moederziel Alleen',
            'Overal en Nergens', 'Wat een drama']
        if self.appdata.albumtype == 'studio':
            self.details = collections.OrderedDict((
                ('Label/jaar:', 'Capricorn, 1970'),
                ('Produced by:', 'Tom Dowd'),
                ('Credits:', ''),
                ('Bezetting:', 'Duane Allman - guitars; '
                    'Gregg Allman - organ/vocals; Dicky Betts - guitar/vocals; '
                    'Berry Oakley - bass; Butch Trucks - drums;Jai Johnny Johanson '
                    "('Jaimoe') - drums"),
                ('Tevens met:', '')))
        else:
            self.details = collections.OrderedDict((
                ('Produced by:', ''),
                ('Credits:', ''),
                ('Bezetting:', 'Richard Jobson - vocals, guitar; '
                    'Russell Webb - bass; John McGeoch - guitar; John Doyle - drums'),
                ('Tevens met:', '')))
        self.tracknames = ['Morgen ben ik de bruid', 'Niemand de deur uit',
            'Worstenbroodje en Uitknijpfruit', 'Sluitingstijd']
        self.recordings = ['CD: enkel', 'Vinyl: LP 2 van 2', 'Banshee Music Player']
        self.edit_det = self.edit_trk = self.edit_rec = False

    def create_widgets(self):

        gbox = qtw.QGridLayout()
        row = 0
        soort = {'studio': 'album', 'live': 'concert'}
        text = 'Gegevens van {} {}'.format(soort[self.appdata.albumtype],
            self.albumnaam)
        ## row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(text, self))
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Snel naar een ander {} van deze artiest:'.format(
            soort[self.appdata.albumtype]), self))
        self.ask_album = qtw.QComboBox(self)
        self.ask_album.addItem('--- selecteer titel ---')
        self.ask_album.addItems(self.album_names)
        self.ask_album.setMaximumWidth(200)
        self.ask_album.setMinimumWidth(200)
        hbox.addWidget(self.ask_album)
        self.change_album = qtw.QPushButton('Go', self)
        self.change_album.setMaximumWidth(40)
        hbox.addWidget(self.change_album)
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
        hbox.addWidget(qtw.QLabel("{}gegevens:".format(
            soort[self.appdata.albumtype].title()), self))
        self.chmode_alg = qtw.QPushButton('wijzigen', self)
        hbox.addWidget(self.chmode_alg)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        for title, text in self.details.items():

            row += 1
            hbox = qtw.QHBoxLayout()
            hbox.addSpacing(20)
            hbox.addWidget(qtw.QLabel(title,self))
            gbox.addLayout(hbox, row, 0, 1, 1)
            if self.edit_det:
                win = qtw.QLineEdit(text,self)
            else:
                win = qtw.QLabel(text,self)
            gbox.addWidget(win, row, 1, 1, 2)

        row += 1
        hbox = qtw.QHBoxLayout()
        frm = qtw.QFrame(self)
        frm.setFrameShape(qtw.QFrame.HLine)
        hbox.addWidget(frm)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Tracks:', self))
        self.chmode_alg = qtw.QPushButton('wijzigen', self)
        hbox.addWidget(self.chmode_alg)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        for trackindex, trackname in enumerate(self.tracknames):

            row += 1
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>8}.'.format(trackindex + 1), self))
            if self.edit_trk:
                win = qtw.QLineEdit(trackname, self)
            else:
                win = qtw.QLabel(trackname, self)
            hbox.addWidget(win)
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
        hbox.addWidget(qtw.QLabel('Opnames:', self))
        self.chmode_alg = qtw.QPushButton('wijzigen', self)
        hbox.addWidget(self.chmode_alg)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        for opnindex, opname in enumerate(self.recordings):

            row += 1
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>8}.'.format(opnindex + 1), self))
            if self.edit_rec:
                win = qtw.QLineEdit(opname, self)
            else:
                win = qtw.QLabel(opname, self)
            hbox.addWidget(win)
            hbox.addStretch()
            gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
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

    def exit(self, *args):
        self.close()

class Artists(qtw.QWidget):

    def __init__(self, albumtype='studio', search=2, search_for=5, sort=2):
        super().__init__()

    def create_widgets(self):
        pass

    def exit(self, *args):
        self.close()

app = qtw.QApplication(sys.argv)
main = Start()
## main = Select()
## main = Detail()
main.create_widgets()
main.refresh_screen()
main.show()
sys.exit(app.exec_())

