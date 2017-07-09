# simple music database frontend
import sys
import types
import collections
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import albums_dml as dmla
SELTXT = {
    'studio': [
            'Niet zoeken, alles tonen',
            'Zoek op Uitvoerende',
            'Zoek op tekst in titel',
            'Zoek op tekst in producer',
            'Zoek op tekst in credits',
            'Zoek op tekst in bezetting',
            ],
    'live': [
            'Niet zoeken, alles tonen',
            'Zoek op Uitvoerende',
            'Zoek op tekst in locatie',
            'Zoek op tekst in datum',
            ## 'Zoek op tekst in credits',
            'Zoek op tekst in bezetting',
            ]}
SELCOL = {
    'studio': ['', 'artist', 'titel', 'producer',  'credits', 'bezetting'],
    'live': ['',  'artist', 'locatie', 'datum', 'bezetting']}
SORTTXT = {
    'studio': ['Niet sorteren', 'Uitvoerende', 'Titel', 'Jaar'],
    'live': ['Niet sorteren', 'Uitvoerende', 'Locatie', 'Datum']}
SORTCOL = {
    'studio': ['', 'artist', 'titel', 'jaar'],
    'live': ['',  'artist', 'locatie', 'datum']}
RECTYPES = (
    'Cassette',
    'CD: Enkel',
    'CD: Dubbel',
    'Vinyl: 1LP',
    'Vinyl: 2LP',
    'Vinyl: 3LP',
    'Vinyl: single',
    'Vinyl: 12" single',
    'Tape',
    'MP3 directory',
    'Banshee music player',)

def get_artist_list():
    """get artist data from the database
    """
    return dmla.list_artists(dmla.db)


def get_all_artists():
    """retrieve artists and keys
    """
    data = get_artist_list()
    artist_names = [' '.join((x["first_name"], x['last_name'])).lstrip()
        for x in data]
    artist_ids = [x["id"] for x in data]
    return artist_names, artist_ids


def get_albums_by_artist(albumtype, search_for, sort_on):
    """get the selected artist's ID and build a list of albums
    """
    data = dmla.list_albums_by_artist(dmla.db, albumtype, search_for, sort_on)
    album_names = [x["name"] for x in data]
    album_ids = [x["id"] for x in data]
    return album_names, album_ids


def get_albums_by_text(albumtype, search_type, search_for, sort_on):
    """get the selected artist's ID and build a list of albums
    """
    if albumtype == 'studio':
        search_type = {0: '*', 2: 'name', 3: 'produced_by', 4: 'credits',
            5: 'bezetting'}[search_type]
    elif albumtype == 'live':
        search_type = {0: '*', 2: 'name', 3: 'name', 4: 'produced_by',
            5: 'bezetting'}[search_type]
    data = dmla.list_albums_by_search(dmla.db, albumtype, search_type, search_for,
        sort_on)
    album_names = [x["name"] for x in data]
    album_ids = [x["id"] for x in data]
    album_artists = [' '.join((x["first_name"], x["last_name"])).lstrip()
        for x in data]
    return album_artists, album_names, album_ids


def get_album(album_id, albumtype):
    """get the selected album's data
    """
    data = dmla.list_album_details(dmla.db, album_id)
    result = {'titel': data['name'],
              'artist': ' '.join((data['first_name'], data['last_name'])).strip()}
    ## result['Label/jaar:'] = ', '.join((data['label'], data['release_year']))
    text = data['label']
    if data['release_year']:
        if text:
            text += ', '
        text += str(data['release_year'])
    result['details'] = [
        ('Label/jaar:', text),
        ('Produced by:', data['produced_by']),
        ('Credits:', data['credits']),
        ('Bezetting:', data['bezetting']),
        ('Tevens met:', data['additional'])]
    if albumtype == 'live':
        result['details'].pop(1)
    data = dmla.list_tracks(dmla.db, album_id)
    result['tracks'] = [(x["name"], x["volgnr"]) for x in data]
    data = dmla.list_recordings(dmla.db, album_id)
    result['opnames'] = [(x["type"], x["oms"]) for x in data]
    return result


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


