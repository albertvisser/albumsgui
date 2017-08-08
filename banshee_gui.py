"""simple music database frontend
"""
import sys
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
import albums_dml as dmla
import banshee_dml as dmlb
import clementine_dml as dmlc
import cddb_dml as dmld
import banshee_settings as config


class MainWidget(qtw.QWidget):
    """User Interface
    """

    def __init__(self):

        super().__init__()
        self.dbnames = sorted([x for x in config.databases], key=lambda x: x.lower())
        self.initializing = True
        self.create_widgets()
        self.initializing = False

    def create_widgets(self):
        """build screen elements
        """
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(qtw.QLabel('Database: ', self))
        self.ask_db = qtw.QComboBox(self)
        ## self.ask_db.setMinimumWidth(260)
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
                                   "Kies een uitvoerende uit de bovenste lijst",
                                   "",
                                   "Daarna een album uit de lijst daaronder",
                                   "",
                                   "De tracks worden dan in dit venster getoond."))
        self.initial_list = True
        hbox.addWidget(self.tracks_list)
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
        self.dbname = self.dbnames[index]
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
        self.ask_artist.clear()
        self.ask_artist.addItems([''] + self.artist_names)
        self.ask_album.clear()
        self.tracks_list.clear()
        self.initializing = False

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
        elif self.dbname == 'CDDB':
            data = self.db.list_tracks(self.album_ids[index - 1])
            self.trackids, self.tracknames = [], []
            for x, y in enumerate(data):
                self.trackids.append(x)
                self.tracknames.append(y)
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
