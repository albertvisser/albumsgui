"""unittests for ./apps/banshee_gui.py
"""
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
    """unittest for banshee_gui.MainWidget.init
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called Application.__init__')
    def mock_init(self, *args):
        """stub
        """
        print('called Widget.__init__')
    def mock_show(self, *args):
        """stub
        """
        print('called Widget.show')
    def mock_list_set(value):
        """stub
        """
        print(f'called tracklist.setVisible(`{value}`)')
    def mock_label_set(value):
        """stub
        """
        print(f'called label.setVisible(`{value}`)')
    def mock_create_widgets(self, *args):
        """stub
        """
        print('called Widget.create_widgets, self.initializing is', self.initializing)
        self.tracks_list = types.SimpleNamespace(setVisible=mock_list_set)
        self.lbl = types.SimpleNamespace(setVisible=mock_label_set)
    # monkeypatch.setattr(testee.qtw, 'QApplication', MockApplication)
    monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(testee.MainWidget, 'create_widgets', mock_create_widgets)
    # monkeypatch.setattr(testee.qtw, 'QWidget', MockWidget)
    monkeypatch.setattr(testee, 'config', types.SimpleNamespace(databases=['x', 'y', 'z']))
    testobj = testee.MainWidget()
    assert testobj.dbnames == ['x', 'y', 'z']
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
    """stub
    """
    def __init__(self):
        def mock_app_exec():
            """stub
            """
            return 'called Application.exec'
        print('called MainWidget.__init__')
        self.app = types.SimpleNamespace(exec=mock_app_exec)
    def setLayout(self, *args):
        """stub
        """
        print('called Widget.setLayout')
    def create_widgets(self):
        """stub
        """
        print('called widget.create_widgets, self.initializing is', self.initializing)


def test_mainwidget_init(monkeypatch, capsys):
    """unittest for banshee_gui.MainWidget__init__.
    """
    def mock_init(self, *args):
        """stub
        """
        print('called Widget.__init__')
    def mock_create(self, *args):
        """stub
        """
        print('called MainWidget.create_widgets')
        self.tracks_list = mockqtw.MockListBox()
        self.lbl = mockqtw.MockLabel()
    def mock_show(self, *args):
        """stub
        """
        print('called Widget.show')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.MainWidget, 'create_widgets', mock_create)
    monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(testee.config, 'databases', ['Yyy', 'xxx'])
    testobj = testee.MainWidget()
    assert testobj.dbnames == ['xxx', 'Yyy']
    assert testobj.dbname == ''
    assert testobj.album_name == ''
    assert testobj.artist_name == ''
    assert not testobj.show_covers
    assert not testobj.initializing
    assert capsys.readouterr().out == ("called Widget.__init__\n"
                                       "called MainWidget.create_widgets\n"
                                       "called List.__init__\n"
                                       "called Label.__init__\n"
                                       "called List.setVisible with arg `True`\n"
                                       "called Label.setVisible with arg `False`\n"
                                       "called Widget.show\n")


def test_mainwidget_init_2(monkeypatch, capsys):
    """unittest for banshee_gui.MainWidget__init__.
    """
    def mock_init(self, *args):
        """stub
        """
        print('called Widget.__init__')
    def mock_create(self, *args):
        """stub
        """
        print('called MainWidget.create_widgets')
        self.tracks_list = mockqtw.MockListBox()
        self.lbl = mockqtw.MockLabel()
    def mock_show(self, *args):
        """stub
        """
        print('called Widget.show')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.MainWidget, 'create_widgets', mock_create)
    monkeypatch.setattr(testee.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(testee.config, 'databases', ['albums', 'banshee', 'clementine', 'strawberry'])
    testobj = testee.MainWidget()
    assert testobj.dbnames == ['albums', 'banshee', 'clementine', 'strawberry', 'covers (banshee)',
                               'covers (clementine)', 'covers (strawberry)']
    assert testobj.dbname == ''
    assert testobj.album_name == ''
    assert testobj.artist_name == ''
    assert not testobj.show_covers
    assert not testobj.initializing
    assert capsys.readouterr().out == ("called Widget.__init__\n"
                                       "called MainWidget.create_widgets\n"
                                       "called List.__init__\n"
                                       "called Label.__init__\n"
                                       "called List.setVisible with arg `True`\n"
                                       "called Label.setVisible with arg `False`\n"
                                       "called Widget.show\n")



def test_mainwidget_go(monkeypatch, capsys):
    """unittest for banshee_gui.MainWidget.go
    """
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    with pytest.raises(SystemExit) as exc:
        testobj.go()
    assert str(exc.value) == 'called Application.exec'


def test_mainwidget_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for banshee_gui.MainWidget.create_widgets
    """
    def mock_setlayout(self, *args):
        """stub
        """
        print('called Widget.setLayout')
    def mock_count(self):
        """stub
        """
        print('called ComboBox.count')
        return 3
    def mock_count_2(self):
        """stub
        """
        print('called ComboBox.count')
        return 0
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(mockqtw.MockComboBox, 'count', mock_count)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.config, 'default_database', '2')
    monkeypatch.setattr(testee.MainWidget, '__init__', MockMainWidget.__init__)
    testobj = testee.MainWidget()
    assert capsys.readouterr().out == 'called MainWidget.__init__\n'
    testobj.dbnames = ['xxx', 'yyy']
    testobj.setLayout = mock_setlayout
    testobj.create_widgets()
    assert isinstance(testobj.ask_db, testee.qtw.QComboBox)
    assert isinstance(testobj.ask_album, testee.qtw.QComboBox)
    assert isinstance(testobj.ask_artist, testee.qtw.QComboBox)
    assert isinstance(testobj.tracks_list, testee.qtw.QListWidget)
    assert isinstance(testobj.lbl, testee.qtw.QLabel)
    bindings = {'testobj': testobj}
    assert capsys.readouterr().out == expected_output['bgui_create_widgets'].format(**bindings)

    # toevoeging t.b.v. full branch coverage
    monkeypatch.setattr(mockqtw.MockComboBox, 'count', mock_count_2)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    testobj.create_widgets()
    assert isinstance(testobj.ask_db, testee.qtw.QComboBox)
    assert isinstance(testobj.ask_album, testee.qtw.QComboBox)
    assert isinstance(testobj.ask_artist, testee.qtw.QComboBox)
    assert isinstance(testobj.tracks_list, testee.qtw.QListWidget)
    assert isinstance(testobj.lbl, testee.qtw.QLabel)
    bindings = {'testobj': testobj}
    assert capsys.readouterr().out == expected_output['bgui_create_widgets2'].format(**bindings)


def test_mainwidget_change_db(monkeypatch, capsys):
    """unittest for banshee_gui.MainWidget.change_db
    """
    def mock_artists_lists():
        """stub
        """
        print('called MainWidget.get_artists_lists`')
        return ['1', '2'], ['A', 'B']
    def mock_get_album(self, arg):
        """stub
        """
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
    """unittest for banshee_gui.MainWidget.get_artist
    """
    def mock_albums_lists(artist):
        """stub
        """
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
    """unittest for banshee_gui.MainWidget.get_album
    """
    def mock_tracks_lists(artist, album):
        """stub
        """
        print(f'called MainWidget.get_tracks_lists for `{artist}`, `{album}`')
        return ['1', '2'], ['A', 'B']
    def mock_album_cover(artist, album):
        """stub
        """
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
                                       'called Pixmap.load with arg `X`\n'
                                       'called Pixmap.scaled with args `500`, `500`\n'
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
    """unittest for banshee_gui.MainWidget.exit
    """
    def mock_init(self, *args):
        """stub
        """
        print('called Widget.__init__')
    def mock_info(self, *args):
        """stub
        """
        print('called messagebox.information with args', args)
    def mock_close(self, *args):
        """stub
        """
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