def exitbutton(parent, callback):
    """create exit button that activates callback
    since it's always the same one, maybe passing it in is not necessary?
    it was originally intended to just close the current screen
    """
    hbox = qtw.QHBoxLayout()
    hbox.addStretch()
    btn = qtw.QPushButton("E&xit", parent)
    btn.clicked.connect(callback)
    hbox.addWidget(btn)
    hbox.addStretch()
    return hbox


class Start(qtw.QWidget):
    """show initial screen asking what to do
    """
    def __init__(self, parent):
        super().__init__(parent)

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
        gbox.addLayout(newline(self), row, 0, 1, 3)
        row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Live Concerten', self))
        gbox.addLayout(hbox, row, 0, 1, 3)
        ## row += 1
        ## hbox = qtw.QHBoxLayout()
        ## frm = qtw.QFrame(self)
        ## frm.setFrameShape(qtw.QFrame.HLine)
        ## hbox.addWidget(frm)
        ## gbox.addLayout(hbox, row, 0, 1, 3)

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
        gbox.addLayout(hbox, row, 0, 1, 3)
        row+= 1
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Uitvoerende Artiesten', self))
        ## frm = qtw.QFrame(self)
        ## frm.setFrameShape(qtw.QFrame.HLine)
        ## hbox.addWidget(frm)
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
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row+= 1
        gbox.addLayout(exitbutton(self, self.exit), row, 0, 1, 3)

        self.setLayout(gbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.names, self.ids = get_all_artists()
        self.ask_studio_artist.addItems(self.names)
        self.ask_live_artist.addItems(self.names)
        if self.parent().albumtype == 'studio':
            widgets = [self.ask_studio_search, self.ask_studio_artist,
                       self.studio_zoektekst, self.ask_studio_sort]
        elif self.parent().albumtype == 'live':
            widgets = [self.ask_live_search, self.ask_live_artist,
                       self.live_zoektekst, self.ask_live_sort]
        else:
            return
        widgets[0].setCurrentIndex(self.parent().searchtype)
        if self.parent().searchtype == 1:
            widgets[1].setCurrentIndex(self.parent().artistid - 1)
        if self.parent().searchtype < 2:
            widgets[2].clear()
        else:
            widgets[2].setText(self.parent().search_arg)
        widgets[3].setCurrentText(self.parent().sorttype)

    def select_album(self, *args):
        "get selection type and argument for studio album"
        # -> selectiescherm
        self.parent().searchtype = self.ask_studio_search.currentIndex()
        self.parent().sorttype = self.ask_studio_sort.currentText()
        chosen = self.ask_studio_artist.currentIndex()
        self.parent().artistid = self.ids[chosen - 1]
        self.parent().search_arg = self.studio_zoektekst.text()
        if self.parent().searchtype == 1:
            self.parent().search_arg = self.parent().artistid
        self.parent().albumtype = 'studio'
        self.parent().do_select()

    def new_album(self, *args):
        "add a studio album to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.parent().albumtype = 'studio'
        self.parent().do_new()

    def select_concert(self, *args):
        "get selection type and argument for live concert"
        # -> selectiescherm
        self.parent().searchtype = self.ask_live_search.currentIndex()
        self.parent().sorttype = self.ask_live_sort.currentText()
        chosen = self.ask_live_artist.currentIndex()
        self.parent().artistid = self.ids[chosen - 1]
        self.parent().search_arg = self.live_zoektekst.text()
        if self.parent().searchtype == 1:
            self.parent().search_arg = self.parent().artistid
        self.parent().albumtype = 'live'
        self.parent().do_select()

    def new_concert(self, *args):
        "add a live concert to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.parent().albumtype = 'live'
        self.parent().do_new()

    def view_artists(self, *args):
        "go to artists screen"
        # -> "selectie"scherm in wijzig modus
        self.parent().albumtype = 'artist'
        self.parent().do_select()

    def new_artist(self, *args):
        "add an artist to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.parent().albumtype = 'artist'
        self.parent().do_new()

    def exit(self, *args):
        """shutdown application"""
        self.parent().close()


class Select(qtw.QWidget):
    """show a selection of albums or concerts
    """
    def __init__(self, parent):
        super().__init__(parent)

    def create_widgets(self):
        """setup screen
        """
        vbox = qtw.QVBoxLayout()
        vbox.addLayout(newline(self))

        hbox = qtw.QHBoxLayout()
        self.heading = qtw.QLabel("", self)
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        # TODO: variabel maken m.b.t. zoeken op tekst (dan tekstvak ipv combobox)
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
        self.change_artist.clicked.connect(self.other_artist)
        hbox.addWidget(self.change_artist)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('of naar een soortgelijke selectie voor ', self))
        self.change_type = qtw.QPushButton('', self)
        self.change_type.clicked.connect(self.other_albumtype)
        hbox.addWidget(self.change_type)
        hbox.addWidget(qtw.QLabel(' van deze artiest', self))
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addLayout(newline(self))

        hbox = qtw.QHBoxLayout()
        self.kiestekst = qtw.QLabel('Kies een item uit de lijst:', self)
        hbox.addWidget(self.kiestekst)
        hbox.addStretch()
        vbox.addLayout(hbox)

        if self.parent().searchtype == 1:
            self.parent().album_artists = []
            self.parent().album_names, self.parent().album_ids = get_albums_by_artist(
                self.parent().albumtype, self.parent().artistid,
                self.parent().sorttype)
        else:
            self.parent().album_artists, self.parent().album_names, self.parent().album_ids = get_albums_by_text(
                self.parent().albumtype, self.parent().searchtype,
                self.parent().search_arg, self.parent().sorttype)
        self.go_buttons = []
        self.frm = qtw.QFrame(self)
        vbox2 = qtw.QVBoxLayout()
        for ix, name in enumerate(self.parent().album_names):
            if self.parent().album_artists:
                name = ' - '.join((self.parent().album_artists[ix], name))
            hbox = qtw.QHBoxLayout()
            hbox.addSpacing(40)
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

        vbox.addStretch()

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
            names, ids = get_all_artists()
            searchtext = 'Artist = {}'.format(
                names[ids.index(self.parent().search_arg)])
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
            self.change_type.setText('concertopnamen')
            itemtype  = 'album'
        else:
            self.change_type.setText('studio albums')
            itemtype = 'concert'
        self.kiestekst.setText('Kies een {} uit de lijst:'.format(itemtype))
        ## if self.parent().searchtype == 1:
            ## self.album_names, self.album_ids = get_albums_by_artist(
                ## self.parent().albumtype, self.parent().artistid,
                ## self.parent().sorttype)
        ## else:
            ## self.album_names, self.album_ids = get_albums_by_text(
                ## self.parent().albumtype, self.parent().searchtype,
                ## self.parent().search_arg, self.parent().sorttype)
        self.add_new.setText('voer een nieuw {} op bij deze selectie'.format(
            itemtype))

    def other_artist(self, *args):
        """read self.ask_artist for artist and change self.parent().artistid
        """
        self.parent().do_select()

    def other_albumtype(self, *args):
        """determine other type of selection and change accordingly, also change
        self.parent().albumtype
        """
        self.parent().do_select()

    def todetail(self, *args):
        """determine which button was clicked and change accordingly
        """
        for ix, btn in enumerate(self.go_buttons):
            if self.sender() == btn:
                self.parent().albumid = self.parent().album_ids[ix]
                break
        self.parent().do_detail()

    def add_new_to_sel(self, *args, **kwargs):
        """
        """
        self.parent().do_new(keep_sel=True)

    def exit(self, *args):
        """shutdown application"""
        self.parent().close()


