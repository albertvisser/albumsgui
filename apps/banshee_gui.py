"""simple music database frontend
"""
import sys
# import os.path
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
## import PyQt5.QtCore as core
import apps.banshee_settings as config
DML = {}
if 'albums' in config.databases:
    # import apps.albums_dml_sql as dmla
    import apps.albums_dml as dmla
    DML['albums'] = dmla
if 'banshee' in config.databases:
    import apps.banshee_dml as dmlb
    DML['banshee'] = dmlb
if 'clementine' in config.databases:
    import apps.clementine_dml as dmlc
    DML['clementine'] = dmlc
if 'strawberry' in config.databases:
    import apps.strawberry_dml as dmls
    DML['strawberry'] = dmls
if 'CDDB' in config.databases:
    import apps.cddb_dml as dmld
    DML['CDDB'] = dmld


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
        sys.exit(self.app.exec())

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
        for index in range(self.ask_db.count()):
            if self.ask_db.itemText(index) == config.default_database:
                self.ask_db.setCurrentIndex(index)
                break
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
        self.artist_ids, self.artist_names = DML[self.dbname].get_artists_lists()
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
        else:
            self.get_album(self.ask_album.currentIndex())
        self.initializing = False

    def get_artist(self, index):
        """get the selected artist's ID and build a list of albums
        """
        if self.initializing:
            return
        if index == 0:
            pass
        else:
            self.artist = self.artist_ids[index - 1]
            self.album_ids, self.album_names = DML[self.dbname].get_albums_lists(self.artist)
        self.artist_name = self.ask_artist.itemText(self.ask_artist.currentIndex())
        self.initializing = True
        self.ask_album.clear()
        self.ask_album.addItems(['-- choose album --'] + self.album_names)
        self.initializing = False
        self.tracks_list.clear()

    def get_album(self, index):
        """get the selected album's ID and build a list of tracks or the album cover
        """
        if self.initializing:
            return
        self.album_name = self.ask_album.itemText(self.ask_album.currentIndex())
        self.album = self.album_ids[index - 1]
        if index == 0:
            self.tracks_list.clear()
            self.lbl.setText('')
        elif self.show_covers:  # (self.dbnames):
            text = ''
            fname = DML[self.dbname].get_album_cover(self.artist, self.album)
            if fname == '(embedded)':
                text = 'Picture is embedded'
            elif fname:
                pic = gui.QPixmap()
                test = pic.load(fname.replace('///', '/').replace('%20', ' '))
                if test:
                    test = pic.scaled(500, 500)
                else:
                    text = f'Picture {fname} could not be loaded'
            else:
                text = "No file associated with this album"
            if text:
                self.lbl.setText(text)
            else:
                self.lbl.setPixmap(pic)
        else:
            self.trackids, self.tracknames = DML[self.dbname].get_tracks_lists(self.artist,
                                                                               self.album)
            self.tracks_list.clear()
            self.tracks_list.addItems(self.tracknames)

    def exit(self):
        """shutdown application
        """
        qtw.QMessageBox.information(self, "Exiting...", "Thank you for calling")
        self.close()
