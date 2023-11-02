# testen van de conditionele imports kan misschien door banshee_gui niet meteen te importeren
# maar als onderdeel van een testfunctie nadat je een specifieke inhoud voor banshee_settings
# hebt klaargezet
# dat moet dan denkelijk in een ander testscript als de testmethodes voor MainWidget
import pytest
import types
import apps.banshee_gui as testee
import mockgui.mockqtwidgets as mockqtw
from unittests.buildscreen_output_fixture import expected_output


def test_mainwidget_init(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called Application.__init__')
    def mock_init(self, *args):
        print('called Widget.__init__')
    def mock_show(self, *args):
        print('called Widget.show')
    def mock_list_set(value):
        print(f'called tracklist.setVisible(`{value}`)')
    def mock_label_set(value):
        print(f'called label.setVisible(`{value}`)')
    def mock_create_widgets(self, *args):
        print('called Widget.create_widgets, self.initializing is', self.initializing)
        self.tracks_list = types.SimpleNamespace(setVisible=mock_list_set)
        self.lbl = types.SimpleNamespace(setVisible=mock_label_set)
    # monkeypatch.setattr(testee.qtw, 'QApplication', MockApplication)
    monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(testee.MainWidget, 'create_widgets', mock_create_widgets)
    # monkeypatch.setattr(testee.qtw, 'QWidget', MockWidget)
    monkeypatch.setattr(testee, 'config',
                        types.SimpleNamespace(databases=['x', 'clementine', 'banshee', 'strawberry']))
    testobj = testee.MainWidget()
    assert testobj.dbnames == ['banshee', 'clementine', 'strawberry', 'x', 'covers (banshee)',
                               'covers (clementine)', 'covers (strawberry)']
    assert testobj.dbname == ''
    assert testobj.album_name == ''
    assert testobj.artist_name == ''
    assert not testobj.show_covers
    assert not testobj.initializing
    assert capsys.readouterr().out == (
        'called Application.__init__\ncalled Widget.__init__\n'
        'called Widget.create_widgets, self.initializing is True\n'
        'called tracklist.setVisible(`True`)\ncalled label.setVisible(`False`)\n'
        'called Widget.show\n')


class MockMainWidget:
    def __init__(self):
        def mock_app_exec():
            return 'called Application.exec_'
        print('called MainWidget.__init__')
        self.app = types.SimpleNamespace(exec_=mock_app_exec)
    def setLayout(self, *args):
        print('called Widget.setLayout')
    def create_widgets(self):
        print('called widget.create_widgets, self.initializing is', self.initializing)


def test_mainwidget_go(monkeypatch, capsys):
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    with pytest.raises(SystemExit) as exc:
        testobj.go()
    assert str(exc.value) == 'called Application.exec_'


def test_mainwidget_create_widgets(monkeypatch, capsys, expected_output):
    def mock_init(self, *args):
        print('called Widget.__init__')
    def mock_setlayout(self, *args):
        print('called Widget.setLayout')
    def mock_show(self, *args):
        print('called Widget.show')
    def mock_count(self):
        print('called ComboBox.count')
        return 3
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(mockqtw.MockComboBox, 'count', mock_count)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.config, 'databases', ['albums', 'banshee', 'clementine', 'strawberry'])
    monkeypatch.setattr(testee.config, 'default_database', '2')
    testobj = testee.MainWidget()   # create widgets wordt hierin aangeroepen
    assert hasattr(testobj, 'ask_db')
    assert hasattr(testobj, 'ask_album')
    assert hasattr(testobj, 'ask_artist')
    assert hasattr(testobj, 'tracks_list')
    assert hasattr(testobj, 'lbl')
    bindings = {'testobj': testobj}
    assert capsys.readouterr().out == expected_output['bgui_create_widgets'].format(**bindings)


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
    testobj.ask_artist = mockqtw.MockComboBox()
    testobj.ask_album = mockqtw.MockComboBox()
    testobj.tracks_list = mockqtw.MockListBox()
    testobj.lbl = mockqtw.MockLabel()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called List.__init__\n'
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
            "called ComboBox.addItems with arg ['-- choose artist --', 'A', 'B']\n"
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg ['-- choose album --']\n"
            'called List.setVisible with arg `True`\n'
            'called Label.setVisible with arg `False`\n'
            'called List.clear\n'
            "called List.addItems with arg `("
            "'', 'Kies een uitvoerende uit de bovenste lijst',"
            " '', 'Daarna een album uit de lijst daaronder',"
            " '', 'De tracks worden dan in dit venster getoond.')`\n")
    testobj.dbname = 'y'
    testobj.change_db(2)
    assert capsys.readouterr().out == (
            'called MainWidget.get_artists_lists`\n'
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg ['-- choose artist --', 'A', 'B']\n"
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg ['-- choose album --']\n"
            'called List.setVisible with arg `False`\n'
            'called Label.setVisible with arg `True`\n'
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
    testobj.ask_artist = mockqtw.MockComboBox()
    testobj.ask_album = mockqtw.MockComboBox()
    testobj.tracks_list = mockqtw.MockListBox()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called List.__init__\n')
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
            "called ComboBox.itemText with value `1`\n"
            "called ComboBox.clear\n"
            "called ComboBox.addItems with arg ['-- choose album --']\n"
            "called List.clear\n")
    testobj.get_artist(1)
    assert testobj.album_ids == ['1', '2']
    assert testobj.album_names == ['A', 'B']
    assert capsys.readouterr().out == (
            "called MainWidget.get_albums_lists for `a`\n"
            "called ComboBox.currentIndex\n"
            "called ComboBox.itemText with value `1`\n"
            "called ComboBox.clear\n"
            "called ComboBox.addItems with arg ['-- choose album --', 'A', 'B']\n"
            "called List.clear\n")


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
    monkeypatch.setattr(testee.gui, 'QPixmap', mockqtw.MockPixmap)
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    testobj.ask_album = mockqtw.MockComboBox()
    testobj.tracks_list = mockqtw.MockListBox()
    testobj.lbl = mockqtw.MockLabel()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called List.__init__\n'
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
                                       "called ComboBox.itemText with value `1`\n"
                                       "called List.clear\n"
                                       "called Label.setText with arg ``\n")
    testobj.get_album(1)
    assert capsys.readouterr().out == ("called ComboBox.currentIndex\n"
                                       "called ComboBox.itemText with value `1`\n"
                                       "called MainWidget.get_tracks_lists for `q`, `a`\n"
                                       "called List.clear\n"
                                       "called List.addItems with arg `['A', 'B']`\n")
    testobj.show_covers = True
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText with value `1`\n'
                                       'called MainWidget.get_album_cover for `q`, `a`\n'
                                       'called Pixmap.__init__\n'
                                       'called Pixmap.load for `fname`\n'
                                       'called Pixmap.scaled to `500`, `500`\n'
                                       'called Label.setPixmap\n')
    monkeypatch.setattr(mockqtw.MockPixmap, 'load', lambda *x: None)
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText with value `1`\n'
                                       'called MainWidget.get_album_cover for `q`, `a`\n'
                                       'called Pixmap.__init__\n'
                                       'called Label.setText with arg'
                                       ' `Picture X could not be loaded`\n')
    monkeypatch.setattr(testee, 'DML', {
        'x': types.SimpleNamespace(get_tracks_lists=mock_tracks_lists,
                                   get_album_cover=lambda *x: '(embedded)')})
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText with value `1`\n'
                                       'called Label.setText with arg `Picture is embedded`\n')
    monkeypatch.setattr(testee, 'DML', {
        'x': types.SimpleNamespace(get_tracks_lists=mock_tracks_lists,
                                   get_album_cover=lambda *x: None)})
    testobj.get_album(1)
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.itemText with value `1`\n'
                                       'called Label.setText with arg'
                                       ' `No file associated with this album`\n')


def test_mainwidget_exit(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called Widget.__init__')
    def mock_info(self, *args):
        print('called messagebox.information with args', args)
    def mock_close(self, *args):
        print('called Widget.close')
    monkeypatch.setattr(testee.MainWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.MainWidget, 'close', mock_close)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called Widget.__init__\n'
    testobj.exit()
    assert capsys.readouterr().out == ("called messagebox.information with args ('Exiting...',"
                                       " 'Thank you for calling')\n"
                                       'called Widget.close\n')