class Detail(qtw.QWidget):
    """show information about a specific album or concert
    """
    def __init__(self, parent):

        super().__init__(parent)
        self.det_captions = {
            'studio': ['Label/jaar:', 'Produced by:', 'Credits:',
                       'Bezetting:', 'Tevens met:'],
            'live': ['Locatie/datum:', 'Produced by:', 'Credits:',
                     'Bezetting:', 'Tevens met:']}

    def create_widgets(self):
        """setup screen
        """
        self.parent().albumdata = get_album(self.parent().albumid,
                                            self.parent().albumtype)
        gbox = qtw.QGridLayout()
        row = 0
        ## row += 1
        self.heading = qtw.QLabel('', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        row += 1
        hbox = qtw.QHBoxLayout()
        self.quickchange = qtw.QLabel('Snel naar een ander item in deze selectie:',
            self)
        hbox.addWidget(self.quickchange)
        self.ask_album = qtw.QComboBox(self)
        self.ask_album.addItem('--- selecteer titel ---')
        self.ask_album.addItems(self.parent().album_names)
        self.ask_album.setMaximumWidth(200)
        self.ask_album.setMinimumWidth(200)
        hbox.addWidget(self.ask_album)
        self.change_album = qtw.QPushButton('Go', self)
        self.change_album.setMaximumWidth(40)
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
        ## for num, title in enumerate(self.det_captions[self.parent().albumtype]):
        for caption, text in self.parent().albumdata['details']:
            row2 += 1
            hbox = qtw.QHBoxLayout()
            hbox.addSpacing(20)
            ## hbox.addWidget(qtw.QLabel(title, self))
            hbox.addWidget(qtw.QLabel(caption, self))
            gbox2.addLayout(hbox, row2, 0, 1, 1)
            ## win = qtw.QLabel(self.details[num], self)
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
        ## self.edit_trk = False

        row += 1
        frm = qtw.QFrame(self)
        vbox2 = qtw.QVBoxLayout()
        for trackname, trackindex in self.parent().albumdata['tracks']:
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>8}.'.format(trackindex), self))
            win = qtw.QLabel(trackname, self)
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
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Opnames:', self))
        self.chmode_rec = qtw.QPushButton('wijzigen', self)
        self.chmode_rec.clicked.connect(self.edit_rec)
        hbox.addWidget(self.chmode_rec)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 0, 1, 3)

        self.recwins = []
        ## self.edit_rec = False

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

        row+= 1
        gbox.addLayout(button_strip(self, 'Select', 'Start'), row, 0, 1, 3)

        row+= 1
        gbox.addLayout(exitbutton(self, self.exit), row, 0, 1, 3)

        self.setLayout(gbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        soort = {'studio': 'album', 'live': 'concert'}
        self.heading.setText('Gegevens van {} {} - {}'.format(
            soort[self.parent().albumtype], self.parent().albumdata['artist'],
            self.parent().albumdata['titel']))
        self.quickchange.setText('Snel naar een ander {} in deze selectie:'.format(
            soort[self.parent().albumtype]))
        self.subheading.setText("{}gegevens:".format(
            soort[self.parent().albumtype].title()))

    ## def select_data(self):

        ## self.albumnaam = ('Worstenbroodje & Co - Overal en Nergens (Zultkop records,'
            ## ' het jaar 0)')
        ## if self.parent().albumtype == 'studio':
            ## self.details = collections.OrderedDict((
                ## ('Label/jaar:', 'Capricorn, 1970'),
                ## ('Produced by:', 'Tom Dowd'),
                ## ('Credits:', ''),
                ## ('Bezetting:', 'Duane Allman - guitars; '
                    ## 'Gregg Allman - organ/vocals; Dicky Betts - guitar/vocals; '
                    ## 'Berry Oakley - bass; Butch Trucks - drums;Jai Johnny Johanson '
                    ## "('Jaimoe') - drums"),
                ## ('Tevens met:', '')))
        ## else:
            ## self.details = collections.OrderedDict((
                ## ('Produced by:', ''),
                ## ('Credits:', ''),
                ## ('Bezetting:', 'Richard Jobson - vocals, guitar; '
                    ## 'Russell Webb - bass; John McGeoch - guitar; John Doyle - drums'),
                ## ('Tevens met:', '')))
        ## self.tracknames = ['Morgen ben ik de bruid', 'Niemand de deur uit',
            ## 'Worstenbroodje en Uitknijpfruit', 'Sluitingstijd']
        ## self.recordings = ['CD: enkel', 'Vinyl: LP 2 van 2', 'Banshee Music Player']
        ## self.details = ['Nooit Meer Slapen Records, 1970', 'Hendrikus Jansonius',
            ## '', 'Alle instrumenten bespeeld als door een wonder','']

    def edit_alg(self):
        self.parent().do_edit_alg()

    def edit_trk(self):
        self.parent().do_edit_trk()

    def edit_rec(self):
        self.parent().do_edit_rec()

    def exit(self, *args):
        """shutdown application"""
        self.parent().close()

class EditDetails(qtw.QWidget):
    """show album details in editable form
    """
    def __init__(self, parent):

        super().__init__(parent)
        ## self.det_captions = {
            ## 'studio': ['Uitvoerende:', 'Albumtitel:', 'Label:',
                ## 'Jaar:', 'Produced by:', 'Credits:', 'Bezetting:', 'Tevens met:'],
            ## 'live': ['Uitvoerende:', 'Locatie:', 'Datum:', 'Produced by:',
                ## 'Credits:', 'Bezetting:', 'Tevens met:']}
        ## self.det_captions = ['Label/jaar:', 'Produced by:', 'Credits:',
            ## 'Bezetting:', 'Tevens met:']

    def create_widgets(self):
        """setup screen
        """
        gbox = qtw.QGridLayout()
        row = 0
        ## row += 1
        self.heading = qtw.QLabel('', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        gbox.addLayout(hbox, row, 0, 1, 3)

        row += 1
        gbox.addLayout(newline(self), row, 0, 1, 3)

        ## self.details = ['Worstenbroodje & Co', 'Overal en Nergens',
            ## 'Zultkop records', 'het jaar 0', 'Hendrikus Jansonius',
            ## '', 'Alle instrumenten bespeeld als door een wonder','']
        self.detailwins = []

        data = [('Uitvoerende:', self.parent().albumdata['artist']),
                ('Albumtitel:', self.parent().albumdata['titel'])]
        if self.parent().albumtype == 'live':
            data[1][0] = 'Locatie/datum:'
        data += self.parent().albumdata['details']
        for caption, text in data:
            row += 1
            hbox = qtw.QHBoxLayout()
            hbox.addSpacing(20)
            if caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
                vbox = qtw.QVBoxLayout()
                vbox.addWidget(qtw.QLabel(caption, self))
                vbox.addStretch()
                hbox.addLayout(vbox)
            else:
                hbox.addWidget(qtw.QLabel(caption, self))
            gbox.addLayout(hbox, row, 0, 1, 1)
            if caption == 'Uitvoerende:':
                win = qtw.QComboBox(self)
                win.addItem('--- Maak een selectie ---')
                listdata = get_all_artists()[0]
                win.addItems(listdata)
                win.setCurrentIndex(listdata.index(text) + 1)
                ## win.setMaximumWidth(200)
                ## win.setMinimumWidth(200)
            elif caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
                win = qtw.QTextEdit(text, self)
            else:
                win = qtw.QLineEdit(text, self)
            self.detailwins.append(win)
            gbox.addWidget(win, row, 1, 1, 2)

        row+= 1
        vbox = qtw.QVBoxLayout()
        vbox.addStretch()
        gbox.addLayout(vbox, row, 0, 1, 3)

        row+= 1
        gbox.addLayout(button_strip(self, 'Cancel', 'Go', 'GoBack', 'Select',
            'Start'), row, 0, 1, 3)

        row+= 1
        gbox.addLayout(exitbutton(self, self.exit), row, 0, 1, 3)

        self.setLayout(gbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        soort = {'studio': 'albums', 'live': 'concerten'}
        self.albumnaam = ('Worstenbroodje & Co - Overal en Nergens (Zultkop records,'
            ' het jaar 0)')
        self.heading.setText('Gegevens van {} {}'.format(
            soort[self.parent().albumtype], self.albumnaam))

    def new_data(self, keep_sel=False):
        self.albumnaam = ''
        self.album_names = []
        ## if self.parent().albumtype == 'studio':
            ## self.details = collections.OrderedDict((
                ## ('Label/jaar:', ''),
                ## ('Produced by:', ''),
                ## ('Credits:', ''),
                ## ('Bezetting:', ''),
                ## ('Tevens met:', '')))
        ## else:
            ## self.details = collections.OrderedDict((
                ## ('Produced by:', ''),
                ## ('Credits:', ''),
                ## ('Bezetting:', ''),
                ## ('Tevens met:', '')))
        self.tracknames = []
        self.recordings = []
        self.edit_det = True
        self.edit_trk = self.edit_rec = False

        if keep_sel:
            if self.parent().searchtype == 1:
                self.parent().artistid
            else:
                self.parent().search_arg

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

    def submit_and_back(self):
        self.submit()
        self.parent().do_detail()

    def exit(self, *args):
        """shutdown application"""
        self.parent().close()

class EditTracks(qtw.QWidget):
    """show list of tracks in editable form
    """
    def __init__(self, parent):

        super().__init__(parent)

    def create_widgets(self):
        """setup screen
        """
        vbox = qtw.QVBoxLayout()
        row = 0
        ## row += 1
        self.heading = qtw.QLabel('', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)

        row += 1
        vbox.addLayout(newline(self))
        ## self.tracknames = ['Morgen ben ik de bruid', 'Niemand de deur uit',
            ## 'Worstenbroodje en Uitknijpfruit', 'Sluitingstijd']
        self.trackwins = []

        frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        for trackname, trackindex in self.parent().albumdata['tracks']:
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>8}.'.format(trackindex), self))
            win = qtw.QLineEdit(trackname, self)
            win.setMaximumWidth(300)
            win.setMinimumWidth(300)
            self.trackwins.append(win)
            hbox.addWidget(win)
            ## hbox.addStretch()
            self.vbox2.addLayout(hbox)
        frm.setLayout(self.vbox2)
        scrl = qtw.QScrollArea()
        scrl.setWidget(frm)
        vbox.addWidget(scrl)

        hbox = qtw.QHBoxLayout()
        self.add_new = qtw.QPushButton('Nieuw track', self)
        self.add_new.clicked.connect(self.add_new_item)
        hbox.addWidget(self.add_new)
        hbox.addStretch()
        vbox.addLayout(hbox)

        ## vbox = qtw.QVBoxLayout()
        ## vbox.addStretch()
        ## gbox.addLayout(vbox, row, 0, 1, 3)

        vbox.addLayout(newline(self))
        vbox.addLayout(button_strip(self, 'Cancel', 'Go', 'GoBack', 'Select',
            'Start'))

        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        soort = {'studio': 'albums', 'live': 'concerten'}
        self.albumnaam = ('Worstenbroodje & Co - Overal en Nergens (Zultkop records,'
            ' het jaar 0)')
        self.heading.setText('Gegevens van {} {}'.format(
            soort[self.parent().albumtype], self.albumnaam))

    def add_new_item(self):
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('    ', self))
        win = qtw.QLineEdit(self)
        self.trackwins.append(win)
        hbox.addWidget(win)
        ## hbox.addStretch()
        self.vbox2.addLayout(hbox)


    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

    def submit_and_back(self):
        self.submit()
        self.parent().do_detail()

    def exit(self, *args):
        """shutdown application"""
        self.parent().close()

class EditRecordings(qtw.QWidget):
    """show list of recordings in editable form
    """
    def __init__(self, parent):

        super().__init__(parent)

    def create_widgets(self):
        """setup screen
        """
        vbox = qtw.QVBoxLayout()
        self.heading = qtw.QLabel('', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)

        vbox.addLayout(newline(self))

        ## self.recordings = ['CD: enkel', 'Vinyl: LP 2 van 2', 'Banshee Music Player']
        self.recwins = []

        frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        for opnindex, opname in enumerate(self.parent().albumdata['opnames']):
            opnsoort, opntext = opname
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>8}.'.format(opnindex + 1), self))
            win = qtw.QComboBox(self)
            win.addItem('--- Maak een selectie ---')
            win.addItems(RECTYPES)
            win.setCurrentIndex(RECTYPES.index(opnsoort) + 1)
            hbox.addWidget(win)

            win = qtw.QLineEdit(opntext, self)
            win.setMaximumWidth(200)
            win.setMinimumWidth(200)
            self.recwins.append(win)
            hbox.addWidget(win)
            hbox.addStretch()
            self.vbox2.addLayout(hbox)
        frm.setLayout(self.vbox2)
        scrl = qtw.QScrollArea()
        scrl.setWidget(frm)
        vbox.addWidget(scrl)

        hbox = qtw.QHBoxLayout()
        self.add_new = qtw.QPushButton('Nieuwe opname', self)
        self.add_new.clicked.connect(self.add_new_item)
        hbox.addWidget(self.add_new)
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addLayout(newline(self))

        vbox.addLayout(button_strip(self, 'Cancel', 'Go', 'GoBack', 'Select',
            'Start'))

        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        soort = {'studio': 'albums', 'live': 'concerten'}
        self.albumnaam = ('Worstenbroodje & Co - Overal en Nergens (Zultkop records,'
            ' het jaar 0)')
        self.heading.setText('Gegevens van {} {}'.format(
            soort[self.parent().albumtype], self.albumnaam))

    def add_new_item(self):
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('    ', self))
        win = qtw.QLineEdit(self)
        self.recwins.append(win)
        hbox.addWidget(win)
        ## hbox.addStretch()
        self.vbox2.addLayout(hbox)

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

    def submit_and_back(self):
        self.submit()
        self.parent().do_detail()

    def exit(self, *args):
        """shutdown application"""
        self.parent().close()

