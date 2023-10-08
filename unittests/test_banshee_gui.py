# testen van de conditionele imports kan misschien door banshee_gui niet meteen te importeren
# maar als onderdeel van een testfunctie nadat je een specifieke inhoud voor banshee_settings
# hebt klaargezet
# dat moet dan denkelijk in een ander testscript als de testmethodes voor MainWidget
import pytest
import types
import apps.banshee_gui as testee

class MockApplication:  # (qtw.QApplication):
    def __init__(self, *args):
        print('called application.__init__')
    def exec_(self):
        print('called app.exec_')

class MockControl:
    def setVisible(self, value):
        print(f'called control.setVisible with args `{type(self)}`, `{value}`')

class MockWidget: # (qtw.QWidget):
    def __init__(self, *args):
        print('called widget.__init__')
        self.tracks_list = MockControl()
        self.lbl = MockControl()
    def create_widgets(self):
        print('called widget.create_widgets, self.initializing is', self.initializing)
    def show(self):
        print('called widget.show')

class MockVBox:
    def __init__(self):
        print('called VBoxLayout.__init__')
    def addWidget(self, *args):
        print('called VBoxLayout.addWidget')
    def addLayout(self, *args):
        print('called VBoxLayout.addLayout')
class MockHBox:
    def __init__(self):
        print('called HBoxLayout.__init__')
    def addWidget(self, *args):
        print('called HBoxLayout.addWidget')
    def addLayout(self, *args):
        print('called HBoxLayout.addLayout')
    def addStretch(self, *args):
        print('called HBoxLayout.addStretch')
class MockGrid:
    def __init__(self):
        print('called GridLayout.__init__')
    def addWidget(self, *args):
        print('called GridLayout.addWidget')
    def addLayout(self, *args):
        print('called GridLayout.addLayout')
class MockComboBox:
    def mock_connect(*args):
        print('called connect with args', args)
    currentIndexChanged = types.SimpleNamespace(connect=mock_connect)
    def __init__(self, *args):
        print('called ComboBox.__init__')
    def setMinimumWidth(self, number):
        print(f'called ComboBox.setMinimumWidth to `{number}`')
    def setCurrentIndex(self, number):
        print(f'called ComboBox.setCurrentIndex to `{number}`')
    def currentIndex(self):
        print('called ComboBox.currentIndex')
        return 1
    def setFocus(self):
        print('called ComboBox.setFocus')
    def clear(self):
        print('called ComboBox.clear')
    def addItems(self, itemlist):
        print(f'called ComboBox.addItems with arg `{itemlist}`')
    def count(self):
        print('called ComboBox.count')
        return 3
    def itemText(self, number):
        print(f'called ComboBox.itemText for `{number}`')
        return str(number)
class MockListBox:
    def __init__(self, *args):
        print('called ListWidget.__init__')
    def setVisible(self, value):
        print(f'called ListWidget.setVisible to `{value}`')
    def setMinimumWidth(self, number):
        print(f'called ListWidget.setMinimumWidth to `{number}`')
    def setMinimumHeight(self, number):
        print(f'called ListWidget.setMinimumHeight to `{number}`')
    def clear(self):
        print('called ListWidget.clear')
    def addItems(self, itemlist):
        print(f'called ListWidget.addItems with arg `{itemlist}`')
class MockLabel:
    def __init__(self, *args):
        print('called Label.__init__')
    def setVisible(self, value):
        print(f'called Label.setVisible to `{value}`')
    def setMinimumWidth(self, number):
        print(f'called Label.setMinimumWidth to `{number}`')
    def setMinimumHeight(self, number):
        print(f'called Label.setMinimumHeight to `{number}`')
    def setText(self, text):
        print(f'called Label.setText with arg `{text}`')
    def setPixmap(self, data):
        print(f'called Label.setPixmap')
class MockButton:
    def mock_connect(*args):
        print('called connect with args', args)
    clicked = types.SimpleNamespace(connect=mock_connect)
    def __init__(self, *args):
        print('called PushButton.__init__')
class MockPixmap:
    def __init__(self, *args):
        print('called Pixmap.__init__')
    def load(self, fname):
        print(f'called Pixmap.load for `fname`')
        return 'ok'
    def scaled(self, x, y):
        print(f'called Pixmap.scaled to `{x}`, `{y}`')
        return 'ok'


