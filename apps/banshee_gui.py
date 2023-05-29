"""simple music database frontend
"""
import sys
# import os.path
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
import apps.banshee_settings as config
if 'albums' in config.databases:
    import apps.albums_dml_sql as dmla
if 'banshee' in config.databases:
    import apps.banshee_dml as dmlb
if 'clementine' in config.databases:
    import apps.clementine_dml as dmlc
if 'strawberry' in config.databases:
    import apps.strawberry_dml as dmls
if 'CDDB' in config.databases:
    import apps.cddb_dml as dmld


class MainWidget(qtw.QWidget):
    """User Interface
    """
    initial_tracks = ("", "Kies een uitvoerende uit de bovenste lijst",
                      "", "Daarna een album uit de lijst daaronder",
                      "", "De tracks worden dan in dit venster getoond.")
    initial_cover_text = "\n".join(initial_tracks).replace("tracks", "cover").replace("worden",
                                                                                      "wordt")

    def __init__(self):
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.dbnames = sorted(list(config.databases), key=lambda x: x.lower())
        for name in ('banshee', 'clementine', 'strawberry'):
            if name in self.dbnames:
                self.dbnames.append(f'covers ({name})')
        self.dbname = ''
        self.album_name = self.artist_name = ''
        self.show_covers = False
        self.initializing = True
        self.create_widgets()
        self.tracks_list.setVisible(True)
        self.lbl.setVisible(False)
        self.initializing = False
        self.show()

    def go(self):
        "start the event loop"
        sys.exit(self.app.exec_())

    def create_widgets(self):
        """build screen elements
        """
        vbox = qtw.QVBoxLayout()

        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel('Database: ', self), 0, 0)
        hbox = qtw.QHBoxLayout()
        self.ask_db = qtw.QComboBox(self)
        self.ask_db.addItems(self.dbnames)
        self.ask_db.currentIndexChanged.connect(self.change_db)
        hbox.addWidget(self.ask_db)
        hbox.addStretch()
        gbox.addLayout(hbox, 0, 1)

        gbox.addWidget(qtw.QLabel('Artist: ', self), 1, 0)
        self.ask_artist = qtw.QComboBox(self)
        self.ask_artist.setMinimumWidth(260)
        self.ask_artist.currentIndexChanged.connect(self.get_artist)
        gbox.addWidget(self.ask_artist, 1, 1)

        gbox.addWidget(qtw.QLabel('Album: ', self), 2, 0)
        self.ask_album = qtw.QComboBox(self)
        self.ask_album.setMinimumWidth(260)
        self.ask_album.currentIndexChanged.connect(self.get_album)
        gbox.addWidget(self.ask_album, 2, 1)
        vbox.addLayout(gbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        self.tracks_list = qtw.QListWidget(self)
        self.tracks_list.setMinimumWidth(400)
        self.tracks_list.setMinimumHeight(300)
        self.initial_list = True
        hbox.addWidget(self.tracks_list)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        self.lbl = qtw.QLabel(self)
        self.lbl.setMinimumWidth(500)
        self.lbl.setMinimumHeight(500)
        hbox.addWidget(self.lbl)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        quit_button = qtw.QPushButton("E&xit", self)
        quit_button.clicked.connect(self.exit)
        hbox.addWidget(quit_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.ask_db.setCurrentIndex(3)
        self.ask_artist.setFocus()

    def change_db(self, index):
        """prepare for querying the correct database
        """
        self.old_dbname = self.dbname
        self.dbname = self.dbnames[index]
        if self.dbname.startswith('covers'):
            self.dbname = self.dbname.replace('covers (', '').replace(')', '')
            self.show_covers = True
        else:
            self.show_covers = False
        self.db = config.databases[self.dbname]
        self.artist_ids, self.artist_names = self.get_artist_lists(self.dbname)
        self.initializing = True
        if self.dbname != self.old_dbname:
            self.ask_artist.clear()
            self.ask_artist.addItems(['-- choose artist --'] + self.artist_names)
            self.ask_album.clear()
            self.ask_album.addItems(['-- choose album --'])
        if self.show_covers:
            self.tracks_list.setVisible(False)
            self.lbl.setVisible(True)
            self.lbl.setText(self.initial_cover_text)
        else:
            self.tracks_list.setVisible(True)
            self.lbl.setVisible(False)
            self.tracks_list.clear()
            self.tracks_list.addItems(self.initial_tracks)
        if self.dbname == self.old_dbname:
            self.get_album(self.ask_album.currentIndex())
        self.initializing = False

    def get_artist_lists(self, dbname):
        "actually get artist data depending on data backend"
        if dbname == 'albums':
            data = dmla.list_artists(self.db)
            return ([x["id"] for x in data],
                    [' '.join((x["first_name"], x['last_name'])).lstrip() for x in data])
        if dbname == 'banshee':
            data = dmlb.list_artists(self.db)
            return ([x["ArtistID"] for x in data], [x["Name"] for x in data])
        if dbname == 'clementine':
            data = [x["artist"] for x in dmlc.list_artists(self.db)]
        elif dbname == 'strawberry':
            data = [x["artist"] for x in dmls.list_artists(self.db)]
        elif dbname == 'CDDB':
            data = sorted(dmld.CDDBData(self.db).list_artists())
        else:
            data = []
        return data, data

    def get_artist(self, index):
        """get the selected artist's ID and build a list of albums
        """
        if self.initializing:
            return
        if index == 0:
            pass
        else:
            self.artist = self.artist_ids[index - 1]
            self.album_ids, self.album_names = self.get_albums_lists(self.dbname)
        self.artist_name = self.ask_artist.itemText(self.ask_artist.currentIndex())
        self.initializing = True
        self.ask_album.clear()
        self.ask_album.addItems([''] + self.album_names)
        self.initializing = False
        self.tracks_list.clear()

    def get_albums_lists(self, dbname):
        "actually get album data depending on data backend"
        if dbname == 'albums':
            data = dmla.list_albums(self.db, self.artist)
            return ([x["id"] for x in data], [x["name"] for x in data])
        if dbname == 'banshee':
            data = dmlb.list_albums(self.db, self.artist)
            return ([x["AlbumID"] for x in data], [x["Title"] for x in data])
        if dbname == 'clementine':
            data = [x["album"] for x in dmlc.list_albums(self.db, self.artist)]
            return data, data
        if dbname == 'strawberry':
            data = [x["album"] for x in dmls.list_albums(self.db, self.artist)]
            return data, data
        if dbname == 'CDDB':
            data = self.db.list_albums(self.artist)
            return [x[0] for x in data], [x[1] for x in data]
        return [], []

    def get_album(self, index):
        """get the selected album's ID and build a list of tracks
        """
        if self.initializing:
            return
        self.album_name = self.ask_album.itemText(self.ask_album.currentIndex())
        self.album = self.album_ids[index - 1]
        if index == 0:
            self.tracks_list.clear()
            self.lbl.setText('')
        elif self.show_covers:  # (self.dbnames):
            text, fname, pic = self.get_cover(self.dbname)
            if text:
                self.lbl.setText(text)
            elif pic:
                self.lbl.setPixmap(pic)
            else:
                self.lbl.setText(f'Picture {fname} could not be loaded')
        else:
            self.trackids, self.tracknames = self.get_track_lists(self.dbname)
            self.tracks_list.clear()
            self.tracks_list.addItems(self.tracknames)

    def get_cover(self, dbname):
        "actually get cover data depending on data backend"
        text, fname, test = '', '', False
        if dbname == 'banshee':
            return "Feature still to be implemented", '', None
        if dbname == 'clementine':
            data = dmlc.list_album_covers(self.db, self.artist, self.album)
        elif dbname == 'strawberry':
            data = dmls.list_album_covers(self.db, self.artist, self.album)
        fname = data[0]['art_manual'] or data[0]['art_automatic']
        if fname == '(embedded)':
            text = 'Picture is embedded'
        elif fname:
            pic = gui.QPixmap()
            test = pic.load(fname.replace('///', '/').replace('%20', ' '))
            if test:
                test = pic.scaled(500, 500)
        return text, fname, test

    def get_track_lists(self, dbname):
        "actually get track data depending on data backend"
        if dbname == 'albums':
            data = dmla.list_tracks(self.db, self.album)
            return [x["volgnr"] for x in data], [x["name"] for x in data]
        if dbname == 'banshee':
            data = dmlb.list_tracks(self.db, self.album)
            return [x["TrackNumber"] for x in data], [x["Title"] for x in data]
        if dbname == 'clementine':
            data = [x["title"] for x in dmlc.list_tracks_for_album(self.db, self.artist, self.album)]
            return data, data
        if dbname == 'strawberry':
            data = [x["title"] for x in dmls.list_tracks_for_album(self.db, self.artist, self.album)]
            return data, data
        if dbname == 'CDDB':
            data = self.db.list_tracks(self.album)
            trackids, tracknames = [], []
            for x, y in enumerate(data):
                trackids.append(x)
                tracknames.append(y)
            return trackids, tracknames
        return [], []

    def exit(self):
        """shutdown application
        """
        qtw.QMessageBox.information(self, "Exiting...", "Thank you for calling")
        self.close()