class Artists(qtw.QWidget):
    """show list of artists
    """
    def __init__(self, parent):
        super().__init__(parent)

    def create_widgets(self):
        """setup screen
        """
        vbox = qtw.QVBoxLayout()
        ## self.vbox2 = qtw.QVBoxLayout()
        self.heading = qtw.QLabel('Artiestenlijst', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)
        vbox.addLayout(newline(self))

        self.frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        for item in get_artist_list():
            hbox = qtw.QHBoxLayout()
            hbox.addWidget(qtw.QLabel('{:>3}.'.format(item['id']), self))
            win = qtw.QLineEdit(item["first_name"], self)
            hbox.addWidget(win)
            win = qtw.QLineEdit(item["last_name"], self)
            win.setMaximumWidth(300)
            win.setMinimumWidth(300)
            hbox.addWidget(win)
            self.vbox2.addLayout(hbox)
        self.frm.setLayout(self.vbox2)
        scrl = qtw.QScrollArea()
        scrl.setWidget(self.frm)
        vbox.addWidget(scrl)

        vbox.addLayout(button_strip(self, 'Edit', 'New', 'Start'))
        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        pass
        ## del self.vbox2
        ## self.vbox2 = qtw.QVBoxLayout()
        ## for item in get_artist_list():
            ## hbox = qtw.QHBoxLayout()
            ## hbox.addWidget(qtw.QLabel('{:>3}.'.format(item['id']), self))
            ## win = qtw.QLineEdit(item["first_name"], self)
            ## hbox.addWidget(win)
            ## win = qtw.QLineEdit(item["last_name"], self)
            ## win.setMaximumWidth(200)
            ## win.setMinimumWidth(200)
            ## hbox.addWidget(win)
            ## self.vbox2.addLayout(hbox)
        ## self.frm.setLayout(self.vbox2)

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

    def new(self):
        """open dialog to add new artist
        """
        if NewArtistDialog(self).exec_() == qtw.QDialog.Accepted:
            self.refresh_screen()

    def exit(self, *args):
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
        gbox.addWidget(qtw.QLabel('Names wil be shown sorted on last name'), 2, 0,
            1, 2)
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
        self.accept()