def test_mainwidget_init(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called QApplication.__init__')
    def mock_init(self, *args):
        print('called QWidget.__init__')
    def mock_show(self, *args):
        print('called QWidget.show')
    def mock_list_set(value):
        print(f'called tracklist.setVisible(`{value}`)')
    def mock_label_set(value):
        print(f'called label.setVisible(`{value}`)')
    def mock_create_widgets(self, *args):
        print('called QWidget.create_widgets, self.initializing is', self.initializing)
        self.tracks_list = types.SimpleNamespace(setVisible=mock_list_set)
        self.lbl = types.SimpleNamespace(setVisible=mock_label_set)
    # monkeypatch.setattr(testee.qtw, 'QApplication', MockApplication)
    monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(testee.MainWidget, 'create_widgets', mock_create_widgets)
    # monkeypatch.setattr(testee.qtw, 'QWidget', MockWidget)
    monkeypatch.setattr(testee, 'config', types.SimpleNamespace(databases=['x', 'clementine',
                                                                           'banshee', 'strawberry']))
    testobj = testee.MainWidget()
    assert testobj.dbnames == ['banshee', 'clementine', 'strawberry', 'x', 'covers (banshee)',
                               'covers (clementine)', 'covers (strawberry)']
    assert testobj.dbname == ''
    assert testobj.album_name == ''
    assert testobj.artist_name == ''
    assert not testobj.show_covers
    assert not testobj.initializing
    assert capsys.readouterr().out == (
        'called QApplication.__init__\ncalled QWidget.__init__\n'
        'called QWidget.create_widgets, self.initializing is True\n'
        'called tracklist.setVisible(`True`)\ncalled label.setVisible(`False`)\n'
        'called QWidget.show\n')


class MockMainWidget:
    def __init__(self):
        def mock_app_exec():
            return 'called QApplication.exec_'
        print('called MainWidget.__init__')
        self.app = types.SimpleNamespace(exec_=mock_app_exec)
    def setLayout(self, *args):
        print('called QWidget.setLayout')


def test_mainwidget_go(monkeypatch, capsys):
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    with pytest.raises(SystemExit) as exc:
        testobj.go()
    assert str(exc.value) == 'called QApplication.exec_'


def test_mainwidget_create_widgets(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called QWidget.__init__')
    def mock_setlayout(self, *args):
        print('called QWidget.setLayout')
    def mock_show(self, *args):
        print('called QWidget.show')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', MockVBox)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', MockHBox)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', MockGrid)
    monkeypatch.setattr(testee.qtw, 'QComboBox', MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QListWidget', MockListBox)
    monkeypatch.setattr(testee.qtw, 'QLabel', MockLabel)
    monkeypatch.setattr(testee.qtw, 'QPushButton', MockButton)
    monkeypatch.setattr(testee.config, 'databases', ['albums', 'banshee', 'clementine', 'strawberry'])
    monkeypatch.setattr(testee.config, 'default_database', '2')
    testobj = testee.MainWidget()   # create widgets wordt hierin aangeroepen
    assert hasattr(testobj, 'ask_db')
    assert hasattr(testobj, 'ask_album')
    assert hasattr(testobj, 'ask_artist')
    assert hasattr(testobj, 'tracks_list')
    assert hasattr(testobj, 'lbl')
    assert capsys.readouterr().out == (
        'called QWidget.__init__\n'
        'called VBoxLayout.__init__\n'
        'called GridLayout.__init__\n'
        'called Label.__init__\n'
        'called GridLayout.addWidget\n'
        'called HBoxLayout.__init__\n'
        'called ComboBox.__init__\n'
        "called ComboBox.addItems with arg `['albums', 'banshee', 'clementine', 'strawberry',"
        " 'covers (banshee)', 'covers (clementine)', 'covers (strawberry)']`\n"
        f'called connect with args ({testobj.change_db},)\n'
        'called HBoxLayout.addWidget\n'
        'called HBoxLayout.addStretch\n'
        'called GridLayout.addLayout\n'
        'called Label.__init__\n'
        'called GridLayout.addWidget\n'
        'called ComboBox.__init__\n'
        'called ComboBox.setMinimumWidth to `260`\n'
        f'called connect with args ({testobj.get_artist},)\n'
        'called GridLayout.addWidget\n'
        'called Label.__init__\n'
        'called GridLayout.addWidget\n'
        'called ComboBox.__init__\n'
        'called ComboBox.setMinimumWidth to `260`\n'
        f'called connect with args ({testobj.get_album},)\n'
        'called GridLayout.addWidget\n'
        'called VBoxLayout.addLayout\n'
        'called HBoxLayout.__init__\n'
        'called HBoxLayout.addStretch\n'
        'called ListWidget.__init__\n'
        'called ListWidget.setMinimumWidth to `400`\n'
        'called ListWidget.setMinimumHeight to `300`\n'
        'called HBoxLayout.addWidget\n'
        'called HBoxLayout.addStretch\n'
        'called VBoxLayout.addLayout\n'
        'called HBoxLayout.__init__\n'
        'called HBoxLayout.addStretch\n'
        'called Label.__init__\n'
        'called Label.setMinimumWidth to `500`\n'
        'called Label.setMinimumHeight to `500`\n'
        'called HBoxLayout.addWidget\n'
        'called HBoxLayout.addStretch\n'
        'called VBoxLayout.addLayout\n'
        'called HBoxLayout.__init__\n'
        'called HBoxLayout.addStretch\n'
        'called PushButton.__init__\n'
        f'called connect with args ({testobj.exit},)\n'
        'called HBoxLayout.addWidget\n'
        'called HBoxLayout.addStretch\n'
        'called VBoxLayout.addLayout\n'
        'called QWidget.setLayout\n'
        'called ComboBox.count\n'
        'called ComboBox.itemText for `0`\n'
        'called ComboBox.itemText for `1`\n'
        'called ComboBox.itemText for `2`\n'
        'called ComboBox.setCurrentIndex to `2`\n'
        'called ComboBox.setFocus\n'
        'called ListWidget.setVisible to `True`\n'
        'called Label.setVisible to `False`\n'
        'called QWidget.show\n')


def test_mainwidget_change_db(monkeypatch, capsys):
    def mock_artists_lists():
        print('called MainWidget.get_artists_lists`')
        return ['1', '2'], ['A', 'B']
    def mock_get_album(self, arg):
        print(f'called MainWidget.get_album with arg `{arg}`')
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    monkeypatch.setattr(testee.MainWidget, 'get_album', mock_get_album)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    testobj.ask_artist = MockComboBox()
    testobj.ask_album = MockComboBox()
    testobj.tracks_list = MockListBox()
    testobj.lbl = MockLabel()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ListWidget.__init__\n'
                                       'called Label.__init__\n')
    testobj.dbnames = ['x', 'y', 'covers (x)']
    monkeypatch.setattr(testee.config, 'databases', {'x': 'dbx', 'y': 'dby'})
    mock_dml = types.SimpleNamespace(get_artists_lists=mock_artists_lists)
    monkeypatch.setattr(testee, 'DML', {'x': mock_dml, 'y': mock_dml})
    testobj.dbname = 'x'
    testobj.change_db(0)
    assert testobj.dbname == 'x'
    assert not testobj.show_covers
    assert testobj.db == 'dbx'
    assert testobj.artist_ids == ['1', '2']
    assert capsys.readouterr().out == ('called MainWidget.get_artists_lists`\n'
                                       'called ComboBox.currentIndex\n'
                                       'called MainWidget.get_album with arg `1`\n')
    testobj.dbname = 'x'
    testobj.change_db(1)
    assert capsys.readouterr().out == (
            'called MainWidget.get_artists_lists`\n'
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg `['-- choose artist --', 'A', 'B']`\n"
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg `['-- choose album --']`\n"
            'called ListWidget.setVisible to `True`\n'
            'called Label.setVisible to `False`\n'
            'called ListWidget.clear\n'
            "called ListWidget.addItems with arg `("
            "'', 'Kies een uitvoerende uit de bovenste lijst',"
            " '', 'Daarna een album uit de lijst daaronder',"
            " '', 'De tracks worden dan in dit venster getoond.')`\n")
    testobj.dbname = 'y'
    testobj.change_db(2)
    assert capsys.readouterr().out == (
            'called MainWidget.get_artists_lists`\n'
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg `['-- choose artist --', 'A', 'B']`\n"
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg `['-- choose album --']`\n"
            'called ListWidget.setVisible to `False`\n'
            'called Label.setVisible to `True`\n'
            "called Label.setText with arg `\n"
            "Kies een uitvoerende uit de bovenste lijst\n\n"
            "Daarna een album uit de lijst daaronder\n\n"
            "De cover wordt dan in dit venster getoond.`\n")


def test_mainwidget_get_artist(monkeypatch, capsys):
    def mock_albums_lists(artist):
        print(f'called MainWidget.get_albums_lists for `{artist}`')
        return ['1', '2'], ['A', 'B']
    monkeypatch.setattr(testee, 'DML', {'x':
                                        types.SimpleNamespace(get_albums_lists=mock_albums_lists)})
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    testobj.ask_artist = MockComboBox()
    testobj.ask_album = MockComboBox()
    testobj.tracks_list = MockListBox()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ListWidget.__init__\n')
    testobj.initializing = True
    testobj.dbname = 'x'
    testobj.artist_ids = ['a', 'b']
    testobj.get_artist(0)
    assert capsys.readouterr().out == ''
    testobj.initializing = False
    testobj.album_ids, testobj.album_names = [], []
    testobj.get_artist(0)
    assert capsys.readouterr().out == (
            "called ComboBox.currentIndex\n"
            "called ComboBox.itemText for `1`\n"
            "called ComboBox.clear\n"
            "called ComboBox.addItems with arg `['-- choose album --']`\n"
            "called ListWidget.clear\n")
    testobj.get_artist(1)
    assert testobj.album_ids == ['1', '2']
    assert testobj.album_names == ['A', 'B']
    assert capsys.readouterr().out == (
            "called MainWidget.get_albums_lists for `a`\n"
            "called ComboBox.currentIndex\n"
            "called ComboBox.itemText for `1`\n"
            "called ComboBox.clear\n"
            "called ComboBox.addItems with arg `['-- choose album --', 'A', 'B']`\n"
            "called ListWidget.clear\n")


def test_mainwidget_get_album(monkeypatch, capsys):
    def mock_tracks_lists(artist, album):
        print(f'called MainWidget.get_tracks_lists for `{artist}`, `{album}`')
        return ['1', '2'], ['A', 'B']
    def mock_album_cover(artist, album):
        print(f'called MainWidget.get_album_cover for `{artist}`, `{album}`')
        return 'X'
    monkeypatch.setattr(testee, 'DML', {
        'x': types.SimpleNamespace(get_tracks_lists=mock_tracks_lists,
                                   get_album_cover=mock_album_cover)})
    monkeypatch.setattr(testee.gui, 'QPixmap', MockPixmap)
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    testobj.ask_album = MockComboBox()
    testobj.tracks_list = MockListBox()
    testobj.lbl = MockLabel()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ListWidget.__init__\n'
                                       'called Label.__init__\n')
    testobj.initializing = True
    testobj.artist = 'q'
    testobj.dbname = 'x'
    testobj.album_ids = ['a', 'b']
    testobj.get_album(2)
    testobj.initializing = False
    assert capsys.readouterr().out == ''
    testobj.show_covers = False
    testobj.get_album(0)
    assert capsys.readouterr().out == ("called ComboBox.currentIndex\n"
                                       "called ComboBox.itemText for `1`\n"
                                       "called ListWidget.clear\n"
                                       "called Label.setText with arg ``\n")
    testobj.get_album(1)
    assert capsys.readouterr().out == ("called ComboBox.currentIndex\n"
                                       "called ComboBox.itemText for `1`\n"
                                       "called MainWidget.get_tracks_lists for `q`, `a`\n"
                                       "called ListWidget.clear\n"
                                       "called ListWidget.addItems with arg `['A', 'B']`\n")
    testobj.show_covers = True
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText for `1`\n'
                                       'called MainWidget.get_album_cover for `q`, `a`\n'
                                       'called Pixmap.__init__\n'
                                       'called Pixmap.load for `fname`\n'
                                       'called Pixmap.scaled to `500`, `500`\n'
                                       'called Label.setPixmap\n')
    monkeypatch.setattr(MockPixmap, 'load', lambda *x: None)
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText for `1`\n'
                                       'called MainWidget.get_album_cover for `q`, `a`\n'
                                       'called Pixmap.__init__\n'
                                       'called Label.setText with arg'
                                       ' `Picture X could not be loaded`\n')
    monkeypatch.setattr(testee, 'DML', {
        'x': types.SimpleNamespace(get_tracks_lists=mock_tracks_lists,
                                   get_album_cover=lambda *x: '(embedded)')})
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText for `1`\n'
                                       'called Label.setText with arg `Picture is embedded`\n')
    monkeypatch.setattr(testee, 'DML', {
        'x': types.SimpleNamespace(get_tracks_lists=mock_tracks_lists,
                                   get_album_cover=lambda *x: None)})
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText for `1`\n'
                                       'called Label.setText with arg'
                                       ' `No file associated with this album`\n')


def test_mainwidget_exit(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called QWidget.__init__')
    def mock_info(self, *args):
        print('called messagebox.information with args', args)
    def mock_close(self, *args):
        print('called QWidget.close')
    monkeypatch.setattr(testee.MainWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.MainWidget, 'close', mock_close)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called QWidget.__init__\n'
    testobj.exit()
    assert capsys.readouterr().out == ("called messagebox.information with args ('Exiting...',"
                                       " 'Thank you for calling')\n"
                                       'called QWidget.close\n')
