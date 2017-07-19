"""PyQT version of albums webapp
"""
import sys


import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
import albums_dml as dmla
TYPETXT = {'studio': 'album', 'live': 'concert'}
SELTXT = {'studio': ['Niet zoeken, alles tonen',
                     'Zoek op Uitvoerende',
                     'Zoek op tekst in titel',
                     'Zoek op tekst in producer',
                     'Zoek op tekst in credits',
                     'Zoek op tekst in bezetting'],
          'live': ['Niet zoeken, alles tonen',
                   'Zoek op Uitvoerende',
                   'Zoek op tekst in locatie',
                   'Zoek op tekst in datum',
                   'Zoek op tekst in bezetting']}
SELCOL = {'studio': ['', 'artist', 'titel', 'producer', 'credits', 'bezetting'],
          'live': ['', 'artist', 'locatie', 'datum', 'bezetting']}
SORTTXT = {'studio': ['Niet sorteren', 'Uitvoerende', 'Titel', 'Jaar'],
           'live': ['Niet sorteren', 'Uitvoerende', 'Locatie', 'Datum']}
SORTCOL = {'studio': ['', 'artist', 'titel', 'jaar'],
           'live': ['', 'artist', 'locatie', 'datum']}
RECTYPES = ('Cassette',
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
    return dmla.list_artists(dmla.DB)


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
    data = dmla.list_albums_by_artist(dmla.DB, albumtype, search_for, sort_on)
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
    data = dmla.list_albums_by_search(dmla.DB, albumtype, search_type, search_for,
                                      sort_on)
    album_names = [x["name"] for x in data]
    album_ids = [x["id"] for x in data]
    album_artists = [' '.join((x["first_name"], x["last_name"])).lstrip()
                     for x in data]
    return album_artists, album_names, album_ids


def get_album(album_id, albumtype):
    """get the selected album's data
    """
    test = dmla.list_album_details(dmla.DB, album_id)
    data = test[0] if test else {}
    result = {'titel': data.get('name', ''),
              'artist': ' '.join((data.get('first_name', ''),
                                  data.get('last_name', ''))).strip()}
    text = data.get('label', '')
    if data.get('release_year', ''):
        if text:
            text += ', '
        text += str(data['release_year'])
    result['details'] = [('Label/jaar:', text),
                         ('Produced by:', data.get('produced_by', '')),
                         ('Credits:', data.get('credits', '')),
                         ('Bezetting:', data.get('bezetting', '')),
                         ('Tevens met:', data.get('additional', ''))]
    if albumtype == 'live':
        result['details'].pop(0)
    if data:
        result['tracks'] = [(x["volgnr"], x["name"], x["written_by"], x["credits"])
                            for x in dmla.list_tracks(dmla.DB, album_id)]
        result['opnames'] = [(x["type"], x["oms"])
                             for x in dmla.list_recordings(dmla.DB, album_id)]
    else:
        result['tracks'], result['opnames'] = [], []
    return result


def build_heading(win):
    """Generate heading text for screen
    """
    if not win.parent().albumdata['artist'] or not win.parent().albumdata['titel']:
        text = 'Opvoeren nieuw {}'.format(TYPETXT[win.parent().albumtype])
    else:
        text = 'Gegevens van {} {} - {}'.format(TYPETXT[win.parent().albumtype],
                                                win.parent().albumdata['artist'],
                                                win.parent().albumdata['titel'])
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
        gbox.addLayout(exitbutton(self, self.exit), row, 0, 1, 3)

        self.setLayout(gbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.ask_studio_artist.addItems(self.parent().names)
        self.ask_live_artist.addItems(self.parent().names)
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
            chosen = self.parent().ids.index(self.parent().artistid)
            widgets[1].setCurrentIndex(chosen + 1)
        if self.parent().searchtype < 2:
            widgets[2].clear()
        else:
            widgets[2].setText(self.parent().search_arg)
        widgets[3].setCurrentText(self.parent().sorttype)

    def select_album(self):
        "get selection type and argument for studio album"
        # -> selectiescherm
        self.parent().searchtype = self.ask_studio_search.currentIndex()
        self.parent().sorttype = self.ask_studio_sort.currentText()
        chosen = self.ask_studio_artist.currentIndex()
        self.parent().artistid = self.parent().ids[chosen - 1]
        self.parent().search_arg = self.studio_zoektekst.text()
        if self.parent().searchtype == 1:
            self.parent().search_arg = self.parent().artistid
        self.parent().albumtype = 'studio'
        self.parent().do_select()

    def new_album(self):
        "add a studio album to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.parent().albumtype = 'studio'
        self.parent().do_new()

    def select_concert(self):
        "get selection type and argument for live concert"
        # -> selectiescherm
        self.parent().searchtype = self.ask_live_search.currentIndex()
        self.parent().sorttype = self.ask_live_sort.currentText()
        chosen = self.ask_live_artist.currentIndex()
        self.parent().artistid = self.parent().ids[chosen - 1]
        self.parent().search_arg = self.live_zoektekst.text()
        if self.parent().searchtype == 1:
            self.parent().search_arg = self.parent().artistid
        self.parent().albumtype = 'live'
        self.parent().do_select()

    def new_concert(self):
        "add a live concert to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.parent().albumtype = 'live'
        self.parent().do_new()

    def view_artists(self):
        "go to artists screen"
        # -> "selectie"scherm in wijzig modus
        self.parent().albumtype = 'artist'
        self.parent().do_select()

    def new_artist(self):
        "add an artist to the collection"
        # -> direct naar detailscherm in wijzig modus
        self.parent().albumtype = 'artist'
        self.parent().do_new()

    def exit(self):
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

        labeltxt = 'naar een soortgelijke selectie voor '
        if self.parent().searchtype:
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
            labeltxt = 'of ' + labeltxt

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltxt, self))
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
        self.add_new = qtw.QPushButton('voer een nieuw item op bij deze selectie', self)
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
            self.parent().search_arg = self.parent().ids[chosen - 1]
            if self.parent().searchtype == 1:
                self.parent().artistid = self.parent().search_arg
            self.parent().do_select()

    def other_albumtype(self):
        """determine other type of selection and change accordingly, also change
        self.parent().albumtype
        """
        if self.parent().albumtype == 'studio':
            self.parent().albumtype = 'live'
        else:
            self.parent().albumtype = 'studio'
        self.parent().do_select()

    def todetail(self):
        """determine which button was clicked and change accordingly
        """
        for ix, btn in enumerate(self.go_buttons):
            if self.sender() == btn:
                self.parent().albumid = self.parent().album_ids[ix]
                break
        self.parent().do_detail()

    def add_new_to_sel(self, *args, **kwargs):
        """TODO
        """
        self.parent().do_new(keep_sel=True)

    def exit(self):
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
        self.ask_album.addItems(self.parent().album_names)
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
        for trackindex, trackname, author, cred in self.parent().albumdata['tracks']:
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
        self.heading.setText(build_heading(self))
        self.quickchange.setText('Snel naar een ander {} in deze selectie:'.format(
            TYPETXT[self.parent().albumtype]))
        self.subheading.setText("{}gegevens:".format(
            TYPETXT[self.parent().albumtype].title()))

    def other_album(self):
        """Determine which other album to show and do so
        """
        test = self.ask_album.currentIndex()
        if test:
            self.parent().albumid = self.parent().album_ids[test - 1]
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
    def __init__(self, parent):

        super().__init__(parent)

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

        data = [('Uitvoerende:', self.parent().albumdata['artist']),
                ['Albumtitel:', self.parent().albumdata['titel']]]
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
                if text:
                    win.setCurrentIndex(listdata.index(text) + 1)
                ## win.setMaximumWidth(200)
                ## win.setMinimumWidth(200)
            elif caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
                win = qtw.QTextEdit(text, self)
            else:
                win = qtw.QLineEdit(text, self)
            gbox.addWidget(win, row, 1, 1, 2)

        row += 1
        vbox = qtw.QVBoxLayout()
        vbox.addStretch()
        gbox.addLayout(vbox, row, 0, 1, 3)

        row += 1
        buttons = ['Cancel', 'Go', 'GoBack', 'Select', 'Start']
        if not self.parent().albumid:
            buttons.remove('Cancel')
            if not self.parent().search_arg:
                buttons.remove('Select')
        gbox.addLayout(button_strip(self, *buttons), row, 0, 1, 3)

        row += 1
        gbox.addLayout(exitbutton(self, self.exit), row, 0, 1, 3)

        self.setLayout(gbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        self.heading.setText(build_heading(self))

    def new_data(self, keep_sel=False):
        """Prepare to show empty screen for entering new album
        """
        self.albumnaam = ''
        self.album_names = []
        self.tracknames = []
        self.recordings = []
        self.edit_det = True
        self.edit_trk = self.edit_rec = False

        if keep_sel:  # what was this about again?
            if self.parent().searchtype == 1:
                self.parent().artistid
            else:
                self.parent().search_arg

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

    def submit_and_back(self):
        """return to previous (details) screen after completion
        """
        self.submit()
        self.parent().do_detail()

    def exit(self):
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
        self.heading = qtw.QLabel('', self)
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
        for trackindex, trackname, author, text in self.parent().albumdata['tracks']:
            self.add_track_fields(trackindex, trackname, author, text)

        self.tracks = int(trackindex)
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
        vbox.addLayout(button_strip(self, 'Cancel', 'Go', 'GoBack', 'Select',
                                    'Start'))

        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def add_track_fields(self, trackindex, trackname='', author='', text=''):
        """Build line in edit area with track data (or not)
        """
        line = self.line + 1
        self.gbox.addWidget(qtw.QLabel('{:>8}.'.format(trackindex), self), line, 0)
        hbox = qtw.QHBoxLayout()
        win = qtw.QLineEdit(trackname, self)
        win.setMaximumWidth(300)
        win.setMinimumWidth(300)
        hbox.addWidget(win)
        win = qtw.QLineEdit(author, self)
        win.setMaximumWidth(200)
        win.setMinimumWidth(200)
        hbox.addWidget(win)
        self.gbox.addLayout(hbox, line, 1)
        line += 1
        win = qtw.QTextEdit(text, self)
        win.setMaximumWidth(508)
        win.setMinimumWidth(508)
        win.setMaximumHeight(38)
        win.setMinimumHeight(38)
        self.gbox.addWidget(win, line, 1)
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
        ## oldfrm = self.scrl.takeWidget()
        ## frm = qtw.QFrame(self)
        ## frm.setLayout(self.gbox)
        ## self.scrl.setWidget(frm)
        ## self.scrl.ensureVisible(0, frm.sizeHint().height())
        ## del oldfrm
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 68)
        vbar.setValue(vbar.maximum())

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

    def submit_and_back(self):
        """return to details screen after completion
        """
        self.submit()
        self.parent().do_detail()

    def exit(self):
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

        self.recwins = []

        frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        self.vbox2.addStretch()
        for opnindex, opname in enumerate(self.parent().albumdata['opnames']):
            self.add_rec_fields(opnindex, opname)

        self.recs = opnindex
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

        vbox.addLayout(button_strip(self, 'Cancel', 'Go', 'GoBack', 'Select',
                                    'Start'))

        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def add_rec_fields(self, opnindex, opname=None):
        """Build line in edit area with recording data (or not)"""
        if opname is None:
            opname = ['', '']
        opnsoort, opntext = opname
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('{:>8}.'.format(opnindex + 1), self))
        win = qtw.QComboBox(self)
        win.addItem('--- Maak een selectie ---')
        win.addItems(RECTYPES)
        try:
            win.setCurrentIndex(RECTYPES.index(opnsoort) + 1)
        except:
            pass
        hbox.addWidget(win)

        win = qtw.QLineEdit(opntext, self)
        win.setMaximumWidth(200)
        win.setMinimumWidth(200)
        self.recwins.append(win)
        hbox.addWidget(win)
        hbox.addStretch()
        self.vbox2.insertLayout(self.vbox2.count() - 1, hbox)

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

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

    def submit_and_back(self):
        """Return to details screen after completion
        """
        self.submit()
        self.parent().do_detail()

    def exit(self):
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
        self.heading = qtw.QLabel('Artiestenlijst', self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.heading)
        vbox.addLayout(hbox)
        vbox.addLayout(newline(self))

        self.frm = qtw.QFrame(self)
        self.vbox2 = qtw.QVBoxLayout()
        ## hbox2 = qtw.QHBoxLayout()
        ## lbl = qtw.QLabel('First name / prefix', self)
        ## lbl.setMaximumWidth(80)
        ## lbl.setMinimumWidth(80)
        ## hbox2.addWidget(lbl)
        ## hbox2.addWidget(qtw.QLabel('Last name / to be sorted on)', self))
        ## self.vbox2.addLayout(hbox2)
        self.last_artistid = 0
        for item in get_artist_list():
            test = item['id']
            if test > self.last_artistid:
                self.last_artistid = test
            self.add_artist_line(test, item["first_name"], item["last_name"])
        self.frm.setLayout(self.vbox2)
        self.scrl = qtw.QScrollArea()
        self.scrl.setWidget(self.frm)
        self.scrl.setWidgetResizable(True)
        vbox.addWidget(self.scrl)

        vbox.addLayout(button_strip(self, 'Edit', 'New', 'Start'))
        vbox.addLayout(exitbutton(self, self.exit))

        self.setLayout(vbox)

    def add_artist_line(self, itemid, first_name='', last_name=''):
        """Create line in edit area with artist data (or not)
        """
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('{:>3}.'.format(itemid), self))
        win = qtw.QLineEdit(first_name, self)
        hbox.addWidget(win)
        win = qtw.QLineEdit(last_name, self)
        win.setMaximumWidth(300)
        win.setMinimumWidth(300)
        hbox.addWidget(win)
        self.vbox2.addLayout(hbox)

    def refresh_screen(self):
        """bring screen up-to-date
        """
        pass

    def submit(self):
        """neem de waarden van de invulvelden over en geef ze door aan de database
        """

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
        self.accept()


class MainFrame(qtw.QMainWindow):
    """Het idee hierachter is om bij elke schermwijziging
    het centralwidget opnieuw in te stellen
    """
    def __init__(self, parent=None):
        app = qtw.QApplication(sys.argv)
        super().__init__()
        self.albumtype = ''
        self.searchtype = 1
        self.artistid = 0
        self.search_arg = ''
        self.sorttype = ''
        self.names, self.ids = get_all_artists()
        self.album_artists, self.album_names, self.album_ids = [], [], []
        self.albumid = 0
        self.albumdata = {}
        self.end = False
        self.move(300, 50)
        self.resize(400, 600)
        self.windows = []
        self.show()
        self.do_start()
        sys.exit(app.exec_())

    def do_start(self):
        """show initial sceen
        """
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
                self.album_artists = []
                self.album_names, self.album_ids = get_albums_by_artist(
                    self.albumtype, self.artistid, self.sorttype)
            else:
                self.album_artists, self.album_names, self.album_ids = get_albums_by_text(
                    self.albumtype, self.searchtype, self.search_arg, self.sorttype)
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
                self.names, self.ids = get_all_artists()
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
            self.albumdata = get_album(self.albumid, self.albumtype)
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

if __name__ == '__main__':
    main = MainFrame(None)
