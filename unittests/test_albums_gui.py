import types
import pytest
import apps.albums_gui as testee
import unittests.mockqtwidgets as mockqtw
from buildscreen_output_fixture import expected_output


def test_get_artist_list(monkeypatch):
    monkeypatch.setattr(testee.dmla, 'list_artists', lambda: ['x', 'y'])
    assert testee.get_artist_list() == ['x', 'y']


def test_get_albums_by_artist(monkeypatch, capsys):
    def mock_list(*args):
        print('called dmla.list_albums_by_artist with args', args)
        return ['x', 'y', 'z']
    monkeypatch.setattr(testee.dmla, 'list_albums_by_artist', mock_list)
    assert testee.get_albums_by_artist('albumtype', 'search_for', 'sort_on') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_artist with args'
                                       " ('albumtype', 'search_for', 'sort_on')\n")


def test_get_albums_by_text(monkeypatch, capsys):
    def mock_list(*args):
        print('called dmla.list_albums_by_search with args', args)
        return ['x', 'y', 'z']
    monkeypatch.setattr(testee.dmla, 'list_albums_by_search', mock_list)
    assert testee.get_albums_by_text('studio', 0, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('studio', '*', 'a', 'b')\n")
    assert testee.get_albums_by_text('studio', 2, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('studio', 'name', 'a', 'b')\n")
    assert testee.get_albums_by_text('studio', 3, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('studio', 'produced_by', 'a', 'b')\n")
    assert testee.get_albums_by_text('studio', 4, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('studio', 'credits', 'a', 'b')\n")
    assert testee.get_albums_by_text('studio', 5, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('studio', 'bezetting', 'a', 'b')\n")
    assert testee.get_albums_by_text('live', 0, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('live', '*', 'a', 'b')\n")
    assert testee.get_albums_by_text('live', 2, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('live', 'name', 'a', 'b')\n")
    assert testee.get_albums_by_text('live', 3, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('live', 'name', 'a', 'b')\n")
    assert testee.get_albums_by_text('live', 4, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('live', 'produced_by', 'a', 'b')\n")
    assert testee.get_albums_by_text('live', 5, 'a', 'b') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_search with args'
                                       " ('live', 'bezetting', 'a', 'b')\n")


def test_get_album(monkeypatch, capsys):
    myact = testee.dmla.my.Act()
    def mock_list(id_):
        print(f'called dmla.list_album_details with arg `{id_}`')
        return types.SimpleNamespace(name='x', artist=myact, label='y', release_year='z',
                                     produced_by='a', credits='b', bezetting='c', additional='d')
    def mock_get_name(id_):
        print(f'called artist.get_name with arg `{id_}`')
        return 'name'
    def mock_list_tracks(id_):
        print(f'called dmla.list_album_tracks with arg `{id_}`')
        return [types.SimpleNamespace(volgnr=1, name='e', written_by='f', credits='g')]
    def mock_list_recordings(id_):
        print(f'called dmla.list_album_recordings with arg `{id_}`')
        return [types.SimpleNamespace(type='h', oms='i')]
    monkeypatch.setattr(testee.dmla, 'list_album_details', mock_list)
    monkeypatch.setattr(testee.dmla.my.Act, 'get_name', mock_get_name)
    monkeypatch.setattr(testee.dmla, 'list_tracks', mock_list_tracks)
    monkeypatch.setattr(testee.dmla, 'list_recordings', mock_list_recordings)
    # default data terugkrijgen kan niet want je kunt alleen maar id's kiezen die ook bestaan
    assert testee.get_album(0, 'studio') == {'titel': '', 'artist': '', 'artist_name': '',
                                          'details': [('Label/jaar:', ''), ('Produced by:', ''),
                                                      ('Credits:', ''), ('Bezetting:', ''),
                                                      ('Tevens met:', '')],
                                          'tracks': {}, 'opnames': []}
    assert capsys.readouterr().out == ''
    assert testee.get_album(9, 'studio') == {'titel': 'x', 'artist': myact, 'artist_name': 'name',
                                             'details': [('Label/jaar:', 'y, z'),
                                                         ('Produced by:', 'a'), ('Credits:', 'b'),
                                                         ('Bezetting:', 'c'), ('Tevens met:', 'd')],
                                             'tracks': {1: ('e', 'f', 'g')}, 'opnames': [('h', 'i')]}
    assert capsys.readouterr().out == ('called dmla.list_album_details with arg `9`\n'
                                       'called artist.get_name with arg ``\n'
                                       'called dmla.list_album_tracks with arg `9`\n'
                                       'called dmla.list_album_recordings with arg `9`\n')
    assert testee.get_album(9, 'live') == {'titel': 'x', 'artist': myact, 'artist_name': 'name',
                                             'details': [('Produced by:', 'a'), ('Credits:', 'b'),
                                                         ('Bezetting:', 'c'), ('Tevens met:', 'd')],
                                             'tracks': {1: ('e', 'f', 'g')}, 'opnames': [('h', 'i')]}
    assert capsys.readouterr().out == ('called dmla.list_album_details with arg `9`\n'
                                       'called artist.get_name with arg ``\n'
                                       'called dmla.list_album_tracks with arg `9`\n'
                                       'called dmla.list_album_recordings with arg `9`\n')


def test_build_heading_new_1(monkeypatch, capsys):
    def mock_parent():
        return types.SimpleNamespace(albumtype='x', albumdata={'artist': '', 'titel': 'b'})
    def mock_text():
        return 'x'
    monkeypatch.setattr(testee, 'TYPETXT', {'x': 'dinges'})
    win = types.SimpleNamespace(parent=mock_parent, heading=types.SimpleNamespace(text=mock_text))
    assert testee.build_heading(win) == "Opvoeren nieuw dinges"

def test_build_heading_new_2(monkeypatch, capsys):
    def mock_parent():
        return types.SimpleNamespace(albumtype='x', albumdata={'artist': 'a', 'titel': ''})
    def mock_text():
        return 'x'
    monkeypatch.setattr(testee, 'TYPETXT', {'x': 'dinges'})
    win = types.SimpleNamespace(parent=mock_parent, heading=types.SimpleNamespace(text=mock_text))
    assert testee.build_heading(win) == "Opvoeren nieuw dinges"

def test_build_heading(monkeypatch, capsys):
    def mock_parent():
        return types.SimpleNamespace(albumtype='x', albumdata={'artist': 'a', 'titel': 'b'})
    counter = 0
    def mock_text():
        nonlocal counter
        counter += 1
        return ['', 'x', 'tracks', 'opnames', '*tracks', '*opnames'][counter]
    monkeypatch.setattr(testee, 'TYPETXT', {'x': 'dinges'})
    win = types.SimpleNamespace(parent=mock_parent, heading=types.SimpleNamespace(text=mock_text))
    assert testee.build_heading(win) == 'Wijzigen gegevens van dinges a - b'
    assert testee.build_heading(win, readonly=True) == 'Gegevens van dinges a - b: tracks'
    assert testee.build_heading(win, readonly=True) == 'Gegevens van dinges a - b: opnames'
    assert testee.build_heading(win, readonly=True) == 'Gegevens van dinges a - b: tracks'
    assert testee.build_heading(win, readonly=True) == 'Gegevens van dinges a - b: opnames'


def test_newline(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    assert isinstance(testee.newline('parent'), mockqtw.MockHBox)
    assert capsys.readouterr().out == ('called HBoxLayout.__init__\n'
                                       'called Frame.__init__\n'
                                       'called Frame.setFrameShape with arg `---`\n'
                                       'called HBoxLayout.addWidget with arg of type'
                                       " <class 'unittests.mockqtwidgets.MockFrame'>\n")


class MockParent:  # evt. vervangen door MockMainFrame (en die dan aanvullen)
    def do_select(self):
        ...
    def do_start(self):
        ...
    def do_detail(self):
        ...

class MockHandler:
    _parent = MockParent()
    def parent(self):
        return self._parent
    def submit(self):
        ...
    def submit_and_back(self):
        ...
    def new(self):
        ...
    def do_select(self):
        ...
    def do_start(self):
        ...


def test_button_strip(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    assert isinstance(testee.button_strip(MockHandler()), mockqtw.MockHBox)
    assert capsys.readouterr().out == ('called HBoxLayout.__init__\n'
                                       'called HBoxLayout.addStretch\n'
                                       'called HBoxLayout.addStretch\n')
    buttons = ['Cancel', 'Go', 'GoBack', 'Edit', 'New', 'Select', 'Start']
    handler = MockHandler()
    assert isinstance(testee.button_strip(handler, *buttons), mockqtw.MockHBox)
    assert capsys.readouterr().out == (
            'called HBoxLayout.__init__\n'
            'called HBoxLayout.addStretch\n'
            f"called PushButton.__init__ with args ('Afbreken', {handler})\n"
            f"called connect with args ({handler.parent().do_detail},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            f"called PushButton.__init__ with args ('Uitvoeren', {handler})\n"
            f"called connect with args ({handler.submit},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            f"called PushButton.__init__ with args ('Uitvoeren en terug', {handler})\n"
            f"called connect with args ({handler.submit_and_back},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            f"called PushButton.__init__ with args ('Wijzigingen doorvoeren', {handler})\n"
            f"called connect with args ({handler.submit},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            f"called PushButton.__init__ with args ('Nieuwe opvoeren', {handler})\n"
            f"called connect with args ({handler.new},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            f"called PushButton.__init__ with args ('Terug naar Selectie', {handler})\n"
            f"called connect with args ({handler.parent().do_select},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            f"called PushButton.__init__ with args ('Terug naar Startscherm', {handler})\n"
            f"called connect with args ({handler.parent().do_start},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            'called HBoxLayout.addStretch\n')


def test_exitbutton(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    handler = MockHandler()
    assert isinstance(testee.exitbutton(handler, handler.submit), mockqtw.MockHBox)
    assert capsys.readouterr().out == (
            'called HBoxLayout.__init__\n'
            'called HBoxLayout.addStretch\n'
            f"called PushButton.__init__ with args ('E&xit', {handler})\n"
            f"called connect with args ({handler.submit},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            'called HBoxLayout.addStretch\n')
    assert isinstance(testee.exitbutton(handler, handler.submit, extrawidget='extra'),
                      mockqtw.MockHBox)
    assert capsys.readouterr().out == (
            'called HBoxLayout.__init__\n'
            'called HBoxLayout.addStretch\n'
            "called HBoxLayout.addWidget with arg of type <class 'str'>\n"
            f"called PushButton.__init__ with args ('E&xit', {handler})\n"
            f"called connect with args ({handler.submit},)\n"
            "called HBoxLayout.addWidget with arg of type"
            " <class 'unittests.mockqtwidgets.MockButton'>\n"
            'called HBoxLayout.addStretch\n')


class MockMainFrame:
    def __init__(self):
        print('called MainFrame.__init__')
        self.app = mockqtw.MockApplication()
    def go(self):
        print('called MainFrame.go')
    def do_start(self):
        print('called MainFrame.do_start')

class MockStart:
    def __init__(self, parent):
        print(f'called Start.__init__ with arg `{parent}`')
    def create_widgets(self):
        print('called Start.create_widgets')
    def refresh_screen(self):
        print('called Start.refresh_screen')

class MockSelect:
    def __init__(self, parent):
        print(f'called Select.__init__ with arg `{parent}`')
    def create_widgets(self):
        print('called Select.create_widgets')
    def refresh_screen(self):
        print('called Select.refresh_screen')

class MockDetail:
    def __init__(self, parent):
        print(f'called Detail.__init__ with arg `{parent}`')
    def create_widgets(self):
        print('called Detail.create_widgets')
    def refresh_screen(self):
        print('called Detail.refresh_screen')

class MockEditDetails:
    def __init__(self, parent):
        print(f'called EditDetails.__init__ with arg `{parent}`')
    def create_widgets(self):
        print('called EditDetails.create_widgets')
    def new_data(self, arg):
        print(f'called EditDetails.new_data with arg `{arg}`')
    def refresh_screen(self):
        print('called EditDetails.refresh_screen')

class MockEditTracks:
    def __init__(self, parent):
        print(f'called EditTracks.__init__ with arg `{parent}`')
    def create_widgets(self):
        print('called EditTracks.create_widgets')
    def new_data(self, arg):
        print(f'called EditTracks.new_data with arg `{arg}`')
    def refresh_screen(self):
        print('called EditTracks.refresh_screen')

class MockEditRecordings:
    def __init__(self, parent):
        print(f'called EditRecordings.__init__ with arg `{parent}`')
    def create_widgets(self):
        print('called EditRecordings.create_widgets')
    def new_data(self, arg):
        print(f'called EditRecordings.new_data with arg `{arg}`')
    def refresh_screen(self):
        print('called EditRecordings.refresh_screen')

class MockDialog:
    def __init__(self, parent):
        print('called NewArtistDialog')
    def exec_(self):
        return testee.qtw.QDialog.Accepted
    def refresh_screen(self):
        print('called Artists.refresh_screen')

class MockArtists:
    def __init__(self, parent):
        print(f'called Artists.__init__ with arg `{parent}`')
    def create_widgets(self):
        print('called Artists.create_widgets')
    def refresh_screen(self):
        print('called Artists.refresh_screen')


def test_main_init(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QApplication', mockqtw.MockApplication)
    monkeypatch.setattr(testee.qtw, 'QMainWindow', mockqtw.MockMainWindow)
    monkeypatch.setattr(testee.MainFrame, 'move', mockqtw.MockMainWindow.move)
    monkeypatch.setattr(testee.MainFrame, 'show', mockqtw.MockMainWindow.show)
    monkeypatch.setattr(testee.MainFrame, 'do_start', MockMainFrame.do_start)
    monkeypatch.setattr(testee.MainFrame, 'go', MockMainFrame.go)
    testobj = testee.MainFrame()
    assert capsys.readouterr().out == ('called QApplication.__init__\n'
                                       'called QMainWindow.__init__\n'
                                       'called QMainWindow.move with args (300, 50)\n'
                                       'called QMainWindow.show\n'
                                       'called MainFrame.do_start\n'
                                       'called MainFrame.go\n')
    assert testobj.artist == None
    assert testobj.album == None
    assert testobj.albumtype == ''
    assert testobj.searchtype == 1
    assert testobj.search_arg == ''
    assert testobj.sorttype == ''
    assert testobj.old_seltype == 0
    assert testobj.albumdata == {}
    assert testobj.end == False
    assert testobj.albums == []
    assert testobj.windows == []

def setup_main(monkeypatch, capsys):
    monkeypatch.setattr(testee.MainFrame, '__init__', MockMainFrame.__init__)
    testobj = testee.MainFrame()
    assert capsys.readouterr().out == ('called MainFrame.__init__\n'
                                       'called QApplication.__init__\n')
    return testobj

def test_main_go(monkeypatch, capsys):
    testobj = setup_main(monkeypatch, capsys)
    with pytest.raises(SystemExit):
        testobj.go()
    assert capsys.readouterr().out == 'called QApplication.exec_\n'

def test_main_get_all_artists(monkeypatch, capsys):
    artist1 = types.SimpleNamespace(id=1, get_name=lambda: 'x')
    artist2 = types.SimpleNamespace(id=2, get_name=lambda: 'y')
    def mock_get_list():
        return artist1, artist2
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee, 'get_artist_list', mock_get_list)
    testobj.get_all_artists()
    assert testobj.all_artists == (artist1, artist2)
    assert testobj.artists == testobj.all_artists
    assert testobj.artist_names == ['x', 'y']
    assert testobj.artist_ids == [1, 2]

def test_main_do_start(monkeypatch, capsys):
    def mock_get():
        print('called MainFrame.get_all_artists')
    def mock_setwidget(arg):
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'get_all_artists', mock_get)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'Start', MockStart)
    testobj.windows = []
    testobj.do_start()
    assert testobj.artist_filter == ''
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockStart
    assert capsys.readouterr().out == ('called MainFrame.get_all_artists\n'
                                       f'called Start.__init__ with arg `{testobj}`\n'
                                       'called Start.create_widgets\n'
                                       'called Start.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockStart}`\n')

def test_main_do_select(monkeypatch, capsys):
    def mock_get_1(*args):
        print('called get_albums_by_artist with args', args)
        return 'albums'
    def mock_get_2(*args):
        print('called get_albums_by_text with args', args)
        return 'albums'
    def mock_setwidget(arg):
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee, 'get_albums_by_artist', mock_get_1)
    monkeypatch.setattr(testee, 'get_albums_by_text', mock_get_2)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'Artists', MockArtists)
    monkeypatch.setattr(testee, 'Select', MockSelect)
    testobj.windows = []
    testobj.albumtype = 'artist'
    testobj.do_select()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockArtists
    assert capsys.readouterr().out == (f'called Artists.__init__ with arg `{testobj}`\n'
                                       'called Artists.create_widgets\n'
                                       'called Artists.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockArtists}`\n')
    testobj.windows = []
    testobj.albumtype = 'rtist'
    testobj.searchtype = 1
    testobj.artist = types.SimpleNamespace(id='x')
    testobj.sorttype = 0
    testobj.do_select()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockSelect
    assert testobj.albums == 'albums'
    assert capsys.readouterr().out == ("called get_albums_by_artist with args ('rtist', 'x', 0)\n"
                                       f'called Select.__init__ with arg `{testobj}`\n'
                                       'called Select.create_widgets\n'
                                       'called Select.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockSelect}`\n')
    testobj.windows = []
    testobj.albumtype = 'rtist'
    testobj.searchtype = 0
    testobj.search_arg = 'y'
    testobj.artist = types.SimpleNamespace(id='x')
    testobj.sorttype = 1
    testobj.do_select()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockSelect
    assert testobj.albums == 'albums'
    assert capsys.readouterr().out == ("called get_albums_by_text with args ('rtist', 0, 'y', 1)\n"
                                       f'called Select.__init__ with arg `{testobj}`\n'
                                       'called Select.create_widgets\n'
                                       'called Select.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockSelect}`\n')

def test_main_do_new(monkeypatch, capsys):
    def mock_get():
        print('called Main.get_all_artists')
    def mock_select():
        print('called.Main.do_select')
    def mock_get_album(*args):
        print('called get_album with args', args)
    def mock_edit(**args):
        print('called Main.do_edit_alg with args', args)
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee, 'NewArtistDialog', MockDialog)
    monkeypatch.setattr(testobj, 'get_all_artists', mock_get)
    monkeypatch.setattr(testobj, 'do_select', mock_select)
    monkeypatch.setattr(testee, 'get_album', mock_get_album)
    monkeypatch.setattr(testobj, 'do_edit_alg', mock_edit)
    testobj.albumtype = 'x'
    testobj.do_new()
    assert capsys.readouterr().out == ("called get_album with args (0, 'x')\n"
                                       "called Main.do_edit_alg with args {'new': True,"
                                       " 'keep_sel': False}\n")
    testobj.do_new(keep_sel=True)
    assert capsys.readouterr().out == ("called get_album with args (0, 'x')\n"
                                       "called Main.do_edit_alg with args {'new': True,"
                                       " 'keep_sel': True}\n")
    testobj.albumtype = 'artist'
    testobj.do_new()
    assert capsys.readouterr().out == ('called NewArtistDialog\n'
                                       'called Main.get_all_artists\n'
                                       'called.Main.do_select\n')
    monkeypatch.setattr(MockDialog, 'exec_', lambda *x: testee.qtw.QDialog.Rejected)
    monkeypatch.setattr(testee, 'NewArtistDialog', MockDialog)
    testobj.do_new()
    assert capsys.readouterr().out == ('called NewArtistDialog\n')

def test_main_do_detail(monkeypatch, capsys):
    def mock_get(*args):
        print('called get_album with args', args)
    def mock_setwidget(arg):
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee, 'get_album', mock_get)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'Artists', MockArtists)
    monkeypatch.setattr(testee, 'Detail', MockDetail)
    testobj.windows = []
    testobj.albumtype = 'artist'
    testobj.do_detail()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockArtists
    assert capsys.readouterr().out == (f'called Artists.__init__ with arg `{testobj}`\n'
                                       'called Artists.create_widgets\n'
                                       'called Artists.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockArtists}`\n')
    testobj.windows = []
    testobj.albumtype = 'x'
    testobj.album = types.SimpleNamespace(id=1)
    testobj.do_detail()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockDetail
    assert capsys.readouterr().out == ("called get_album with args (1, 'x')\n"
                                       f'called Detail.__init__ with arg `{testobj}`\n'
                                       'called Detail.create_widgets\n'
                                       'called Detail.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockDetail}`\n')

def test_main_do_edit_alg(monkeypatch, capsys):
    def mock_setwidget(arg):
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'EditDetails', MockEditDetails)
    testobj.windows = []
    testobj.do_edit_alg()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockEditDetails
    assert capsys.readouterr().out == (f'called EditDetails.__init__ with arg `{testobj}`\n'
                                       'called EditDetails.create_widgets\n'
                                       'called EditDetails.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditDetails}`\n')
    testobj.windows = []
    testobj.do_edit_alg(new=True)
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockEditDetails
    assert capsys.readouterr().out == (f'called EditDetails.__init__ with arg `{testobj}`\n'
                                       'called EditDetails.create_widgets\n'
                                       'called EditDetails.new_data with arg `False`\n'
                                       'called EditDetails.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditDetails}`\n')
    testobj.windows = []
    testobj.do_edit_alg(new=True, keep_sel=True)
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockEditDetails
    assert capsys.readouterr().out == (f'called EditDetails.__init__ with arg `{testobj}`\n'
                                       'called EditDetails.create_widgets\n'
                                       'called EditDetails.new_data with arg `True`\n'
                                       'called EditDetails.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditDetails}`\n')

def test_main_do_edit_trk(monkeypatch, capsys):
    def mock_setwidget(arg):
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'EditTracks', MockEditTracks)
    testobj.windows = []
    testobj.do_edit_trk()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockEditTracks
    assert capsys.readouterr().out == (f'called EditTracks.__init__ with arg `{testobj}`\n'
                                       'called EditTracks.create_widgets\n'
                                       'called EditTracks.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditTracks}`\n')

def test_main_do_edit_rec(monkeypatch, capsys):
    def mock_setwidget(arg):
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'EditRecordings', MockEditRecordings)
    testobj.windows = []
    testobj.do_edit_rec()
    assert len(testobj.windows) == 1
    assert type(testobj.windows[0]) == MockEditRecordings
    assert capsys.readouterr().out == (f'called EditRecordings.__init__ with arg `{testobj}`\n'
                                       'called EditRecordings.create_widgets\n'
                                       'called EditRecordings.refresh_screen\n'
                                       'called Main.setCentralWidget with arg'
                                       f" `{MockEditRecordings}`\n")

def test_main_start_import_tool(monkeypatch, capsys):
    def mock_mainframe(**args):
        print('called AlbumsMatcher with args', args)
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee.apps.albumsmatcher, 'MainFrame', mock_mainframe)
    testobj.start_import_tool()
    assert capsys.readouterr().out == f"called AlbumsMatcher with args {{'app': {testobj.app}}}\n"

class MockMain:  # evt. vervangen door MockMainFrame (en die dan aanvullen)
    def do_start(self):
        print('called Main.do_start')
    def do_select(self):
        print('called Main.do_select')
    def do_new(self):
        print('called Main.do_new')
    def start_import_tool(self):
        print('called Main.start_import_tool')
    def close(self):
        print('called Main.close')

def setup_start(monkeypatch, capsys):
    def mock_init(self):
        print('called QWidget.__init__')
        self._parent = MockMain()
    def mock_setLayout(self, arg):
        print(f'called QWidget.setLayout with arg of type {type(arg)}')
    def mock_parent(self):
        return self._parent
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setLayout)
    monkeypatch.setattr(testee.Start, 'parent', mock_parent)
    testobj = testee.Start()    # wil ik hier niet juist MockStart?
    assert capsys.readouterr().out == 'called QWidget.__init__\n'
    return testobj

def test_start_create_widgets(monkeypatch, capsys, expected_output):
    def mock_newline(*args):
        print(f'called newline with arg of type {type(args[0])}')
        return mockqtw.MockHBox
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGrid)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee, 'newline', mock_newline)
    testobj = setup_start(monkeypatch, capsys)
    testobj.create_widgets()
    bindings = {'select_album': testobj.select_album,
                'new_album': testobj.new_album,
                'select_concert': testobj.select_concert,
                'new_concert': testobj.new_concert,
                'view_artists': testobj.view_artists,
                'new_artist': testobj.new_artist,
                'start_imp': testobj.parent().start_import_tool,
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['start'].format(**bindings)

def test_start_refresh_screen(monkeypatch, capsys):
    testobj = setup_start(monkeypatch, capsys)
    testobj.ask_studio_artist = mockqtw.MockComboBox()
    testobj.ask_studio_search = mockqtw.MockComboBox()
    testobj.ask_studio_sort = mockqtw.MockComboBox()
    testobj.studio_zoektekst = mockqtw.MockLineEdit()
    testobj.ask_live_artist = mockqtw.MockComboBox()
    testobj.ask_live_search = mockqtw.MockComboBox()
    testobj.ask_live_sort = mockqtw.MockComboBox()
    testobj.live_zoektekst = mockqtw.MockLineEdit()
    testobj.parent().artist_names = ['twee', 'een']
    testobj.parent().albumtype = 'x'
    testobj.parent().searchtype = 1
    testobj.refresh_screen()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       "called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       "called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       'called ComboBox.setCurrentIndex to `1`\n'
                                       'called ComboBox.setCurrentIndex to `3`\n'
                                       'called ComboBox.setCurrentIndex to `1`\n'
                                       'called ComboBox.setCurrentIndex to `2`\n')
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 1
    testobj.parent().sorttype = 'x'
    testobj.parent().artistids = [2, 1]
    testobj.parent().artist = types.SimpleNamespace(id=1)
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       "called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       "called ComboBox.setCurrentIndex to `1`\n"
                                       "called ComboBox.setCurrentIndex to `2`\n"
                                       "called LineEdit.clear\n"
                                       "called ComboBox.setCurrentText to `x`\n")
    testobj.parent().albumtype = 'live'
    testobj.parent().searchtype = 1
    testobj.parent().sorttype = 'y'
    testobj.parent().artist = types.SimpleNamespace(id=2)
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       "called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       "called ComboBox.setCurrentIndex to `1`\n"
                                       "called ComboBox.setCurrentIndex to `1`\n"
                                       "called LineEdit.clear\n"
                                       "called ComboBox.setCurrentText to `y`\n")
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 0
    testobj.parent().sorttype = 'z'
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       "called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       'called ComboBox.setCurrentIndex to `0`\n'
                                       'called LineEdit.clear\n'
                                       'called ComboBox.setCurrentText to `z`\n')
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 2
    testobj.parent().search_arg= 'y'
    testobj.parent().sorttype = 'x'
    testobj.parent().artist = types.SimpleNamespace(id=0)
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       "called ComboBox.addItems with arg `['twee', 'een']`\n"
                                       'called ComboBox.setCurrentIndex to `2`\n'
                                       'called LineEdit.setText with arg `y`\n'
                                       'called ComboBox.setCurrentText to `x`\n')

