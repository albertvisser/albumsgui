"""simple music database frontend
"""
import sys
import os.path
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
import banshee_settings as config
if 'albums' in config.databases:
    import albums_dml_sql as dmla
if 'banshee' in config.databases:
    import banshee_dml as dmlb
if 'clementine' in config.databases:
    import clementine_dml as dmlc
if 'CDDB' in config.databases:
    import cddb_dml as dmld


class MainWidget(qtw.QWidget):
    """User Interface
    """
    def __init__(self):
        super().__init__()
        self.dbnames = sorted([x for x in config.databases], key=lambda x: x.lower())
        self.dbnames.append('covers')
        self.dbname = ''
        self.album_name = self.artist_name = ''
        self.show_covers = False
        self.initializing = True
        self.create_widgets()
        self.tracks_list.setVisible(True)
        self.lbl.setVisible(False)
        self.initializing = False

    def create_widgets(self):
        """build screen elements
        """
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(qtw.QLabel('Database: ', self))
        self.ask_db = qtw.QComboBox(self)
        self.ask_db.addItems(self.dbnames)
        self.ask_db.currentIndexChanged.connect(self.change_db)
        hbox.addWidget(self.ask_db)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        self.ask_artist = qtw.QComboBox(self)
        self.ask_artist.setMinimumWidth(260)
        self.ask_artist.currentIndexChanged.connect(self.get_artist)
        hbox.addWidget(self.ask_artist)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        self.ask_album = qtw.QComboBox(self)
        self.ask_album.setMinimumWidth(260)
        self.ask_album.currentIndexChanged.connect(self.get_album)
        hbox.addWidget(self.ask_album)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        self.tracks_list = qtw.QListWidget(self)
        self.tracks_list.setMinimumWidth(280)
        self.tracks_list.addItems(("",
                                   "Kies een uitvoerende uit de bovenste lijst", "",
                                   "Daarna een album uit de lijst daaronder", "",
                                   "De tracks worden dan in dit venster getoond."))
        self.initial_list = True
        hbox.addWidget(self.tracks_list)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        self.lbl = qtw.QLabel(self)
        self.lbl.setMinimumWidth(500)
        self.lbl.setMinimumHeight(500)
        self.lbl.setText("\n".join(("Kies een uitvoerende uit de bovenste lijst", "",
                                    "Daarna een album uit de lijst daaronder", "",
                                    "De cover wordt dan in dit venster getoond.")))
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
        self.ask_db.setCurrentIndex(1)
        self.ask_artist.setFocus()

    def change_db(self, index):
        """prepare for querying the correct database
        """
        self.old_dbname = self.dbname
        self.dbname = self.dbnames[index]
        if self.dbname == 'covers':
            self.dbname = 'clementine'
            self.show_covers = True
        else:
            self.show_covers = False
        self.db = config.databases[self.dbname]
        if self.dbname == 'albums':
            data = dmla.list_artists(self.db)
            self.artist_names = [' '.join((x["first_name"], x['last_name'])).lstrip()
                                 for x in data]
            self.artist_ids = [x["id"] for x in data]
        elif self.dbname == 'banshee':
            data = dmlb.list_artists(self.db)
            self.artist_names = [x["Name"] for x in data]
            self.artist_ids = [x["ArtistID"] for x in data]
        elif self.dbname == 'clementine':
            data = dmlc.list_artists(self.db)
            self.artist_ids = self.artist_names = [x["artist"] for x in data]
        elif self.dbname == 'CDDB':
            self.db = dmld.CDDBData(self.db)
            self.artist_ids = self.artist_names = sorted(self.db.list_artists())
        self.initializing = True
        if self.dbname != self.old_dbname:
            self.ask_artist.clear()
            self.ask_artist.addItems([''] + self.artist_names)
            self.ask_album.clear()
        if self.show_covers:
            self.tracks_list.setVisible(False)
            self.lbl.setVisible(True)
            self.lbl.clear()
        else:
            self.tracks_list.setVisible(True)
            self.lbl.setVisible(False)
            self.tracks_list.clear()
        self.initializing = False
        if self.dbname == self.old_dbname:
            self.get_album(self.ask_album.currentIndex())

    def get_artist(self, index):
        """get the selected artist's ID and build a list of albums
        """
        if self.initializing:
            return
        if index == 0:
            pass
        elif self.dbname == 'albums':
            data = dmla.list_albums(self.db, self.artist_ids[index - 1])
            self.album_names = [x["name"] for x in data]
            self.album_ids = [x["id"] for x in data]
        elif self.dbname == 'banshee':
            data = dmlb.list_albums(self.db, self.artist_ids[index - 1])
            self.album_names = [x["Title"] for x in data]
            self.album_ids = [x["AlbumID"] for x in data]
        elif self.dbname == 'clementine':
            self.artist = self.artist_ids[index - 1]
            data = dmlc.list_albums(self.db, self.artist)
            self.album_ids = self.album_names = [x["album"] for x in data]
        elif self.dbname == 'CDDB':
            self.artist = self.artist_ids[index - 1]
            data = self.db.list_albums(self.artist)
            self.album_ids = [x[0] for x in data]
            self.album_names = [x[1] for x in data]
        self.artist_name = self.ask_artist.itemText(self.ask_artist.currentIndex())
        self.initializing = True
        self.ask_album.clear()
        self.ask_album.addItems([''] + self.album_names)
        self.initializing = False
        self.tracks_list.clear()

    def get_album(self, index):
        """get the selected album's ID and build a list of tracks
        """
        if self.initializing:
            return
        self.album_name = self.ask_album.itemText(self.ask_album.currentIndex())
        if self.show_covers:
            pic = gui.QPixmap()
            text, test, fname = '', False, ''
        if index == 0:
            if self.show_covers:
                text = 'ahem'
            else:
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
            if self.show_covers:
                data = dmlc.list_album_covers(self.db, self.artist,
                                              self.album_ids[index - 1])
                auto, manu = data[0]['art_automatic'], data[0]['art_manual']
                fname = manu or auto
                if fname == '(embedded)':
                    text = 'Picture is embedded'
                elif fname:
                    test = pic.load(fname)
            else:
                data = dmlc.list_tracks_for_album(self.db, self.artist,
                                                  self.album_ids[index - 1])
                self.trackids = self.tracknames = [x["title"] for x in data]
        elif self.dbname == 'CDDB':
            data = self.db.list_tracks(self.album_ids[index - 1])
            self.trackids, self.tracknames = [], []
            for x, y in enumerate(data):
                self.trackids.append(x)
                self.tracknames.append(y)
        if self.show_covers:
            if text:
                self.lbl.setText(text)
            elif test:
                self.lbl.setPixmap(pic)
            else:
                self.lbl.setText('Picture could not be loaded')
        else:
            self.tracks_list.clear()
            self.tracks_list.addItems(self.tracknames)

    def exit(self):
        """shutdown application
        """
        qtw.QMessageBox.information(self, "Exiting...", "Thank you for calling")
        self.close()


def main():
    """start application
    """
    app = qtw.QApplication(sys.argv)
    win = MainWidget()
    win.show()
    sys.exit(app.exec_())
