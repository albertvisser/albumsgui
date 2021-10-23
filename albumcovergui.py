"""simple music database frontend
"""
import sys
import os.path
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
# import banshee_dml as dmlb
import clementine_dml as dmlc
import banshee_settings as config


class MainWidget(qtw.QWidget):
    """User Interface
    """

    def __init__(self):

        super().__init__()
        self.dbnames = ['banshee', 'clementine']
        self.album_name = self.artist_name = ''
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
        self.lbl = qtw.QLabel(self)
        self.lbl.setMinimumWidth(500)
        self.lbl.setMinimumHeight(500)
        self.lbl.setText("\n".join(("Kies een uitvoerende uit de bovenste lijst",
                                    "",
                                    "Daarna een album uit de lijst daaronder",
                                    "",
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

        ter makkelijker vergelijking: onthou de artst en album selecties en stel ze
        opnieuw in
        """
        self.dbname = self.dbnames[index]
        print(self.dbname)
        self.db = config.databases[self.dbname]
        if self.dbname == 'banshee':
            data = dmlb.list_artists(self.db)
            self.artist_names = [x["Name"] for x in data]
            self.artist_ids = [x["ArtistID"] for x in data]
        elif self.dbname == 'clementine':
            data = dmlc.list_artists(self.db)
            self.artist_ids = self.artist_names = [x["artist"] for x in data]
        self.initializing = True
        self.ask_artist.clear()
        self.ask_artist.addItems([''] + self.artist_names)
        self.ask_album.clear()
        self.initializing = False

    def get_artist(self, index):
        """get the selected artist's ID and build a list of albums
        """
        if self.initializing:
            return
        if index == 0:
            pass
        elif self.dbname == 'banshee':
            data = dmlb.list_albums(self.db, self.artist_ids[index - 1])
            self.album_names = [x["Title"] for x in data]
            self.album_ids = [x["AlbumID"] for x in data]
        elif self.dbname == 'clementine':
            self.artist = self.artist_ids[index - 1]
            data = dmlc.list_albums(self.db, self.artist)
            self.album_ids = self.album_names = [x["album"] for x in data]
        self.artist_name = self.ask_artist.itemText(self.ask_artist.currentIndex())
        self.initializing = True
        self.ask_album.clear()
        self.ask_album.addItems([''] + self.album_names)
        self.initializing = False

    def get_album(self, index):
        """get the selected album's ID and put up the cover
        """
        if self.initializing:
            return
        self.album_name = self.ask_album.itemText(self.ask_album.currentIndex())
        print('getting album cover')
        pic = gui.QPixmap()
        text, test, fname = '', False, ''
        if index == 0:
            text = 'ahem'
        elif self.dbname == 'banshee':
            print(self.album_ids[index - 1])
            data = dmlb.list_album_covers(self.db, 0, self.album_ids[index - 1])
            print(data)
            for sub in ('', '300', 'xxx', '36', '64', '90'):
                fname = os.path.join('/home/albert/.cache/media-art',
                                     sub,
                                     data[0]['ArtworkID'])
                if pic.load(fname):
                    test = True
                    break
        elif self.dbname == 'clementine':
            data = dmlc.list_album_covers(self.db, self.artist,
                                          self.album_ids[index - 1])
            print(data)
            auto, manu = data[0]['art_automatic'], data[0]['art_manual']
            fname = manu or auto
            if fname == '(embedded)':
                text = 'Picture is embedded'
            elif fname:
                test = pic.load(fname)
        if text:
            self.lbl.setText(text)
        elif test:
            self.lbl.setPixmap(pic)
        else:
            self.lbl.setText('Picture could not be loaded')

    def exit(self):
        """shutdown application
        """
        self.close()


def main():
    """start application
    """
    app = qtw.QApplication(sys.argv)
    win = MainWidget()
    win.show()
    sys.exit(app.exec_())