class MainFrame(qtw.QMainWindow):
    """Het idee hierachter is om bij elke schermwijziging
    het centralwidget opnieuw in te stellen
    """
    def __init__(self, parent):
        super().__init__()
        self.albumtype = ''
        self.searchtype = 1
        self.artistid = 0
        self.search_arg = ''
        self.sorttype = 1
        self.album_artists, self.album_names, self.album_ids = [], [], []
        self.albumid = 0
        self.albumdata = {}
        self.end = False
        self.move(300, 50)
        self.resize(400, 600)
        ## self.start = self.select = self.detail = self.artists = None
        ## self.edit_det = self.edit_trk = self.edit_rec = None
        self.windows = []

    def do_start(self):
        """show initial sceen
        """
        go = Start(self)
        self.windows.append(go)
        go.create_widgets()
        go.refresh_screen()
        ## go.show()
        self.setCentralWidget(go)

    def do_select(self):
        """show selection screen
        """
        if self.albumtype == 'artist':
            go = Artists(self)
        else:
            go = Select(self)
        self.windows.append(go)
        go.create_widgets()
        go.refresh_screen()
        ## go.show()
        self.setCentralWidget(go)

    def do_new(self, keep_sel=False):
        """show screen for adding a new album or artist
        """
        if self.albumtype == 'artist':
            if NewArtistDialog(self).exec_() == qtw.QDialog.Accepted:
                self.do_select()
        else:
            self.do_edit_alg(new=True, keep_sel=keep_sel)
            self.windows.append(go)

    def do_detail(self):
        """show albums details
        """
        if self.albumtype == 'artist':
            go = Artists(self)
        else:
            go = Detail(self)
        self.windows.append(go)
        go.create_widgets()
        ## go.select_data()
        go.refresh_screen()
        ## go.show()
        self.setCentralWidget(go)

    def do_edit_alg(self, new=False, keep_sel=False):
        """edit album details
        """
        go = EditDetails(self)
        self.windows.append(go)
        go.create_widgets()
        if new:
            go.new_data(keep_sel)
        ## go.select_data()
        go.refresh_screen()
        ## go.show()
        self.setCentralWidget(go)

    def do_edit_trk(self):
        """edit track list
        """
        go = EditTracks(self)
        self.windows.append(go)
        go.create_widgets()
        ## go.select_data()
        go.refresh_screen()
        ## go.show()
        self.setCentralWidget(go)

    def do_edit_rec(self):
        """edit recordings list
        """
        go = EditRecordings(self)
        self.windows.append(go)
        go.create_widgets()
        ## go.select_data()
        go.refresh_screen()
        ## go.show()
        self.setCentralWidget(go)

app = qtw.QApplication(sys.argv)
main = MainFrame(None)
main.show()
main.do_start()
sys.exit(app.exec_())