def test_start_select_album(monkeypatch, capsys):
    def mock_select(self, *args):
        print('called Start._select with args', args)
    monkeypatch.setattr(testee.Start, '_select', mock_select)
    testobj = setup_start(monkeypatch, capsys)
    testobj.ask_studio_search = 1
    testobj.ask_studio_artist = 'y'
    testobj.studio_zoektekst = 'z'
    testobj.ask_studio_sort = 1
    testobj.select_album()
    assert capsys.readouterr().out == "called Start._select with args ('studio', 1, 'y', 'z', 1)\n"

def test_start_select_concert(monkeypatch, capsys):
    def mock_select(self, *args):
        print('called Start._select with args', args)
    monkeypatch.setattr(testee.Start, '_select', mock_select)
    testobj = setup_start(monkeypatch, capsys)
    testobj.ask_live_search = 1
    testobj.ask_live_artist = 'y'
    testobj.live_zoektekst = 'z'
    testobj.ask_live_sort = 1
    testobj.select_concert()
    assert capsys.readouterr().out == "called Start._select with args ('live', 1, 'y', 'z', 1)\n"

def test_start_select_1(monkeypatch, capsys):
    # geen selectie
    counter = 0
    def mock_index(self):
        nonlocal counter
        counter += 1
        return [1, 0][counter]
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index)
    testobj = setup_start(monkeypatch, capsys)
    testobj.parent().artists = ['x', 'y', 'z']
    typewin = mockqtw.MockComboBox()
    actwin = mockqtw.MockComboBox()
    argwin = mockqtw.MockLineEdit()
    sortwin = mockqtw.MockComboBox()
    testobj._select('studio', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 0
    # assert testobj.parent().artist == 1
    # assert testobj.parent().search_arg == 'x'
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().sorttype == '.'
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ComboBox.currentText\n'
                                       'called Main.do_select\n')

def test_start_select_2(monkeypatch, capsys):
    # selectie op artist
    counter = 0
    def mock_index(self):
        nonlocal counter
        counter += 1
        return [0, 1, 2][counter]
    def mock_index_2(self):
        nonlocal counter
        counter += 1
        return [0, 1, 0][counter]
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_start(monkeypatch, capsys)
    testobj.parent().artists = ['x', 'y', 'z']
    typewin = mockqtw.MockComboBox()
    actwin = mockqtw.MockComboBox()
    argwin = mockqtw.MockLineEdit()
    sortwin = mockqtw.MockComboBox()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.__init__\n')
    testobj._select('live', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 1
    assert testobj.parent().artist == 'y'
    assert testobj.parent().search_arg == 'y'
    assert testobj.parent().albumtype == 'live'
    assert testobj.parent().sorttype == '.'
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called Main.do_select\n')
    counter = 0
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index_2)
    testobj._select('live', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 1
    # assert testobj.parent().artist == 'y'
    # assert testobj.parent().search_arg == ''
    assert testobj.parent().albumtype == 'live'
    assert testobj.parent().sorttype == '.'
    assert capsys.readouterr().out == ('called QMessageBox.information with args'
                                       ' `Albums` `Selecteer een uitvoerende`\n')

def test_start_select_3(monkeypatch, capsys):
    counter = 0
    def mock_index(self):
        nonlocal counter
        counter += 1
        return[2, 3][counter]
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_start(monkeypatch, capsys)
    typewin = mockqtw.MockComboBox()
    actwin = mockqtw.MockComboBox()
    argwin = mockqtw.MockLineEdit()
    sortwin = mockqtw.MockComboBox()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.__init__\n')
    testobj._select('studio', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 3
    # assert testobj.parent().artist == ''
    assert testobj.parent().search_arg == '..'
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().sorttype == '.'
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called ComboBox.currentText\n'
                                       'called Main.do_select\n')
    counter = 0
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda *x: '')
    testobj._select('studio', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 3
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().sorttype == '.'
    assert capsys.readouterr().out == ('called QMessageBox.information with args'
                                       ' `Albums` `Geef een zoekargument op`\n')

def test_start_new_album(monkeypatch, capsys):
    def mock_new(self, *args):
        print('called Start._new with args', args)
    monkeypatch.setattr(testee.Start, '_new', mock_new)
    testobj = setup_start(monkeypatch, capsys)
    testobj.new_album()
    assert capsys.readouterr().out == "called Start._new with args ('studio',)\n"

def test_start_new_concert(monkeypatch, capsys):
    def mock_new(self, *args):
        print('called Start._new with args', args)
    monkeypatch.setattr(testee.Start, '_new', mock_new)
    testobj = setup_start(monkeypatch, capsys)
    testobj.new_concert()
    assert capsys.readouterr().out == "called Start._new with args ('live',)\n"

def test_start_new(monkeypatch, capsys):
    testobj = setup_start(monkeypatch, capsys)
    testobj._new('x')
    assert testobj.parent().albumtype == 'x'
    assert capsys.readouterr().out == 'called Main.do_new\n'

def test_start_view_artists(monkeypatch, capsys):
    testobj = setup_start(monkeypatch, capsys)
    testobj.view_artists()
    assert testobj.parent().albumtype == 'artist'
    assert capsys.readouterr().out == 'called Main.do_select\n'

def test_start_new_artist(monkeypatch, capsys):
    testobj = setup_start(monkeypatch, capsys)
    testobj.new_artist()
    assert testobj.parent().albumtype == 'artist'
    assert capsys.readouterr().out == 'called Main.do_new\n'

def test_start_exit(monkeypatch, capsys):
    testobj = setup_start(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


class _TestSelect:
    def test_create_widgets(self):
        ...

    def test_refresh_screen(self):
        ...

    def test_other_artist(self):
        ...

    def test_other_search(self):
        ...

    def test_other_albumtype(self):
        ...

    def test_todetail(self):
        ...

    def test_add_new_to_sel(self):
        ...

    def test_exit(self):
        ...


class _TestDetail:
    def test_create_widgets(self):
        ...

    def test_refresh_screen(self):
        ...

    def test_other_album(self):
        ...

    def test_edit_alg(self):
        ...

    def test_edit_trk(self):
        ...

    def test_edit_rec(self):
        ...

    def test_exit(self):
        ...


class _TestEditDetails:
    def test_create_widgets(self):
        ...

    def test_new_data(self, keep_sel=False):
        ...

    def test_refresh_screen(self):
        ...

    def test_submit(self, goback=False):
        def test_replace_details(caption, value):
            ...

    def test_add_another(self):
        ...

    def test_submit_and_back(self):
        ...

    def test_exit(self):
        ...


class _TestEditTracks:
    def test_create_widgets(self):
        ...

    def test_add_track_fields(self, trackindex, trackname='', author='', text=''):
        ...

    def test_refresh_screen(self):
        ...

    def test_add_new_item(self):
        ...

    def test_submit(self, skip_confirm=False):
        ...

    def test_submit_and_back(self):
        ...

    def test_exit(self):
        ...


class _TestEditRecordings:
    def test_create_widgets(self):
        ...

    def test_add_rec_fields(self, opnindex, opname=None):
        ...

    def test_refresh_screen(self):
        ...

    def test_add_new_item(self):
        ...

    def test_submit(self, skip_confirm=False):
        ...

    def test_submit_and_back(self):
        ...

    def test_exit(self):
        ...


class _TestArtists:
    def test_create_widgets(self):
        ...

    def test_filter(self):
        ...

    def test_add_artist_line(self, itemid, first_name='', last_name=''):
        ...

    def test_refresh_screen(self):
        ...

    def test_submit(self):
        ...

    def test_new(self):
        ...

    def test_exit(self):
        ...


class _TestNewArtistDialog:
    def test___init__(self, parent):
        ...

    def test_update(self):
        ...
