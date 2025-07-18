"""unittests for ./apps/albums_gui.py
"""
import types
import pytest
import apps.albums_gui as testee
import mockgui.mockqtwidgets as mockqtw
from buildscreen_output_fixture import expected_output


#  helper class voor test_button_strip en text_exitbutton
class MockHandler:
    """mock van een subscherm, alleen omdat ik de aanroepen nodog heb
    """
    class MockParent:
        """mock van het hoofdscherm, alleen omdat ik de methode aanroepen nodig heb
        """
        def do_select(self):
            """stub
            """
        def do_start(self):
            """stub
            """
        def do_detail(self):
            """stub
            """
    _parent = MockParent()
    def parent(self):
        """stub
        """
        return self._parent
    def submit(self):
        """stub
        """
    def submit_and_back(self):
        """stub
        """
    def new(self):
        """stub
        """
    def do_select(self):
        """stub
        """
    def do_start(self):
        """stub
        """


# mock implementations of module-level functions
def mock_newline(*args):
    """stub for albums_gui.newline
    """
    print(f'called newline with arg {type(args[0]).__name__}')
    return mockqtw.MockHBoxLayout()

def mock_button_strip(*args):
    """stub for albums_gui.button_strip
    """
    print('called button_strip with args', args)
    return mockqtw.MockHBoxLayout()

def mock_exitbutton(*args, **kwargs):
    """stub for albums_gui.exitbutton
    """
    if len(args) == 3:
        print(f'called exitbutton with args {args[0]}, {args[1]}, {type(args[2]).__name__}')
    else:
        print('called exitbutton with args', args, kwargs)
    return mockqtw.MockHBoxLayout()


# mock implementations of application classes
class MockMainFrame:
    """stub for albums_gui.MainFrame object
    """
    def __init__(self):
        print('called Main.__init__')
        self.app = mockqtw.MockApplication()
    def go(self):
        """stub
        """
        print('called Main.go')
    def do_start(self):
        """stub
        """
        print('called Main.do_start')
    def do_select(self):
        """stub
        """
        print('called Main.do_select')
    def do_new(self, **kwargs):
        """stub
        """
        print('called Main.do_new with args', kwargs)
    def do_detail(self):
        """stub
        """
        print('called Main.do_detail')
    # def do_edit_alg(self, **kwargs):
    #    print(f'called Main.do_edit_alg with args', kwargs)
    def do_edit_alg(self):
        """stub
        """
        print('called Main.do_edit_alg')
    def do_edit_trk(self):
        """stub
        """
        print('called Main.do_edit_trk')
    def do_edit_rec(self):
        """stub
        """
        print('called Main.do_edit_rec')
    def get_all_artists(self):
        """stub
        """
        print('called Main.get_all_artists')
    def start_import_tool(self):
        """stub
        """
        print('called Main.start_import_tool')
    def close(self):
        """stub
        """
        print('called Main.close')


class MockStart:
    """stub for albums_gui.Start object
    """
    def __init__(self, parent):
        print(f'called Start.__init__ with arg `{parent}`')
    def create_widgets(self):
        """stub
        """
        print('called Start.create_widgets')
    def refresh_screen(self):
        """stub
        """
        print('called Start.refresh_screen')


class MockSelect:
    """stub for albums_gui.Select object
    """
    def __init__(self, parent):
        print(f'called Select.__init__ with arg `{parent}`')
    def create_widgets(self):
        """stub
        """
        print('called Select.create_widgets')
    def refresh_screen(self):
        """stub
        """
        print('called Select.refresh_screen')


class MockDetail:
    """stub for albums_gui.Detail object
    """
    def __init__(self, parent):
        print(f'called Detail.__init__ with arg `{parent}`')
    def create_widgets(self):
        """stub
        """
        print('called Detail.create_widgets')
    def refresh_screen(self):
        """stub
        """
        print('called Detail.refresh_screen')


class MockEditDetails:
    """stub for albums_gui.EditDetails object
    """
    def __init__(self, parent):
        print(f'called EditDetails.__init__ with arg `{parent}`')
    def create_widgets(self):
        """stub
        """
        print('called EditDetails.create_widgets')
    def new_data(self, arg):
        """stub
        """
        print(f'called EditDetails.new_data with arg `{arg}`')
    def refresh_screen(self):
        """stub
        """
        print('called EditDetails.refresh_screen')


class MockEditTracks:
    """stub for albums_gui.EditTracks object
    """
    def __init__(self, parent):
        print(f'called EditTracks.__init__ with arg `{parent}`')
    def create_widgets(self):
        """stub
        """
        print('called EditTracks.create_widgets')
    def new_data(self, arg):
        """stub
        """
        print(f'called EditTracks.new_data with arg `{arg}`')
    def refresh_screen(self):
        """stub
        """
        print('called EditTracks.refresh_screen')


class MockEditRecordings:
    """stub for albums_gui.EditRecordings object
    """
    def __init__(self, parent):
        print(f'called EditRecordings.__init__ with arg `{parent}`')
    def create_widgets(self):
        """stub
        """
        print('called EditRecordings.create_widgets')
    def new_data(self, arg):
        """stub
        """
        print(f'called EditRecordings.new_data with arg `{arg}`')
    def refresh_screen(self):
        """stub
        """
        print('called EditRecordings.refresh_screen')


class MockNewArtist:
    """stub for albums_gui.NewArtistDialog object
    """
    def __init__(self, parent):
        print('called NewArtistDialog')
    def exec(self):
        """stub
        """
        return testee.qtw.QDialog.DialogCode.Accepted
    def refresh_screen(self):
        """stub
        """
        print('called Artists.refresh_screen')


class MockArtists:
    """stub for albums_gui.Artists object
    """
    def __init__(self, parent):
        print(f'called Artists.__init__ with arg `{parent}`')
    def create_widgets(self):
        """stub
        """
        print('called Artists.create_widgets')
    def refresh_screen(self):
        """stub
        """
        print('called Artists.refresh_screen')


# module level functions ------------------
def test_get_artist_list(monkeypatch):
    """unittest for albums_gui.get_artist_list
    """
    monkeypatch.setattr(testee.dmla, 'list_artists', lambda: ['x', 'y'])
    assert testee.get_artist_list() == ['x', 'y']


def test_get_albums_by_artist(monkeypatch, capsys):
    """unittest for albums_gui.get_albums_by_artist
    """
    def mock_list(*args):
        """stub
        """
        print('called dmla.list_albums_by_artist with args', args)
        return ['x', 'y', 'z']
    monkeypatch.setattr(testee.dmla, 'list_albums_by_artist', mock_list)
    assert testee.get_albums_by_artist('albumtype', 'search_for', 'sort_on') == ['x', 'y', 'z']
    assert capsys.readouterr().out == ('called dmla.list_albums_by_artist with args'
                                       " ('albumtype', 'search_for', 'sort_on')\n")


def test_get_albums_by_text(monkeypatch, capsys):
    """unittest for albums_gui.get_albums_by_text
    """
    def mock_list(*args):
        """stub
        """
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
    """unittest for albums_gui.get_album
    """
    myact = testee.dmla.my.Act()
    def mock_list(id_):
        """stub
        """
        print(f'called dmla.list_album_details with arg `{id_}`')
        return types.SimpleNamespace(name='x', artist=myact, label='y', release_year='z',
                                     produced_by='a', credits='b', bezetting='c', additional='d')
    def mock_list_2(id_):
        """stub
        """
        print(f'called dmla.list_album_details with arg `{id_}`')
        return types.SimpleNamespace(name='x', artist=myact, label='y', release_year='',
                                     produced_by='a', credits='b', bezetting='c', additional='d')
    def mock_list_3(id_):
        """stub
        """
        print(f'called dmla.list_album_details with arg `{id_}`')
        return types.SimpleNamespace(name='x', artist=myact, label='', release_year='z',
                                     produced_by='a', credits='b', bezetting='c', additional='d')
    def mock_get_name(id_):
        """stub
        """
        print(f'called artist.get_name with arg `{id_}`')
        return 'name'
    def mock_list_tracks(id_):
        """stub
        """
        print(f'called dmla.list_album_tracks with arg `{id_}`')
        return [types.SimpleNamespace(volgnr=1, name='e', written_by='f', credits='g')]
    def mock_list_recordings(id_):
        """stub
        """
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
    monkeypatch.setattr(testee.dmla, 'list_album_details', mock_list_2)
    assert testee.get_album(9, 'studio') == {'titel': 'x', 'artist': myact, 'artist_name': 'name',
                                             'details': [('Label/jaar:', 'y'),
                                                         ('Produced by:', 'a'), ('Credits:', 'b'),
                                                         ('Bezetting:', 'c'), ('Tevens met:', 'd')],
                                             'tracks': {1: ('e', 'f', 'g')}, 'opnames': [('h', 'i')]}
    assert capsys.readouterr().out == ('called dmla.list_album_details with arg `9`\n'
                                       'called artist.get_name with arg ``\n'
                                       'called dmla.list_album_tracks with arg `9`\n'
                                       'called dmla.list_album_recordings with arg `9`\n')
    monkeypatch.setattr(testee.dmla, 'list_album_details', mock_list_3)
    assert testee.get_album(9, 'studio') == {'titel': 'x', 'artist': myact, 'artist_name': 'name',
                                             'details': [('Label/jaar:', 'z'),
                                                         ('Produced by:', 'a'), ('Credits:', 'b'),
                                                         ('Bezetting:', 'c'), ('Tevens met:', 'd')],
                                             'tracks': {1: ('e', 'f', 'g')}, 'opnames': [('h', 'i')]}
    assert capsys.readouterr().out == ('called dmla.list_album_details with arg `9`\n'
                                       'called artist.get_name with arg ``\n'
                                       'called dmla.list_album_tracks with arg `9`\n'
                                       'called dmla.list_album_recordings with arg `9`\n')


def test_build_heading_new_1(monkeypatch, capsys):
    """unittest for albums_gui.build_heading_new: empty albumdata values
    """
    def mock_parent():
        """stub
        """
        return types.SimpleNamespace(albumtype='x', albumdata={'artist': '', 'titel': 'b'})
    def mock_text():
        """stub
        """
        return 'x'
    monkeypatch.setattr(testee, 'TYPETXT', {'x': 'dinges'})
    win = types.SimpleNamespace(parent=mock_parent, heading=types.SimpleNamespace(text=mock_text))
    assert testee.build_heading(win) == "Opvoeren nieuw dinges"


def test_build_heading_new_2(monkeypatch, capsys):
    """unittest for albums_gui.build_heading_new: filled albumdata value
    """
    def mock_parent():
        """stub
        """
        return types.SimpleNamespace(albumtype='x', albumdata={'artist': 'a', 'titel': ''})
    def mock_text():
        """stub
        """
        return 'x'
    monkeypatch.setattr(testee, 'TYPETXT', {'x': 'dinges'})
    win = types.SimpleNamespace(parent=mock_parent, heading=types.SimpleNamespace(text=mock_text))
    assert testee.build_heading(win) == "Opvoeren nieuw dinges"


def test_build_heading(monkeypatch, capsys):
    """unittest for albums_gui.build_heading
    """
    def mock_parent():
        """stub
        """
        return types.SimpleNamespace(albumtype='x', albumdata={'artist': 'a', 'titel': 'b'})
    counter = 0
    def mock_text():
        """stub
        """
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
    """unittest for albums_gui.newline
    """
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    assert isinstance(testee.newline('parent'), mockqtw.MockHBoxLayout)
    assert capsys.readouterr().out == ('called HBox.__init__\n'
                                       'called Frame.__init__\n'
                                       'called Frame.setFrameShape with arg `---`\n'
                                       'called HBox.addWidget with arg MockFrame\n')


def test_button_strip(monkeypatch, capsys):
    """unittest for albums_gui.button_strip
    """
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    assert isinstance(testee.button_strip(MockHandler()), mockqtw.MockHBoxLayout)
    assert capsys.readouterr().out == ('called HBox.__init__\n'
                                       'called HBox.addStretch\n'
                                       'called HBox.addStretch\n')
    buttons = ['Cancel', 'Go', 'GoBack', 'Edit', 'New', 'Select', 'Start']
    handler = MockHandler()
    assert isinstance(testee.button_strip(handler, *buttons), mockqtw.MockHBoxLayout)
    assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('Afbreken', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.parent().do_detail},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('Uitvoeren', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.submit},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('Uitvoeren en terug', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.submit_and_back},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('Wijzigingen doorvoeren', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.submit},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('Nieuwe opvoeren', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.new},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('Terug naar Selectie', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.parent().do_select},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('Terug naar Startscherm', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.parent().do_start},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            'called HBox.addStretch\n')


def test_create_exitbutton(monkeypatch, capsys):
    """unittest for albums_gui.create_exitbutton
    """
    monkeypatch.setattr(mockqtw.MockMessageBox, 'addButton', lambda *x: 'button')
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    assert testee.create_next_button(testee.qtw.QMessageBox) == 'button'
    assert capsys.readouterr().out == ''


def test_exitbutton(monkeypatch, capsys):
    """unittest for albums_gui.exitbutton
    """
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    handler = MockHandler()
    assert isinstance(testee.exitbutton(handler, handler.submit), mockqtw.MockHBoxLayout)
    assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('E&xit', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.submit},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            'called HBox.addStretch\n')
    assert isinstance(testee.exitbutton(handler, handler.submit, extrawidget='extra'),
                      mockqtw.MockHBoxLayout)
    assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            "called HBox.addWidget with arg str\n"
            f"called PushButton.__init__ with args ('E&xit', {handler}) {{}}\n"
            f"called Signal.connect with args ({handler.submit},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            'called HBox.addStretch\n')


# Main Window --------------
def test_main_init(monkeypatch, capsys):
    """unittest for albums_gui.Main.init
    """
    def mock_app_init(self, *args):
        """stub
        """
        print('called Application.__init__')
    def mock_init(self, *args):
        """stub
        """
        print('called MainWindow.__init__')
    monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
    monkeypatch.setattr(testee.MainFrame, 'move', mockqtw.MockMainWindow.move)
    monkeypatch.setattr(testee.MainFrame, 'show', mockqtw.MockMainWindow.show)
    monkeypatch.setattr(testee.MainFrame, 'do_start', MockMainFrame.do_start)
    monkeypatch.setattr(testee.MainFrame, 'go', MockMainFrame.go)
    testobj = testee.MainFrame()
    assert capsys.readouterr().out == ('called Application.__init__\n'
                                       'called MainWindow.__init__\n'
                                       'called MainWindow.move with args (300, 50)\n'
                                       'called MainWindow.show\n'
                                       'called Main.do_start\n'
                                       'called Main.go\n')
    assert testobj.artist is None
    assert testobj.album is None
    assert testobj.albumtype == ''
    assert testobj.searchtype == 1
    assert testobj.search_arg == ''
    assert testobj.sorttype == ''
    assert testobj.old_seltype == 0
    assert testobj.albumdata == {}
    assert not testobj.end
    assert testobj.albums == []
    assert testobj.windows == []

def setup_main(monkeypatch, capsys):
    """stub for setting up Main object
    """
    monkeypatch.setattr(testee.MainFrame, '__init__', MockMainFrame.__init__)
    testobj = testee.MainFrame()
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n')
    return testobj

def test_main_go(monkeypatch, capsys):
    """unittest for albums_gui.Main.go
    """
    testobj = setup_main(monkeypatch, capsys)
    with pytest.raises(SystemExit):
        testobj.go()
    assert capsys.readouterr().out == 'called Application.exec\n'

def test_main_get_all_artists(monkeypatch, capsys):
    """unittest for albums_gui.Main.get_all_artists
    """
    artist1 = types.SimpleNamespace(id=1, get_name=lambda: 'x')
    artist2 = types.SimpleNamespace(id=2, get_name=lambda: 'y')
    def mock_get_list():
        """stub
        """
        return artist1, artist2
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee, 'get_artist_list', mock_get_list)
    testobj.get_all_artists()
    assert testobj.all_artists == (artist1, artist2)
    assert testobj.artists == testobj.all_artists
    assert testobj.artist_names == ['x', 'y']
    assert testobj.artist_ids == [1, 2]

def test_main_do_start(monkeypatch, capsys):
    """unittest for albums_gui.Main.do_start
    """
    def mock_get():
        """stub
        """
        print('called MainFrame.get_all_artists')
    def mock_setwidget(arg):
        """stub
        """
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'get_all_artists', mock_get)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'Start', MockStart)
    testobj.windows = []
    testobj.do_start()
    assert testobj.artist_filter == ''
    assert len(testobj.windows) == 1
    assert isinstance(testobj.windows[0], MockStart)
    assert capsys.readouterr().out == ('called MainFrame.get_all_artists\n'
                                       f'called Start.__init__ with arg `{testobj}`\n'
                                       'called Start.create_widgets\n'
                                       'called Start.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockStart}`\n')

def test_main_do_select(monkeypatch, capsys):
    """unittest for albums_gui.Main.do_select
    """
    def mock_get_1(*args):
        """stub
        """
        print('called get_albums_by_artist with args', args)
        return 'albums'
    def mock_get_2(*args):
        """stub
        """
        print('called get_albums_by_text with args', args)
        return 'albums'
    def mock_setwidget(arg):
        """stub
        """
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
    assert isinstance(testobj.windows[0], MockArtists)
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
    assert isinstance(testobj.windows[0], MockSelect)
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
    assert isinstance(testobj.windows[0], MockSelect)
    assert testobj.albums == 'albums'
    assert capsys.readouterr().out == ("called get_albums_by_text with args ('rtist', 0, 'y', 1)\n"
                                       f'called Select.__init__ with arg `{testobj}`\n'
                                       'called Select.create_widgets\n'
                                       'called Select.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockSelect}`\n')

def test_main_do_new(monkeypatch, capsys):
    """unittest for albums_gui.Main.do_new
    """
    def mock_get():
        """stub
        """
        print('called Main.get_all_artists')
    def mock_select():
        """stub
        """
        print('called.Main.do_select')
    def mock_get_album(*args):
        """stub
        """
        print('called get_album with args', args)
    def mock_edit(**args):
        """stub
        """
        print('called Main.do_edit_alg with args', args)
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee, 'NewArtistDialog', MockNewArtist)
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
    monkeypatch.setattr(MockNewArtist, 'exec', lambda *x: testee.qtw.QDialog.DialogCode.Rejected)
    monkeypatch.setattr(testee, 'NewArtistDialog', MockNewArtist)
    testobj.do_new()
    assert capsys.readouterr().out == ('called NewArtistDialog\n')

def test_main_do_detail(monkeypatch, capsys):
    """unittest for albums_gui.Main.do_detail
    """
    def mock_get(*args):
        """stub
        """
        print('called get_album with args', args)
    def mock_setwidget(arg):
        """stub
        """
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
    assert isinstance(testobj.windows[0], MockArtists)
    assert capsys.readouterr().out == (f'called Artists.__init__ with arg `{testobj}`\n'
                                       'called Artists.create_widgets\n'
                                       'called Artists.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockArtists}`\n')
    testobj.windows = []
    testobj.albumtype = 'x'
    testobj.album = types.SimpleNamespace(id=1)
    testobj.do_detail()
    assert len(testobj.windows) == 1
    assert isinstance(testobj.windows[0], MockDetail)
    assert capsys.readouterr().out == ("called get_album with args (1, 'x')\n"
                                       f'called Detail.__init__ with arg `{testobj}`\n'
                                       'called Detail.create_widgets\n'
                                       'called Detail.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockDetail}`\n')

def test_main_do_edit_alg(monkeypatch, capsys):
    """unittest for albums_gui.Main.do_edit_alg
    """
    def mock_setwidget(arg):
        """stub
        """
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'EditDetails', MockEditDetails)
    testobj.windows = []
    testobj.do_edit_alg()
    assert len(testobj.windows) == 1
    assert isinstance(testobj.windows[0], MockEditDetails)
    assert capsys.readouterr().out == (f'called EditDetails.__init__ with arg `{testobj}`\n'
                                       'called EditDetails.create_widgets\n'
                                       'called EditDetails.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditDetails}`\n')
    testobj.windows = []
    testobj.do_edit_alg(new=True)
    assert len(testobj.windows) == 1
    assert isinstance(testobj.windows[0], MockEditDetails)
    assert capsys.readouterr().out == (f'called EditDetails.__init__ with arg `{testobj}`\n'
                                       'called EditDetails.create_widgets\n'
                                       'called EditDetails.new_data with arg `False`\n'
                                       'called EditDetails.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditDetails}`\n')
    testobj.windows = []
    testobj.do_edit_alg(new=True, keep_sel=True)
    assert len(testobj.windows) == 1
    assert isinstance(testobj.windows[0], MockEditDetails)
    assert capsys.readouterr().out == (f'called EditDetails.__init__ with arg `{testobj}`\n'
                                       'called EditDetails.create_widgets\n'
                                       'called EditDetails.new_data with arg `True`\n'
                                       'called EditDetails.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditDetails}`\n')

def test_main_do_edit_trk(monkeypatch, capsys):
    """unittest for albums_gui.Main.do_edit_trk
    """
    def mock_setwidget(arg):
        """stub
        """
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'EditTracks', MockEditTracks)
    testobj.windows = []
    testobj.do_edit_trk()
    assert len(testobj.windows) == 1
    assert isinstance(testobj.windows[0], MockEditTracks)
    assert capsys.readouterr().out == (f'called EditTracks.__init__ with arg `{testobj}`\n'
                                       'called EditTracks.create_widgets\n'
                                       'called EditTracks.refresh_screen\n'
                                       f'called Main.setCentralWidget with arg `{MockEditTracks}`\n')

def test_main_do_edit_rec(monkeypatch, capsys):
    """unittest for albums_gui.Main.do_edit_rec
    """
    def mock_setwidget(arg):
        """stub
        """
        print(f'called Main.setCentralWidget with arg `{type(arg)}`')
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
    monkeypatch.setattr(testee, 'EditRecordings', MockEditRecordings)
    testobj.windows = []
    testobj.do_edit_rec()
    assert len(testobj.windows) == 1
    assert isinstance(testobj.windows[0], MockEditRecordings)
    assert capsys.readouterr().out == (f'called EditRecordings.__init__ with arg `{testobj}`\n'
                                       'called EditRecordings.create_widgets\n'
                                       'called EditRecordings.refresh_screen\n'
                                       'called Main.setCentralWidget with arg'
                                       f" `{MockEditRecordings}`\n")

def test_main_start_import_tool(monkeypatch, capsys):
    """unittest for albums_gui.Main.start_import_tool
    """
    def mock_mainframe(**args):
        """stub
        """
        print('called AlbumsMatcher with args', args)
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testee.apps.albumsmatcher, 'MainFrame', mock_mainframe)
    testobj.start_import_tool()
    assert capsys.readouterr().out == f"called AlbumsMatcher with args {{'app': {testobj.app}}}\n"


# Application Start screen
def setup_start(monkeypatch, capsys):
    """stub for setting up Start object
    """
    def mock_init(self, parent):
        """stub
        """
        print('called Widget.__init__')
    def mock_setlayout(self, layout):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(layout).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.Start(testparent)
    monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n'
                                       'called Widget.__init__\n')
    return testobj

def test_start_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.Start.create_widgets
    """
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee, 'newline', mock_newline)
    monkeypatch.setattr(testee, 'exitbutton', mock_exitbutton)
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
    """unittest for albums_gui.Start.refresh_screen
    """
    testobj = setup_start(monkeypatch, capsys)
    testobj.ask_studio_artist = mockqtw.MockComboBox()
    testobj.ask_studio_search = mockqtw.MockComboBox()
    testobj.ask_studio_sort = mockqtw.MockComboBox()
    testobj.studio_zoektekst = mockqtw.MockLineEdit()
    testobj.ask_live_artist = mockqtw.MockComboBox()
    testobj.ask_live_search = mockqtw.MockComboBox()
    testobj.ask_live_sort = mockqtw.MockComboBox()
    testobj.live_zoektekst = mockqtw.MockLineEdit()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n')
    testobj.parent().artist_names = ['twee', 'een']
    testobj.parent().albumtype = 'x'
    testobj.parent().searchtype = 1
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg ['twee', 'een']\n"
                                       "called ComboBox.addItems with arg ['twee', 'een']\n"
                                       'called ComboBox.setCurrentIndex with arg `1`\n'
                                       'called ComboBox.setCurrentIndex with arg `3`\n'
                                       'called ComboBox.setCurrentIndex with arg `1`\n'
                                       'called ComboBox.setCurrentIndex with arg `2`\n')
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 1
    testobj.parent().sorttype = 'x'
    testobj.parent().artist_ids = [2, 1]
    testobj.parent().artist = types.SimpleNamespace(id=1)
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg ['twee', 'een']\n"
                                       "called ComboBox.addItems with arg ['twee', 'een']\n"
                                       "called ComboBox.setCurrentIndex with arg `1`\n"
                                       "called ComboBox.setCurrentIndex with arg `2`\n"
                                       "called LineEdit.clear\n"
                                       "called ComboBox.setCurrentText with arg `x`\n")
    testobj.parent().albumtype = 'live'
    testobj.parent().searchtype = 1
    testobj.parent().sorttype = 'y'
    testobj.parent().artist = types.SimpleNamespace(id=2)
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg ['twee', 'een']\n"
                                       "called ComboBox.addItems with arg ['twee', 'een']\n"
                                       "called ComboBox.setCurrentIndex with arg `1`\n"
                                       "called ComboBox.setCurrentIndex with arg `1`\n"
                                       "called LineEdit.clear\n"
                                       "called ComboBox.setCurrentText with arg `y`\n")
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 0
    testobj.parent().sorttype = 'z'
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg ['twee', 'een']\n"
                                       "called ComboBox.addItems with arg ['twee', 'een']\n"
                                       'called ComboBox.setCurrentIndex with arg `0`\n'
                                       'called LineEdit.clear\n'
                                       'called ComboBox.setCurrentText with arg `z`\n')
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 2
    testobj.parent().search_arg = 'y'
    testobj.parent().sorttype = 'x'
    testobj.parent().artist = types.SimpleNamespace(id=0)
    testobj.refresh_screen()
    assert capsys.readouterr().out == ("called ComboBox.addItems with arg ['twee', 'een']\n"
                                       "called ComboBox.addItems with arg ['twee', 'een']\n"
                                       'called ComboBox.setCurrentIndex with arg `2`\n'
                                       'called LineEdit.setText with arg `y`\n'
                                       'called ComboBox.setCurrentText with arg `x`\n')

def test_start_select_album(monkeypatch, capsys):
    """unittest for albums_gui.Start.select_album
    """
    def mock_select(self, *args):
        """stub
        """
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
    """unittest for albums_gui.Start.select_concert
    """
    def mock_select(self, *args):
        """stub
        """
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
    """unittest for albums_gui.Start.select_1
    """
    # geen selectie
    counter = 0
    def mock_index(self):
        """stub
        """
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
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.__init__\n')
    testobj._select('studio', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 0
    # assert testobj.parent().artist == 1
    # assert testobj.parent().search_arg == 'x'
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().sorttype == 'current text'
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called Main.do_select\n')

def test_start_select_2(monkeypatch, capsys):
    """unittest for albums_gui.Start.select_2
    """
    # selectie op artist
    counter = 0
    def mock_index(self):
        """stub
        """
        nonlocal counter
        counter += 1
        return [0, 1, 2][counter]
    def mock_index_2(self):
        """stub
        """
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
    assert testobj.parent().sorttype == 'current text'
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called Main.do_select\n')
    counter = 0
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index_2)
    testobj._select('live', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 1
    # assert testobj.parent().artist == 'y'
    # assert testobj.parent().search_arg == ''
    assert testobj.parent().albumtype == 'live'
    assert testobj.parent().sorttype == 'current text'
    assert capsys.readouterr().out == (f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Selecteer een uitvoerende`\n')

def test_start_select_3(monkeypatch, capsys):
    """unittest for albums_gui.Start.select_3
    """
    counter = 0
    def mock_index(self):
        """stub
        """
        nonlocal counter
        counter += 1
        return [2, 3][counter]
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_start(monkeypatch, capsys)
    typewin = mockqtw.MockComboBox()
    actwin = mockqtw.MockComboBox()
    argwin = mockqtw.MockLineEdit('..')
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
    assert testobj.parent().sorttype == 'current text'
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called ComboBox.currentText\n'
                                       'called Main.do_select\n')
    counter = 0
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda *x: '')
    testobj._select('studio', typewin, actwin, argwin, sortwin)
    assert testobj.parent().searchtype == 3
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().sorttype == 'current text'
    assert capsys.readouterr().out == (f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Geef een zoekargument op`\n')

def test_start_new_album(monkeypatch, capsys):
    """unittest for albums_gui.Start.new_album
    """
    def mock_new(self, *args):
        """stub
        """
        print('called Start._new with args', args)
    monkeypatch.setattr(testee.Start, '_new', mock_new)
    testobj = setup_start(monkeypatch, capsys)
    testobj.new_album()
    assert capsys.readouterr().out == "called Start._new with args ('studio',)\n"

def test_start_new_concert(monkeypatch, capsys):
    """unittest for albums_gui.Start.new_concert
    """
    def mock_new(self, *args):
        """stub
        """
        print('called Start._new with args', args)
    monkeypatch.setattr(testee.Start, '_new', mock_new)
    testobj = setup_start(monkeypatch, capsys)
    testobj.new_concert()
    assert capsys.readouterr().out == "called Start._new with args ('live',)\n"

def test_start_new(monkeypatch, capsys):
    """unittest for albums_gui.Start.new
    """
    testobj = setup_start(monkeypatch, capsys)
    testobj._new('x')
    assert testobj.parent().albumtype == 'x'
    assert capsys.readouterr().out == 'called Main.do_new with args {}\n'

def test_start_view_artists(monkeypatch, capsys):
    """unittest for albums_gui.Start.view_artists
    """
    testobj = setup_start(monkeypatch, capsys)
    testobj.view_artists()
    assert testobj.parent().albumtype == 'artist'
    assert capsys.readouterr().out == 'called Main.do_select\n'

def test_start_new_artist(monkeypatch, capsys):
    """unittest for albums_gui.Start.new_artist
    """
    testobj = setup_start(monkeypatch, capsys)
    testobj.new_artist()
    assert testobj.parent().albumtype == 'artist'
    assert capsys.readouterr().out == 'called Main.do_new with args {}\n'

def test_start_exit(monkeypatch, capsys):
    """unittest for albums_gui.Start.exit
    """
    testobj = setup_start(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


# Application Selection screen
def setup_select(monkeypatch, capsys):
    """stub for setting up Select object
    """
    def mock_init(self, parent):
        """stub
        """
        print('called Widget.__init__')
    def mock_setlayout(self, layout):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(layout).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.Select(testparent)
    monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n'
                                       'called Widget.__init__\n')
    return testobj

def test_select_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.Select.create_widgets
    """
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
    monkeypatch.setattr(testee, 'newline', mock_newline)
    monkeypatch.setattr(testee, 'button_strip', mock_button_strip)
    monkeypatch.setattr(testee, 'exitbutton', mock_exitbutton)
    testobj = setup_select(monkeypatch, capsys)
    testobj.parent().searchtype = 1                  # conditie 1: of niet 1
    testobj.parent().albumtype = 'live'            # conditie 2: of niet
    testobj.parent().artist_names = ['X', 'Y']                  # loop: of leeg
    testobj.parent().albums = ['1', '2']                  # loop: of leeg
    testobj.create_widgets()
    bindings = {'other_search': testobj.other_search,
                'other_artist': testobj.other_artist,
                'other_albumtype': testobj.other_albumtype,
                'todetail': testobj.todetail,
                'add_new_to_sel': testobj.add_new_to_sel,
                'do_start': testobj.parent().do_start,
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['select_1'].format(**bindings)
    testobj = setup_select(monkeypatch, capsys)
    testobj.parent().searchtype = 2
    testobj.parent().albumtype = 'studio'
    testobj.parent().albums = ['1']
    testobj.create_widgets()
    bindings = {'other_search': testobj.other_search,
                'other_artist': testobj.other_artist,
                'other_albumtype': testobj.other_albumtype,
                'todetail': testobj.todetail,
                'add_new_to_sel': testobj.add_new_to_sel,
                'do_start': testobj.parent().do_start,
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['select_2'].format(**bindings)
    testobj = setup_select(monkeypatch, capsys)
    testobj.parent().searchtype = 3
    testobj.parent().albumtype = 'studio'
    testobj.parent().albums = []
    testobj.create_widgets()
    bindings = {'other_search': testobj.other_search,
                'other_albumtype': testobj.other_albumtype,
                'add_new_to_sel': testobj.add_new_to_sel,
                'do_start': testobj.parent().do_start,
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['select_3'].format(**bindings)
    testobj = setup_select(monkeypatch, capsys)
    testobj.parent().searchtype = 4
    testobj.parent().albumtype = 'studio'
    testobj.parent().albums = []
    testobj.create_widgets()
    bindings = {'other_search': testobj.other_search,
                'todetail': testobj.todetail,
                'add_new_to_sel': testobj.add_new_to_sel,
                'do_start': testobj.parent().do_start,
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['select_3'].format(**bindings)

def test_select_refresh_screen(monkeypatch, capsys):
    """unittest for albums_gui.Select.refresh_screen
    """
    testobj = setup_select(monkeypatch, capsys)
    testobj.heading = mockqtw.MockLabel()
    testobj.change_type = mockqtw.MockLabel()
    testobj.kiestekst = mockqtw.MockLabel()
    testobj.add_new = mockqtw.MockLabel()
    assert capsys.readouterr().out == ('called Label.__init__\n'
                                       'called Label.__init__\n'
                                       'called Label.__init__\n'
                                       'called Label.__init__\n')
    testobj.parent().searchtype = 0
    testobj.parent().albumtype = 'studio'
    testobj.parent().sorttype = 'x'
    testobj.refresh_screen()
    assert capsys.readouterr().out == ('called Label.setText with arg `Lijst studio albums'
                                       ' - selectie: geen selectie gesorteerd op x`\n'
                                       'called Label.setText with arg `concertopnamen`\n'
                                       'called Label.setText with arg `Kies een album'
                                       ' uit de lijst:`\n'
                                       'called Label.setText with arg `voer een nieuw album'
                                       ' op bij deze selectie`\n')
    testobj.parent().searchtype = 1
    testobj.parent().albumtype = 'studio'
    testobj.parent().artist = types.SimpleNamespace(get_name=lambda *x: 'xxx')
    testobj.parent().sorttype = 'x'
    testobj.refresh_screen()
    assert capsys.readouterr().out == ('called Label.setText with arg `Lijst studio albums'
                                       ' - selectie: Artist = xxx gesorteerd op x`\n'
                                       'called Label.setText with arg `concertopnamen`\n'
                                       'called Label.setText with arg `Kies een album'
                                       ' uit de lijst:`\n'
                                       'called Label.setText with arg `voer een nieuw album'
                                       ' op bij deze selectie`\n')
    monkeypatch.setattr(testee, 'SELCOL', {'studio': ['', '', 'aaa', 'bbb', 'ccc']})
    testobj.parent().searchtype = 2
    testobj.parent().search_arg = 'qqq'
    testobj.parent().albumtype = 'studio'
    testobj.parent().sorttype = 'x'
    testobj.refresh_screen()
    assert capsys.readouterr().out == ('called Label.setText with arg `Lijst studio albums'
                                       ' - selectie: aaa contains "qqq" gesorteerd op x`\n'
                                       'called Label.setText with arg `concertopnamen`\n'
                                       'called Label.setText with arg `Kies een album'
                                       ' uit de lijst:`\n'
                                       'called Label.setText with arg `voer een nieuw album'
                                       ' op bij deze selectie`\n')
    testobj.parent().searchtype = 3
    testobj.parent().albumtype = 'studio'
    testobj.parent().sorttype = 'x'
    testobj.refresh_screen()
    assert capsys.readouterr().out == ('called Label.setText with arg `Lijst studio albums'
                                       ' - selectie: bbb contains "qqq" gesorteerd op x`\n'
                                       'called Label.setText with arg `Kies een album'
                                       ' uit de lijst:`\n'
                                       'called Label.setText with arg `voer een nieuw album'
                                       ' op bij deze selectie`\n')
    monkeypatch.setattr(testee, 'SELCOL', {'live': ['', '', 'aaa', 'bbb', 'ccc']})
    testobj.parent().searchtype = 4
    testobj.parent().albumtype = 'live'
    testobj.parent().sorttype = 'x'
    testobj.refresh_screen()
    assert capsys.readouterr().out == ('called Label.setText with arg `Lijst live concerten'
                                       ' - selectie: ccc contains "qqq" gesorteerd op x`\n'
                                       'called Label.setText with arg `studio albums`\n'
                                       'called Label.setText with arg `Kies een concert'
                                       ' uit de lijst:`\n'
                                       'called Label.setText with arg `voer een nieuw concert'
                                       ' op bij deze selectie`\n')
    assert capsys.readouterr().out == ''

def test_select_other_artist(monkeypatch, capsys):
    """unittest for albums_gui.Select.other_artist
    """
    def mock_index(self):
        """stub
        """
        print('called ComboBox.index')
    def mock_index_2(self):
        """stub
        """
        return 1
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index)
    testobj = setup_select(monkeypatch, capsys)
    testobj.ask_artist = mockqtw.MockComboBox()
    assert capsys.readouterr().out == 'called ComboBox.__init__\n'
    testobj.other_artist()
    assert capsys.readouterr().out == 'called ComboBox.index\n'
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', mock_index_2)
    testobj.parent().artist_ids = ['id1', 'id2']
    testobj.parent().artists = ['xxx', 'yyy']
    testobj.parent().searchtype = 1
    testobj.other_artist()
    assert testobj.parent().search_arg == 'id1'
    assert testobj.parent().artist == 'xxx'
    assert capsys.readouterr().out == 'called Main.do_select\n'
    testobj.parent().artist_ids = ['id1', 'id2']
    testobj.parent().artists = ['xxx', 'yyy']
    testobj.parent().searchtype = 0
    testobj.parent().artist = ''
    testobj.other_artist()
    assert testobj.parent().search_arg == 'id1'
    assert testobj.parent().artist == ''
    assert capsys.readouterr().out == 'called Main.do_select\n'

def test_select_other_search(monkeypatch, capsys):
    """unittest for albums_gui.Select.other_search
    """
    def mock_text(self):
        """stub
        """
        print('called LineEdit.text')
    def mock_text_2(self):
        """stub
        """
        return 'xxx'
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text)
    testobj = setup_select(monkeypatch, capsys)
    testobj.ask_zoekarg = mockqtw.MockLineEdit()
    assert capsys.readouterr().out == 'called LineEdit.__init__\n'
    testobj.other_search()
    assert capsys.readouterr().out == 'called LineEdit.text\n'
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_2)
    testobj.other_search()
    assert testobj.parent().search_arg == 'xxx'
    assert capsys.readouterr().out == 'called Main.do_select\n'

def test_select_other_albumtype(monkeypatch, capsys):
    """unittest for albums_gui.Select.other_albumtype
    """
    testobj = setup_select(monkeypatch, capsys)
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 5
    testobj.parent().old_seltype = 'old_value'
    testobj.other_albumtype()
    assert testobj.parent().albumtype == 'live'
    assert testobj.parent().searchtype == 4
    assert testobj.parent().old_seltype == 'old_value'
    assert capsys.readouterr().out == 'called Main.do_select\n'
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 2
    testobj.parent().old_seltype = 'old_value'
    testobj.other_albumtype()
    assert testobj.parent().albumtype == 'live'
    assert testobj.parent().searchtype == 'old_value'
    assert testobj.parent().old_seltype == 'old_value'
    assert capsys.readouterr().out == 'called Main.do_select\n'
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 'new_value'
    testobj.parent().old_seltype = 'old_value'
    testobj.other_albumtype()
    assert testobj.parent().albumtype == 'live'
    assert testobj.parent().searchtype == 'new_value'
    assert testobj.parent().old_seltype == 'old_value'
    assert capsys.readouterr().out == 'called Main.do_select\n'

    testobj.parent().albumtype = 'live'  # niet 'studio'
    testobj.parent().searchtype = 4
    testobj.parent().old_seltype = 'old_value'
    testobj.other_albumtype()
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().searchtype == 5
    assert testobj.parent().old_seltype == 'old_value'
    assert capsys.readouterr().out == 'called Main.do_select\n'
    testobj.parent().albumtype = 'live'  # niet 'studio'
    testobj.parent().searchtype = 2
    testobj.parent().old_seltype = 'old_value'
    testobj.other_albumtype()
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().searchtype == 2
    assert testobj.parent().old_seltype == 2
    assert capsys.readouterr().out == 'called Main.do_select\n'
    testobj.parent().albumtype = 'live'  # niet 'studio'
    testobj.parent().searchtype = 3
    testobj.parent().old_seltype = 'old_value'
    testobj.other_albumtype()
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().searchtype == 2
    assert testobj.parent().old_seltype == 3
    assert capsys.readouterr().out == 'called Main.do_select\n'
    testobj.parent().albumtype = 'live'  # niet 'studio'
    testobj.parent().searchtype = 'new_value'
    testobj.parent().old_seltype = 'old_value'
    testobj.other_albumtype()
    assert testobj.parent().albumtype == 'studio'
    assert testobj.parent().searchtype == 'new_value'
    assert testobj.parent().old_seltype == 'old_value'
    assert capsys.readouterr().out == 'called Main.do_select\n'

def test_select_todetail(monkeypatch, capsys):
    """unittest for albums_gui.Select.todetail
    """
    testobj = setup_select(monkeypatch, capsys)
    testobj.parent().albums = ['xxx', 'yyy']
    monkeypatch.setattr(testobj, 'sender', lambda *x: 'btn1')
    testobj.go_buttons = ['btn1', 'btn2']
    testobj.todetail()
    assert testobj.parent().album == 'xxx'
    assert capsys.readouterr().out == 'called Main.do_detail\n'
    testobj.parent().album = ''
    testobj.go_buttons = []
    testobj.todetail()
    assert not testobj.parent().album
    assert capsys.readouterr().out == 'waaat\ncalled Main.do_detail\n'
    monkeypatch.setattr(testobj, 'sender', lambda *x: 'btn')
    testobj.go_buttons = ['btn1', 'btn2']
    testobj.todetail()
    assert not testobj.parent().album
    assert capsys.readouterr().out == 'waaat\ncalled Main.do_detail\n'

def test_select_add_new_to_sel(monkeypatch, capsys):
    """unittest for albums_gui.Select.add_new_to_sel
    """
    testobj = setup_select(monkeypatch, capsys)
    testobj.add_new_to_sel()
    assert capsys.readouterr().out == "called Main.do_new with args {'keep_sel': True}\n"

def test_select_exit(monkeypatch, capsys):
    """unittest for albums_gui.Select.exit
    """
    testobj = setup_select(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


# Application details screen
def setup_detail(monkeypatch, capsys):
    """stub for setting up Detail object
    """
    def mock_init(self, parent):
        """stubzc
        """
        print('called Widget.__init__')
    def mock_setlayout(self, layout):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(layout).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.Detail(testparent)
    monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n'
                                       'called Widget.__init__\n')
    return testobj

def test_detail_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.Detail.create_widgets
    """
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
    monkeypatch.setattr(testee, 'newline', mock_newline)
    monkeypatch.setattr(testee, 'button_strip', mock_button_strip)
    monkeypatch.setattr(testee, 'exitbutton', mock_exitbutton)
    testobj = setup_detail(monkeypatch, capsys)
    testobj.parent().albums = [types.SimpleNamespace(name='xxx'), types.SimpleNamespace(name='yyy')]
    testobj.parent().albumdata = {'details': [('x', 'y'), ('a', 'b')],
                                  'tracks': {1: ['a', 'b', 'c'], 2: ['x', 'y', '']},
                                  'opnames': [['p', 'q'], ['r']]}
    testobj.create_widgets()
    bindings = {'other_album': testobj.other_album,
                'edit_alg': testobj.edit_alg,
                'edit_trk': testobj.edit_trk,
                'edit_rec': testobj.edit_rec,
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['detail'].format(**bindings)
    assert testobj.detailwins == []
    assert testobj.trackwins == []
    assert testobj.recwins == []

def test_detail_refresh_screen(monkeypatch, capsys):
    """unittest for albums_gui.Detail.refresh_screen
    """
    def mock_build(*args, **kwargs):
        """stub
        """
        print('called build_heading with args', args, kwargs)
        return 'heading'
    monkeypatch.setattr(testee, 'build_heading', mock_build)
    monkeypatch.setattr(testee, 'TYPETXT', {'x': 'item'})
    testobj = setup_detail(monkeypatch, capsys)
    testobj.heading = mockqtw.MockLabel()
    testobj.quickchange = mockqtw.MockLabel()
    testobj.subheading = mockqtw.MockLabel()
    assert capsys.readouterr().out == ('called Label.__init__\n'
                                       'called Label.__init__\n'
                                       'called Label.__init__\n')
    testobj.parent().albumtype = 'x'
    testobj.refresh_screen()
    assert capsys.readouterr().out == (f'called build_heading with args ({testobj},)'
                                       " {'readonly': True}\n"
                                       'called Label.setText with arg `heading`\n'
                                       'called Label.setText with arg'
                                       ' `Snel naar een ander item in deze selectie:`\n'
                                       'called Label.setText with arg `Itemgegevens:`\n')

def test_detail_other_album(monkeypatch, capsys):
    """unittest for albums_gui.Detail.other_album
    """
    testobj = setup_detail(monkeypatch, capsys)
    testobj.parent().albums = ['xxx']
    testobj.ask_album = mockqtw.MockComboBox()
    testobj.other_album()
    assert testobj.parent().album == 'xxx'
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called ComboBox.currentIndex\n'
                                       'called Main.do_detail\n')
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', lambda *x: 0)
    testobj.other_album()
    assert capsys.readouterr().out == ''

def test_detail_edit_alg(monkeypatch, capsys):
    """unittest for albums_gui.Detail.edit_alg
    """
    testobj = setup_detail(monkeypatch, capsys)
    testobj.edit_alg()
    assert capsys.readouterr().out == 'called Main.do_edit_alg\n'

def test_detail_edit_trk(monkeypatch, capsys):
    """unittest for albums_gui.Detail.edit_trk
    """
    testobj = setup_detail(monkeypatch, capsys)
    testobj.edit_trk()
    assert capsys.readouterr().out == 'called Main.do_edit_trk\n'

def test_detail_edit_rec(monkeypatch, capsys):
    """unittest for albums_gui.Detail.edit_rec
    """
    testobj = setup_detail(monkeypatch, capsys)
    testobj.edit_rec()
    assert capsys.readouterr().out == 'called Main.do_edit_rec\n'

def test_detail_exit(monkeypatch, capsys):
    """unittest for albums_gui.Detail.exit
    """
    testobj = setup_detail(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


# Application Details screen edit mode general part
def setup_edit(monkeypatch, capsys):
    """stub for setting up EditDetails object
    """
    def mock_init(self, parent):
        """stub
        """
        print('called Widget.__init__')
    def mock_setlayout(self, layout):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(layout).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.EditDetails(testparent)
    monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n'
                                       'called Widget.__init__\n')
    return testobj

def test_edit_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.EditDetails.create_widgets
    """
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
    monkeypatch.setattr(testee, 'newline', mock_newline)
    monkeypatch.setattr(testee, 'button_strip', mock_button_strip)
    monkeypatch.setattr(testee, 'exitbutton', mock_exitbutton)
    testobj = setup_edit(monkeypatch, capsys)
    testobj.parent().album = 2
    testobj.parent().albumtype = 'studio'  # of 'live'
    testobj.parent().albumdata = {'artist': 'xxx', 'titel': 'yyy',
                                  'details': [('Label/jaar:', 'lll'),
                                              ('Credits:', 'q')]}
    testobj.parent().artist_names = ['xxx', 'bbb']
    testobj.create_widgets()
    assert not testobj.new_album
    assert not testobj.keep_sel
    assert testobj.first_time
    # assert screendata == [(lbl, win), ...]
    # heading, bbox - deze hoeven niet
    bindings = {'other_album': 'testobj.other_album',
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['editdetails_studio'].format(**bindings)

    testobj.parent().albumdata = {'artist': 'xxx', 'titel': 'yyy',
                                  'details': [('Label/jaar:', 'lll, mmm'),
                                              ('Credits:', 'q')]}
    testobj.parent().artist_names = ['xxx', 'bbb']
    testobj.create_widgets()
    assert not testobj.new_album
    assert not testobj.keep_sel
    assert testobj.first_time
    # assert screendata == [(lbl, win), ...]
    # heading, bbox - deze hoeven niet
    bindings = {'other_album': 'testobj.other_album',
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['editdetails_studio'].format(**bindings)

    testobj.parent().album = 2
    testobj.parent().albumtype = 'live'
    testobj.parent().albumdata = {'artist': 'xxx', 'titel': 'yyy',
                                  'details': [('Bezetting:', 'rr'),
                                              ('Tevens met:', 'sss')]}
    testobj.parent().artist_names = ['xxx', 'bbb']
    testobj.create_widgets()
    assert not testobj.new_album
    assert not testobj.keep_sel
    assert testobj.first_time
    # assert screendata == [(lbl, win), ...]
    # heading, bbox - deze hoeven niet
    bindings = {'other_album': 'testobj.other_album',
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['editdetails_live'].format(**bindings)
    testobj.parent().album = 0
    testobj.parent().albumtype = 'studio'
    testobj.parent().search_arg = ''  # or any value
    testobj.parent().albumdata = {'artist': '', 'titel': '', 'details': []}
    testobj.create_widgets()
    assert not testobj.new_album
    assert not testobj.keep_sel
    assert testobj.first_time
    bindings = {'other_album': 'testobj.other_album',
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['editdetails_studio_nw'].format(**bindings)
    testobj.parent().album = 0
    testobj.parent().albumtype = 'live'
    testobj.parent().search_arg = 'x'
    testobj.parent().albumdata = {'artist': '', 'titel': '', 'details': []}
    testobj.create_widgets()
    assert not testobj.new_album
    assert not testobj.keep_sel
    assert testobj.first_time
    bindings = {'other_album': 'testobj.other_album',
                'exit': testobj.exit,
                'me': testobj}
    assert capsys.readouterr().out == expected_output['editdetails_live_nw'].format(**bindings)

def test_edit_new_data(monkeypatch, capsys):
    """unittest for albums_gui.EditDetails.new_data
    """
    testobj = setup_edit(monkeypatch, capsys)
    testobj.new_data()
    assert not testobj.keep_sel
    assert testobj.new_album
    assert testobj.albumnaam == ''
    assert testobj.album_names == []
    assert testobj.tracknames == []
    assert testobj.recordings == []
    assert testobj.edit_det
    assert not testobj.edit_trk
    assert not testobj.edit_rec
    assert capsys.readouterr().out == ''
    lbl1 = mockqtw.MockLabel('Uitvoerende:')
    win1 = mockqtw.MockComboBox()
    lbl2 = mockqtw.MockLabel('Albumtitel:')
    win2 = mockqtw.MockLineEdit()
    lbl3 = mockqtw.MockLabel('Locatie/datum:')
    win3 = mockqtw.MockLineEdit()
    lbl4 = mockqtw.MockLabel('Produced by:')
    win4 = mockqtw.MockLineEdit()
    lbl5 = mockqtw.MockLabel('Credits:')
    win5 = mockqtw.MockLineEdit()
    lbl6 = mockqtw.MockLabel('Bezetting:')
    win6 = mockqtw.MockLineEdit()
    assert capsys.readouterr().out == ("called Label.__init__ with args ('Uitvoerende:',)\n"
                                       "called ComboBox.__init__\n"
                                       "called Label.__init__ with args ('Albumtitel:',)\n"
                                       "called LineEdit.__init__\n"
                                       "called Label.__init__ with args ('Locatie/datum:',)\n"
                                       "called LineEdit.__init__\n"
                                       "called Label.__init__ with args ('Produced by:',)\n"
                                       "called LineEdit.__init__\n"
                                       "called Label.__init__ with args ('Credits:',)\n"
                                       "called LineEdit.__init__\n"
                                       "called Label.__init__ with args ('Bezetting:',)\n"
                                       "called LineEdit.__init__\n")
    testobj.screendata = [(lbl1, win1), (lbl2, win2), ()]
    testobj.parent().artist_ids = [0, 1, 2]
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 1
    testobj.parent().search_arg = types.SimpleNamespace(id=1)
    testobj.new_data(keep_sel=True)
    assert win1.currentIndex() == 2
    assert capsys.readouterr().out == ('called ComboBox.setCurrentIndex with arg `2`\n'
                                       'called ComboBox.currentIndex\n')
    testobj.screendata = [(lbl1, win1), (lbl2, win2), ()]
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 2
    testobj.parent().search_arg = 'search_arg'
    testobj.new_data(keep_sel=True)
    assert win2.text() == 'search_arg'
    assert capsys.readouterr().out == ('called LineEdit.setText with arg `search_arg`\n'
                                       'called LineEdit.text\n')
    testobj.screendata = [(lbl3, win3), (lbl4, win4), ()]
    testobj.parent().albumtype = 'live'
    testobj.parent().searchtype = 2
    testobj.new_data(keep_sel=True)
    assert win3.text() == 'search_arg'
    assert capsys.readouterr().out == ('called LineEdit.setText with arg `search_arg`\n'
                                       'called LineEdit.text\n')
    testobj.screendata = [(lbl3, win3), (lbl4, win4), ()]
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 3
    testobj.new_data(keep_sel=True)
    assert win4.text() == 'search_arg'
    assert capsys.readouterr().out == ('called LineEdit.setText with arg `search_arg`\n'
                                       'called LineEdit.text\n')
    testobj.screendata = [(lbl3, win3), (lbl4, win4), ()]
    testobj.parent().albumtype = 'live'
    testobj.parent().searchtype = 3
    testobj.new_data(keep_sel=True)
    assert win3.text() == 'search_arg'
    assert capsys.readouterr().out == ('called LineEdit.setText with arg `search_arg`\n'
                                       'called LineEdit.text\n')
    testobj.screendata = [(lbl5, win5), (lbl6, win6), ()]
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 4
    testobj.new_data(keep_sel=True)
    assert win5.text() == 'search_arg'
    assert capsys.readouterr().out == ('called LineEdit.setText with arg `search_arg`\n'
                                       'called LineEdit.text\n')
    testobj.screendata = [(lbl5, win5), (lbl6, win6), ()]
    testobj.parent().albumtype = 'live'
    testobj.parent().searchtype = 4
    testobj.new_data(keep_sel=True)
    assert win6.text() == 'search_arg'
    assert capsys.readouterr().out == ('called LineEdit.setText with arg `search_arg`\n'
                                       'called LineEdit.text\n')
    testobj.screendata = [(lbl5, win5), (lbl6, win6), ()]
    testobj.parent().albumtype = 'studio'
    testobj.parent().searchtype = 5
    testobj.new_data(keep_sel=True)
    assert win6.text() == 'search_arg'
    assert capsys.readouterr().out == ('called LineEdit.setText with arg `search_arg`\n'
                                       'called LineEdit.text\n')

def test_edit_refresh_screen(monkeypatch, capsys):
    """unittest for albums_gui.EditDetails.refresh_screen
    """
    def mock_itemat(num):
        """stub
        """
        if num == 0:
            return types.SimpleNamespace(widget=lambda: mockqtw.MockPushButton('X'))
        if num == 1:
            return types.SimpleNamespace(widget=lambda: None)
        return types.SimpleNamespace(widget=lambda: mockqtw.MockPushButton('Uitvoeren en terug'))
    monkeypatch.setattr(testee, 'build_heading', lambda *x: 'heading')
    testobj = setup_edit(monkeypatch, capsys)
    testobj.heading = mockqtw.MockLabel()
    testobj.first_time = True
    testobj.refresh_screen()
    assert capsys.readouterr().out == ('called Label.__init__\n'
                                       'called Label.setText with arg `heading`\n')
    testobj.bbox = mockqtw.MockHBoxLayout()
    assert capsys.readouterr().out == 'called HBox.__init__\n'
    monkeypatch.setattr(testobj.bbox, 'count', lambda *x: 3)
    monkeypatch.setattr(testobj.bbox, 'itemAt', mock_itemat)
    monkeypatch.setattr(testobj.parent(), 'do_detail', lambda *x: x)
    testobj.first_time = False
    testobj.refresh_screen()
    assert capsys.readouterr().out == (
            'called Label.setText with arg `heading`\n'
            "called PushButton.__init__ with args ('X',) {}\n"
            "called PushButton.text\n"
            "called PushButton.__init__ with args ('Uitvoeren en terug',) {}\n"
            "called PushButton.text\n"
            'called PushButton.setText with arg `Naar Details`\n'
            f'called Signal.connect with args ({testobj.parent().do_detail},)\n')
    # toevoeging t.b.v. full branch coverage
    monkeypatch.setattr(testobj.bbox, 'count', lambda *x: 0)
    testobj.refresh_screen()
    assert capsys.readouterr().out == 'called Label.setText with arg `heading`\n'

def test_edit_submit(monkeypatch, capsys):
    """unittest for albums_gui.EditDetails.submit
    """
    def mock_refresh():
        """stub
        """
        print('called EditDetails.refresh_screen')
    def mock_add():
        """stub
        """
        print('called EditDetails.add_another')
    def mock_replace(*args):
        """stub
        """
        print('called EditDetails._replace_details with args', args)
        return True
    def mock_update(*args):
        """stub
        """
        print('called dmla.update_album_details with args', args)
        return 'yy', True
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_edit(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    monkeypatch.setattr(testobj, '_replace_details', mock_replace)
    monkeypatch.setattr(testobj, 'add_another', mock_add)
    testobj.screendata = []
    testobj.first_time = True
    testobj.submit()
    assert not testobj.first_time
    assert capsys.readouterr().out == (f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Nothing changed`\n'
                                       'called EditDetails.refresh_screen\n')
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda *x: 'cb_text')
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentIndex', lambda *x: 2)
    monkeypatch.setattr(testee.dmla, 'update_album_details', mock_update)

    testobj.parent().albums = ['ww']
    testobj.parent().artists = ['aaa', 'bbb']
    testobj.new_album = False
    testobj.parent().albumdata = {'artist': 'x', 'titel': 'y'}
    testobj.parent().album = types.SimpleNamespace(id='xx')
    testobj.screendata = [(mockqtw.MockLabel('Uitvoerende:'), mockqtw.MockComboBox()),
                          (mockqtw.MockLabel('Albumtitel:'), mockqtw.MockLineEdit()),
                          (mockqtw.MockLabel('Label/jaar:'), mockqtw.MockLineEdit(),
                           mockqtw.MockLineEdit()),
                          (mockqtw.MockLabel('Credits:'), mockqtw.MockEditorWidget()),
                          (mockqtw.MockLabel('Bezetting:'), mockqtw.MockEditorWidget()),
                          (mockqtw.MockLabel('Tevens met:'), mockqtw.MockEditorWidget())]
    assert capsys.readouterr().out == ("called Label.__init__ with args ('Uitvoerende:',)\n"
                                       "called ComboBox.__init__\n"
                                       "called Label.__init__ with args ('Albumtitel:',)\n"
                                       "called LineEdit.__init__\n"
                                       "called Label.__init__ with args ('Label/jaar:',)\n"
                                       "called LineEdit.__init__\n"
                                       "called LineEdit.__init__\n"
                                       "called Label.__init__ with args ('Credits:',)\n"
                                       "called Editor.__init__\n"
                                       "called Label.__init__ with args ('Bezetting:',)\n"
                                       "called Editor.__init__\n"
                                       "called Label.__init__ with args ('Tevens met:',)\n"
                                       "called Editor.__init__\n")
    testobj.submit(goback=True)
    assert testobj.parent().albumdata['artist'] == testobj.parent().artist == 'bbb'
    assert testobj.parent().albumdata['titel'] == ''
    assert testobj.parent().album == 'yy'
    assert testobj.parent().albums == ['ww']
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called LineEdit.text\n'
                                       'called LineEdit.text\n'
                                       'called EditDetails._replace_details with args'
                                       " ('Label/jaar:', ', ')\n"
                                       'called Editor.toPlainText\n'
                                       'called EditDetails._replace_details with args'
                                       " ('Credits:', 'editor text')\n"
                                       'called Editor.toPlainText\n'
                                       'called EditDetails._replace_details with args'
                                       " ('Bezetting:', 'editor text')\n"
                                       'called Editor.toPlainText\n'
                                       'called EditDetails._replace_details with args'
                                       " ('Tevens met:', 'editor text')\n"
                                       "called dmla.update_album_details with args"
                                       " ('xx', {'artist': 'bbb', 'titel': ''})\n")

    testobj.parent().artists = ['aaa', 'bbb']
    testobj.new_album = False
    testobj.parent().albumdata = {'artist': 'x', 'titel': 'y'}
    testobj.parent().album = types.SimpleNamespace(id='xx')
    testobj.screendata = [(mockqtw.MockLabel('Uitvoerende:'), mockqtw.MockComboBox()),
                          (mockqtw.MockLabel('Albumtitel:'), mockqtw.MockLineEdit())]
    assert capsys.readouterr().out == ("called Label.__init__ with args ('Uitvoerende:',)\n"
                                       "called ComboBox.__init__\n"
                                       "called Label.__init__ with args ('Albumtitel:',)\n"
                                       "called LineEdit.__init__\n")
    testobj.submit()
    assert testobj.parent().albumdata['artist'] == testobj.parent().artist == 'bbb'
    assert testobj.parent().albumdata['titel'] == ''
    assert testobj.parent().album == 'yy'
    assert capsys.readouterr().out == (
            'called LineEdit.text\n'
            "called dmla.update_album_details with args ('xx', {'artist': 'bbb', 'titel': ''})\n"
            f'called MessageBox.information with args `{testobj}` `Albums` `Details updated`\n')

    testobj.parent().artists = ['aaa', 'bbb']
    testobj.parent().albums = ['xx']
    testobj.new_album = True
    testobj.parent().albumdata = {'artist': 'x', 'titel': 'y'}
    testobj.parent().album = types.SimpleNamespace(id='xx')
    testobj.screendata = [(mockqtw.MockLabel('Uitvoerende:'), mockqtw.MockComboBox()),
                          (mockqtw.MockLabel('Albumtitel:'), mockqtw.MockLineEdit())]
    assert capsys.readouterr().out == ("called Label.__init__ with args ('Uitvoerende:',)\n"
                                       "called ComboBox.__init__\n"
                                       "called Label.__init__ with args ('Albumtitel:',)\n"
                                       "called LineEdit.__init__\n")
    testobj.submit()
    assert testobj.parent().albumdata['artist'] == testobj.parent().artist == 'bbb'
    assert testobj.parent().albumdata['titel'] == ''
    assert testobj.parent().album == 'yy'
    assert testobj.parent().albums == ['xx', 'yy']
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       "called dmla.update_album_details with args"
                                       " (0, {'artist': 'bbb', 'titel': ''})\n"
                                       'called EditDetails.add_another\n')

    testobj.parent().artists = ['aaa', 'bbb']
    testobj.new_album = False
    testobj.parent().albumdata = {'artist': 'cb_text'}
    testobj.parent().album = types.SimpleNamespace(id='xx')
    testobj.screendata = [(mockqtw.MockLabel('Uitvoerende:'), mockqtw.MockComboBox())]
    assert capsys.readouterr().out == ("called Label.__init__ with args ('Uitvoerende:',)\n"
                                       "called ComboBox.__init__\n")
    testobj.submit(goback=True)
    assert capsys.readouterr().out == (f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Nothing changed`\n')

    testobj.parent().albumdata = {'titel': ''}
    testobj.parent().album = types.SimpleNamespace(id='xx')
    testobj.screendata = [(mockqtw.MockLabel('Locatie/datum:'), mockqtw.MockLineEdit())]
    assert capsys.readouterr().out == ("called Label.__init__ with args ('Locatie/datum:',)\n"
                                       "called LineEdit.__init__\n")
    testobj.submit(goback=True)
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Nothing changed`\n')

    testobj.parent().album = types.SimpleNamespace(id='xx')
    testobj.screendata = [(mockqtw.MockLabel('x:'), mockqtw.MockLineEdit())]
    assert capsys.readouterr().out == ("called Label.__init__ with args ('x:',)\n"
                                       "called LineEdit.__init__\n")
    testobj.submit(goback=True)
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called EditDetails._replace_details with args'
                                       " ('x:', '')\n"
                                       "called dmla.update_album_details with args"
                                       " ('xx', {'titel': ''})\n")

    monkeypatch.setattr(testee.dmla, 'update_album_details', lambda *x: ('', False))
    testobj.parent().artists = ['aaa', 'bbb']
    testobj.new_album = False
    testobj.parent().albumdata = {'artist': 'x', 'titel': 'y'}
    testobj.parent().album = types.SimpleNamespace(id='xx')
    testobj.screendata = [(mockqtw.MockLabel('Uitvoerende:'), mockqtw.MockComboBox()),
                          (mockqtw.MockLabel('Albumtitel:'), mockqtw.MockLineEdit())]
    assert capsys.readouterr().out == ("called Label.__init__ with args ('Uitvoerende:',)\n"
                                       "called ComboBox.__init__\n"
                                       "called Label.__init__ with args ('Albumtitel:',)\n"
                                       "called LineEdit.__init__\n")
    testobj.submit()
    assert testobj.parent().albumdata['artist'] == testobj.parent().artist == 'bbb'
    assert testobj.parent().albumdata['titel'] == ''
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Something went wrong, please try again`\n')

def test_edit_replace_details(monkeypatch, capsys):
    """unittest for albums_gui.EditDetails.replace_details
    """
    testobj = setup_edit(monkeypatch, capsys)
    original = {'details': []}
    testobj.parent().albumdata = original
    assert not testobj._replace_details('x', 'y')
    assert testobj.parent().albumdata == original
    original = {'details': [('x', 'y')]}
    testobj.parent().albumdata = original
    assert not testobj._replace_details('x', 'y')
    assert testobj.parent().albumdata == original
    original = {'details': [('x', 'y')]}
    testobj.parent().albumdata = original
    assert testobj._replace_details('x', 'z')
    assert testobj.parent().albumdata == {'details': [('x', 'z')]}
    # toevoeging t.b.v. full branch coverage
    testobj.parent().albumdata = original
    assert not testobj._replace_details('y', 'z')
    assert testobj.parent().albumdata == {'details': [('x', 'z')]}

def test_edit_add_another(monkeypatch, capsys):
    """unittest for albums_gui.EditDetails.add_another
    """
    def mock_create(win):
        """stub
        """
        print(f'called create_next_button with arg {type(win).__name__}')
    def mock_create_2(win):
        """stub
        """
        return 'button'
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee, 'create_next_button', mock_create)
    testobj = setup_edit(monkeypatch, capsys)
    testobj.keep_sel = True
    testobj.add_another()
    assert capsys.readouterr().out == ("called MessageBox.__init__ with args ("
                                       f"{mockqtw.MockMessageBox.information},"
                                       " 'Albums', 'Album added') {'buttons': 1,"
                                       f" 'parent': {testobj}}}\n"
                                       "called MessageBox.setDefaultButton with arg `1`\n"
                                       "called MessageBox.setEscapeButton with arg `1`\n"
                                       "called create_next_button with arg MockMessageBox\n"
                                       "called MessageBox.exec\n"
                                       "called MessageBox.clickedButton\n")
    monkeypatch.setattr(testee, 'create_next_button', mock_create_2)
    testobj.add_another()
    assert capsys.readouterr().out == ("called MessageBox.__init__ with args ("
                                       f"{mockqtw.MockMessageBox.information},"
                                       " 'Albums', 'Album added') {'buttons': 1,"
                                       f" 'parent': {testobj}}}\n"
                                       "called MessageBox.setDefaultButton with arg `1`\n"
                                       "called MessageBox.setEscapeButton with arg `1`\n"
                                       "called MessageBox.exec\n"
                                       "called MessageBox.clickedButton\n"
                                       "called Main.do_new with args {'keep_sel': True}\n")

def test_edit_submit_and_back(monkeypatch, capsys):
    """unittest for albums_gui.EditDetails.submit_and_back
    """
    def mock_submit(**kwargs):
        """stub
        """
        print('called EditDetails.submit with arg', kwargs)
    testobj = setup_edit(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'submit', mock_submit)
    testobj.first_time = True
    testobj.keep_sel = True
    testobj.submit_and_back()
    assert capsys.readouterr().out == ("called EditDetails.submit with arg {'goback': True}\n"
                                       "called Main.do_select\n")
    testobj.first_time = True
    testobj.keep_sel = False
    testobj.submit_and_back()
    assert capsys.readouterr().out == ("called EditDetails.submit with arg {'goback': True}\n"
                                       "called Main.do_start\n")
    testobj.first_time = False
    testobj.keep_sel = True
    testobj.submit_and_back()
    assert capsys.readouterr().out == ("called EditDetails.submit with arg {'goback': True}\n"
                                       "called Main.do_detail\n")

def test_edit_exit(monkeypatch, capsys):
    """unittest for albums_gui.EditDetails.exit
    """
    testobj = setup_edit(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


# Application Details screen edit mode tracks part
def setup_edittracks(monkeypatch, capsys):
    """stub for setting up EditTracks object
    """
    def mock_init(self, parent):
        """stub
        """
        print('called Widget.__init__')
    def mock_setlayout(self, layout):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(layout).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.EditTracks(testparent)
    monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n'
                                       'called Widget.__init__\n')
    return testobj

def test_edittracks_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.EditTracks.create_widgets
    """
    def mock_add(*args):
        """stub
        """
        print('called EditTracks.add_track_fields with args', args)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
    monkeypatch.setattr(testee, 'button_strip', mock_button_strip)
    monkeypatch.setattr(testee, 'exitbutton', mock_exitbutton)
    testobj = setup_edittracks(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'add_track_fields', mock_add)
    testobj.parent().albumdata = {'tracks': {}}
    testobj.parent().album = None
    testobj.parent().search_arg = ''
    testobj.create_widgets()
    assert testobj.first_time
    assert testobj.line == 1
    assert testobj.widgets == []
    assert testobj.tracks == 0
    bindings = {'me': testobj,
                'add_new_item': testobj.add_new_item,
                'exit': testobj.exit}
    assert capsys.readouterr().out == expected_output['edittracks'].format(**bindings)
    testobj.parent().albumdata = {'tracks': {}}
    testobj.parent().album = None
    testobj.parent().search_arg = 'x'
    testobj.create_widgets()
    assert testobj.line == 1
    assert testobj.widgets == []
    assert testobj.tracks == 0
    assert capsys.readouterr().out == expected_output['edittracks_2'].format(**bindings)
    testobj.parent().albumdata = {'tracks': {1: {'x': 'y'}, 2: {'a': 'b', 'c': 'd'}}}
    trackcount = len(testobj.parent().albumdata['tracks'])
    testobj.parent().album = 'x'
    testobj.parent().search_arg = ''
    testobj.create_widgets()
    assert testobj.line == 1      # ophogen wordt bij add_track_fields test geverifieerd
    assert testobj.widgets == []  # uitbreiden wordt bij add_track_fields test geverifieerd
    assert testobj.tracks == trackcount  # 2
    assert capsys.readouterr().out == expected_output['edittracks_3'].format(**bindings)

def test_edittracks_add_track_fields(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.EditTracks.add_track_fields
    """
    def mock_init(self, *args):
        """stub
        """
        print("called LineEdit.__init__ with args", args)
    def mock_init_2(self, *args):
        """stub
        """
        print("called Editor.__init__ with args", args)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(mockqtw.MockLineEdit, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    monkeypatch.setattr(mockqtw.MockEditorWidget, '__init__', mock_init_2)
    monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
    testobj = setup_edittracks(monkeypatch, capsys)
    testobj.gbox = mockqtw.MockGridLayout()
    assert capsys.readouterr().out == 'called Grid.__init__\n'
    testobj.widgets = []
    testobj.line = 0
    linecount = 2
    testobj.add_track_fields(1)
    assert testobj.line == linecount
    assert len(testobj.widgets) == 1
    assert isinstance(testobj.widgets[0][0], testee.qtw.QLineEdit)
    assert isinstance(testobj.widgets[0][1], testee.qtw.QLineEdit)
    assert isinstance(testobj.widgets[0][2], testee.qtw.QTextEdit)
    bindings = {'me': testobj, 'num': 1, 'text1': '', 'text2': '', 'text3': ''}
    assert capsys.readouterr().out == expected_output['edittracks_line'].format(**bindings)
    testobj.widgets = []
    testobj.line = 0
    testobj.add_track_fields(2, trackname='x', author='y', text='z')
    assert testobj.line == linecount
    assert len(testobj.widgets) == 1
    assert isinstance(testobj.widgets[0][0], testee.qtw.QLineEdit)
    assert isinstance(testobj.widgets[0][1], testee.qtw.QLineEdit)
    assert isinstance(testobj.widgets[0][2], testee.qtw.QTextEdit)
    bindings = {'me': testobj, 'num': 2, 'text1': 'x', 'text2': 'y', 'text3': 'z'}
    assert capsys.readouterr().out == expected_output['edittracks_line'].format(**bindings)

def test_edittracks_refresh_screen(monkeypatch, capsys):
    """unittest for albums_gui.EditTracks.refresh_screen
    """
    def mock_build_heading(win):
        """stub
        """
        print(f'called build_heading with arg `{win}`')
        return 'heading'
    def mock_settext(self, text):
        """stub
        """
        print(f'called Label.setText with arg `{text}`')
    monkeypatch.setattr(testee, 'build_heading', mock_build_heading)
    monkeypatch.setattr(mockqtw.MockLabel, 'setText', mock_settext)
    testobj = setup_edittracks(monkeypatch, capsys)
    testobj.heading = mockqtw.MockLabel()
    assert capsys.readouterr().out == 'called Label.__init__\n'
    testobj.refresh_screen()
    assert capsys.readouterr().out == (f'called build_heading with arg `{testobj}`\n'
                                       'called Label.setText with arg `heading`\n')

def test_edittracks_add_new_item(monkeypatch, capsys):
    """unittest for albums_gui.EditTracks.add_new_item
    """
    def mock_add(num):
        """stub
        """
        print(f'called Artists.add_track_fields with arg `{num}`')
    testobj = setup_edittracks(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'add_track_fields', mock_add)
    oldcount = 5
    testobj.tracks = oldcount
    testobj.scrl = mockqtw.MockScrolledWidget()
    testobj.bar = mockqtw.MockScrollBar()
    testobj.add_new_item()
    assert testobj.tracks == oldcount + 1  # 6
    assert capsys.readouterr().out == ('called ScrolledWidget.__init__\n'
                                       'called ScrollBar.__init__\n'
                                       'called Artists.add_track_fields with arg `6`\n'
                                       'called Scrollbar.maximum\n'
                                       'called Scrollbar.setMaximum with value `167`\n'
                                       'called Scrollbar.maximum\n'
                                       'called Scrollbar.setValue with value `99`\n')

def test_edittracks_submit(monkeypatch, capsys):
    """unittest for albums_gui.EditTracks.submit
    """
    def mock_refresh():
        """stub
        """
        print('called EditDetails.refresh_screen')
    def mock_update(*args):
        """stub
        """
        print('called dmla.update_album_tracks with args', args)
        return True
    monkeypatch.setattr(testee.dmla, 'update_album_tracks', mock_update)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_edittracks(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    testobj.widgets = []
    testobj.first_time = True
    testobj.submit()
    assert not testobj.first_time
    assert capsys.readouterr().out == (f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Nothing changed`\n'
                                       'called EditDetails.refresh_screen\n')
    testobj.widgets = [(mockqtw.MockLineEdit('', testobj), mockqtw.MockLineEdit('', testobj),
                        mockqtw.MockEditorWidget('', testobj))]
    assert capsys.readouterr().out == ('called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n'
                                       f"called Editor.__init__ with args ('', {testobj})\n")
    testobj.parent().albumdata = {'tracks': {}}
    testobj.parent().album = types.SimpleNamespace(id=1)
    testobj.submit()
    assert testobj.parent().albumdata == {'tracks': {}}
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called LineEdit.text\n'
                                       'called Editor.toPlainText\n'
                                       'called dmla.update_album_tracks with args'
                                       " (1, [(1, ('', '', 'editor text'))])\n"
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Tracks updated`\n')
    testobj.widgets = [(mockqtw.MockLineEdit('x', testobj), mockqtw.MockLineEdit('y', testobj),
                        mockqtw.MockEditorWidget('z', testobj))]
    assert capsys.readouterr().out == ('called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n'
                                       f"called Editor.__init__ with args ('z', {testobj})\n")
    testobj.parent().albumdata = {'tracks': {1: ('x', 'y', 'z')}}
    testobj.parent().album = types.SimpleNamespace(id=1)
    testobj.submit()
    assert testobj.parent().albumdata == {'tracks': {1: ('x', 'y', 'z')}}
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called LineEdit.text\n'
                                       'called Editor.toPlainText\n'
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Nothing changed`\n')
    testobj.parent().albumdata = {'tracks': {1: ('a', 'b', 'c')}}
    testobj.parent().album = types.SimpleNamespace(id=1)
    testobj.submit(skip_confirm=True)
    assert testobj.parent().albumdata == {'tracks': {1: ('x', 'y', 'z')}}
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called LineEdit.text\n'
                                       'called Editor.toPlainText\n'
                                       'called dmla.update_album_tracks with args'
                                       " (1, [(1, ('x', 'y', 'z'))])\n")
    testobj.parent().albumdata = {'tracks': {}}
    testobj.parent().album = types.SimpleNamespace(id=1)
    monkeypatch.setattr(testee.dmla, 'update_album_tracks', lambda *x: False)
    testobj.submit()
    assert testobj.parent().albumdata == {'tracks': {}}   # waarom verandert deze niet?
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called LineEdit.text\n'
                                       'called Editor.toPlainText\n'
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Something went wrong, please try again`\n')

def test_edittracks_submit_and_back(monkeypatch, capsys):
    """unittest for albums_gui.EditTracks.submit_and_back
    """
    def mock_submit(**kwargs):
        """stub
        """
        print('called EditTracks.submit with args', kwargs)
    testobj = setup_edittracks(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'submit', mock_submit)
    testobj.submit_and_back()
    assert capsys.readouterr().out == ("called EditTracks.submit with args {'skip_confirm': True}\n"
                                       'called Main.do_detail\n')

def test_edittracks_exit(monkeypatch, capsys):
    """unittest for albums_gui.EditTracks.exit
    """
    testobj = setup_edittracks(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


# Application Details screen edit mode recordings part
def setup_editrecs(monkeypatch, capsys):
    """stub for setting up EditRecordings object
    """
    def mock_init(self, parent):
        """stub
        """
        print('called Widget.__init__')
    def mock_setlayout(self, layout):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(layout).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.EditRecordings(testparent)
    monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n'
                                       'called Widget.__init__\n')
    return testobj

def test_editrecs_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.EditRecordings.create_widgets
    """
    def mock_add(*args):
        """stub
        """
        print('called EditRecordings.add_track_fields with args', args)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
    monkeypatch.setattr(testee, 'button_strip', mock_button_strip)
    monkeypatch.setattr(testee, 'exitbutton', mock_exitbutton)
    testobj = setup_editrecs(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'add_rec_fields', mock_add)
    testobj.parent().albumdata = {'opnames': {}}
    testobj.parent().album = None
    testobj.parent().search_arg = ''
    testobj.create_widgets()
    assert testobj.first_time
    assert testobj.recwins == []
    assert testobj.recs == 0
    bindings = {'me': testobj,
                'add_new_item': testobj.add_new_item,
                'exit': testobj.exit}
    assert capsys.readouterr().out == expected_output['editrecs'].format(**bindings)
    testobj.parent().albumdata = {'opnames': {}}
    testobj.parent().album = None
    testobj.parent().search_arg = 'x'
    testobj.create_widgets()
    assert testobj.recwins == []
    assert testobj.recs == 0
    assert capsys.readouterr().out == expected_output['editrecs_2'].format(**bindings)
    testobj.parent().albumdata = {'opnames': [(1, ('x', 'y')), (2, ('a', 'b'))]}
    reccount = len(testobj.parent().albumdata['opnames'])
    testobj.parent().album = 'x'
    testobj.parent().search_arg = ''
    testobj.create_widgets()
    assert testobj.recwins == []  # uitbreiden wordt bij add_track_fields test geverifieerd
    assert testobj.recs == reccount  # 2
    assert capsys.readouterr().out == expected_output['editrecs_3'].format(**bindings)

def test_editrecs_add_rec_fields(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.EditRecordings.add_rec_fields
    """
    def mock_init(self, *args):
        """stub
        """
        print("called LineEdit.__init__ with args", args)
    def mock_init_2(self, *args):
        """stub
        """
        print("called TextEdit.__init__ with args", args)
    monkeypatch.setattr(testee, 'RECTYPES', ('x', 'y', 'z'))
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(mockqtw.MockLineEdit, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    testobj = setup_editrecs(monkeypatch, capsys)
    testobj.vbox2 = mockqtw.MockVBoxLayout()
    assert capsys.readouterr().out == 'called VBox.__init__\n'
    testobj.recwins = []
    testobj.add_rec_fields(1)
    assert len(testobj.recwins) == 1
    assert isinstance(testobj.recwins[0][0], testee.qtw.QComboBox)
    assert isinstance(testobj.recwins[0][1], testee.qtw.QLineEdit)
    bindings = {'me': testobj, 'num': 2, 'text': '', 'insertpos': -1}
    assert capsys.readouterr().out == expected_output['editrecs_line'].format(**bindings)
    testobj.recwins = []
    testobj.add_rec_fields(2, opname=('x', 'y'))
    assert len(testobj.recwins) == 1
    assert isinstance(testobj.recwins[0][0], testee.qtw.QComboBox)
    assert isinstance(testobj.recwins[0][1], testee.qtw.QLineEdit)
    bindings = {'me': testobj, 'num': 3, 'text': 'y', 'insertpos': 0}
    assert capsys.readouterr().out == expected_output['editrecs_line_2'].format(**bindings)

def test_editrecs_refresh_screen(monkeypatch, capsys):
    """unittest for albums_gui.EditRecordings.refresh_screen
    """
    def mock_build_heading(win):
        """stub
        """
        print(f'called build_heading with arg `{win}`')
        return 'heading'
    def mock_settext(self, text):
        """stub
        """
        print(f'called Label.setText with arg `{text}`')
    monkeypatch.setattr(testee, 'build_heading', mock_build_heading)
    monkeypatch.setattr(mockqtw.MockLabel, 'setText', mock_settext)
    testobj = setup_editrecs(monkeypatch, capsys)
    testobj.heading = mockqtw.MockLabel()
    assert capsys.readouterr().out == 'called Label.__init__\n'
    testobj.refresh_screen()
    assert capsys.readouterr().out == (f'called build_heading with arg `{testobj}`\n'
                                       'called Label.setText with arg `heading`\n')

def test_editrecs_add_new_item(monkeypatch, capsys):
    """unittest for albums_gui.EditRecordings.add_new_item
    """
    def mock_add(num):
        """stub
        """
        print(f'called Artists.add_rec_fields with arg `{num}`')
    testobj = setup_editrecs(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'add_rec_fields', mock_add)
    oldcount = 5
    testobj.recs = oldcount
    testobj.scrl = mockqtw.MockScrolledWidget()
    testobj.bar = mockqtw.MockScrollBar()
    testobj.add_new_item()
    assert testobj.recs == oldcount + 1  # 6
    assert capsys.readouterr().out == ('called ScrolledWidget.__init__\n'
                                       'called ScrollBar.__init__\n'
                                       'called Artists.add_rec_fields with arg `6`\n'
                                       'called Scrollbar.maximum\n'
                                       'called Scrollbar.setMaximum with value `135`\n'
                                       'called Scrollbar.maximum\n'
                                       'called Scrollbar.setValue with value `99`\n')

# 1275->1278
def test_editrecs_submit(monkeypatch, capsys):
    """unittest for albums_gui.EditRecordings.submit
    """
    def mock_refresh():
        """stub
        """
        print('called EditDetails.refresh_screen')
    def mock_update(*args):
        """stub
        """
        print('called dmla.update_album_recordings with args', args)
        return True
    monkeypatch.setattr(testee.dmla, 'update_album_recordings', mock_update)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_editrecs(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    testobj.recwins = []
    testobj.first_time = True
    testobj.submit()
    assert not testobj.first_time
    assert capsys.readouterr().out == (f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Nothing changed`\n'
                                       'called EditDetails.refresh_screen\n')
    testobj.recwins = [(mockqtw.MockComboBox(testobj), mockqtw.MockLineEdit('', testobj))]
    testobj.recwins[0][0].setCurrentText('')
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.setCurrentText with arg ``\n')
    testobj.parent().albumdata = {'opnames': []}  #
    testobj.parent().album = types.SimpleNamespace(id=1)
    testobj.submit()
    assert testobj.parent().albumdata == {'opnames': []}
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called LineEdit.text\n'
                                       'called dmla.update_album_recordings with args'
                                       " (1, [(0, ('current text', ''))])\n"
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Recordings updated`\n')
    testobj.recwins = [(mockqtw.MockComboBox(testobj), mockqtw.MockLineEdit('y', testobj))]
    newvalue = 'x'
    testobj.recwins[0][0].setCurrentText(newvalue)
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called ComboBox.setCurrentText with arg `x`\n')
    monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda *x: newvalue)
    testobj.parent().albumdata = {'opnames': [('x', 'y')]}
    testobj.parent().album = types.SimpleNamespace(id=1)
    testobj.submit()
    assert testobj.parent().albumdata == {'opnames': [('x', 'y')]}
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Nothing changed`\n')
    testobj.submit(skip_confirm=True)
    assert testobj.parent().albumdata == {'opnames': [('x', 'y')]}
    assert capsys.readouterr().out == 'called LineEdit.text\n'
    testobj.parent().albumdata = {'opnames': [('a', 'b')]}
    testobj.parent().album = types.SimpleNamespace(id=1)
    testobj.submit(skip_confirm=True)
    assert testobj.parent().albumdata == {'opnames': [('x', 'y')]}
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called dmla.update_album_recordings with args'
                                       " (1, [(0, ('x', 'y'))])\n")
    testobj.parent().albumdata = {'opnames': []}
    testobj.parent().album = types.SimpleNamespace(id=1)
    monkeypatch.setattr(testee.dmla, 'update_album_recordings', lambda *x: False)
    testobj.submit()
    assert testobj.parent().albumdata == {'opnames': []}
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       f'called MessageBox.information with args `{testobj}`'
                                       ' `Albums` `Something went wrong, please try again`\n')

def test_editrecs_submit_and_back(monkeypatch, capsys):
    """unittest for albums_gui.EditRecordings.submit_and_back
    """
    def mock_submit(**kwargs):
        """stub
        """
        print('called EditRecordings.submit with args', kwargs)
    testobj = setup_editrecs(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'submit', mock_submit)
    testobj.submit_and_back()
    assert capsys.readouterr().out == ("called EditRecordings.submit with args"
                                       " {'skip_confirm': True}\n"
                                       'called Main.do_detail\n')

def test_editrecs_exit(monkeypatch, capsys):
    """unittest for albums_gui.EditRecordings.exit
    """
    testobj = setup_editrecs(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


# Application Artists (list) screen
def setup_artists(monkeypatch, capsys):
    """stub for setting up Artist object
    """
    def mock_init(self, parent):
        """stub
        """
        print('called Widget.__init__')
    def mock_setlayout(self, layout):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(layout).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.Artists(testparent)
    monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called Main.__init__\n'
                                       'called Application.__init__\n'
                                       'called Widget.__init__\n')
    return testobj

def test_artists_create_widgets(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.Artists.create_widgets
    """
    def mock_add(*args):
        """stub
        """
        print('called Artists.add_artist_line with args', args)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
    monkeypatch.setattr(testee, 'button_strip', mock_button_strip)
    monkeypatch.setattr(testee, 'exitbutton', mock_exitbutton)
    testobj = setup_artists(monkeypatch, capsys)
    testobj.parent().artist_filter = 'xxx'
    artist1 = types.SimpleNamespace(id=1, first_name='a', last_name='b')
    artist2 = types.SimpleNamespace(id=3, first_name='b', last_name='a')
    artist3 = types.SimpleNamespace(id=2, first_name='x', last_name='y')
    testobj.parent().artists = [artist1, artist2, artist3]
    artistcount = len(testobj.parent().artists)
    monkeypatch.setattr(testobj, 'add_artist_line', mock_add)
    testobj.create_widgets()
    assert testobj.artist_list == [artist1, artist2, artist3]
    assert testobj.last_artistid == artistcount
    bindings = {'testobj': testobj,
                'filter': testobj.filter,
                'exit': testobj.exit}
    assert capsys.readouterr().out == expected_output['artists'].format(**bindings)
    testobj.parent().artists = []
    testobj.create_widgets()
    assert testobj.artist_list == []
    assert testobj.last_artistid == 0
    assert capsys.readouterr().out == expected_output['artists_2'].format(**bindings)

def test_artists_filter(monkeypatch, capsys):
    """unittest for albums_gui.Artists.filter
    """
    def mock_list(arg):
        """stub
        """
        print(f'called dmla.list_artists with arg `{arg}`')
        return ['x', 'z']
    testobj = setup_artists(monkeypatch, capsys)
    monkeypatch.setattr(testee.dmla, 'list_artists', mock_list)
    testobj.ask_filter = mockqtw.MockLineEdit('..')
    assert capsys.readouterr().out == 'called LineEdit.__init__\n'
    testobj.parent().all_artists = ['x', 'y', 'z']
    testobj.filter()
    assert testobj.parent().artists == ['x', 'z']
    assert testobj.parent().artist_filter == '..'
    assert capsys.readouterr().out == ('called LineEdit.text\n'
                                       'called dmla.list_artists with arg `..`\n'
                                       'called Main.do_select\n')
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda *x: '')
    testobj.ask_filter = mockqtw.MockLineEdit()
    assert capsys.readouterr().out == 'called LineEdit.__init__\n'
    testobj.filter()
    assert testobj.parent().artists == ['x', 'y', 'z']
    assert testobj.parent().artist_filter == ''
    assert capsys.readouterr().out == 'called Main.do_select\n'

def test_artists_add_artist_line(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.Artists.add_artist_line
    """
    def mock_init(self, *args):
        """stub
        """
        print("called LineEdit.__init__ with args", args)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(mockqtw.MockLineEdit, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    testobj = setup_artists(monkeypatch, capsys)
    testobj.vbox2 = mockqtw.MockVBoxLayout()
    assert capsys.readouterr().out == "called VBox.__init__\n"
    testobj.fields = []
    testobj.add_artist_line(1)
    assert len(testobj.fields) == 1
    assert isinstance(testobj.fields[0][0], testee.qtw.QLineEdit)
    assert isinstance(testobj.fields[0][1], testee.qtw.QLineEdit)
    bindings = {'testobj': testobj, 'num': 1, 'text1': '', 'text2': ''}
    assert capsys.readouterr().out == expected_output['artist_line'].format(**bindings)
    testobj.fields = []
    testobj.add_artist_line(2, first_name='x', last_name='y')
    assert len(testobj.fields) == 1
    assert isinstance(testobj.fields[0][0], testee.qtw.QLineEdit)
    assert isinstance(testobj.fields[0][1], testee.qtw.QLineEdit)
    bindings = {'testobj': testobj, 'num': 2, 'text1': 'x', 'text2': 'y'}
    assert capsys.readouterr().out == expected_output['artist_line'].format(**bindings)

def test_artists_refresh_screen():
    """unittest for albums_gui.Artists.refresh_screen

    method-to-test is empty
    """

# 1373->1369
def test_artists_submit(monkeypatch, capsys):
    """unittest for albums_gui.Artists.submit
    """
    def mock_update(*args):
        """stub
        """
        print('called dmla.update_artists with args', args)
        return True
    # monkeypatch.setattr(testee.core.Qt.CursorShape, 'WaitCursor', 'waitcursor')
    monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
    monkeypatch.setattr(testee.dmla, 'update_artists', mock_update)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_artists(monkeypatch, capsys)
    testobj.fields = ()
    testobj.submit()
    assert capsys.readouterr().out == (
            f'called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n'
            'called Application.setOverrideCursor with arg MockCursor\n'
            f'called MessageBox.information with args `{testobj}` `Albums` `Nothing changed`\n'
            'called Application.restoreOverrideCursor\n'
            'called Main.get_all_artists\n'
            'called Main.do_select\n')
    testobj.parent().artists = ()
    testobj.fields = [(mockqtw.MockLineEdit('x'), mockqtw.MockLineEdit('y'))]
    assert capsys.readouterr().out == ('called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n')
    testobj.submit()
    assert capsys.readouterr().out == (
            f'called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n'
            'called Application.setOverrideCursor with arg MockCursor\n'
            'called LineEdit.text\n'
            'called LineEdit.text\n'
            "called dmla.update_artists with args ([(0, 'x', 'y')],)\n"
            'called Application.restoreOverrideCursor\n'
            'called Main.get_all_artists\n'
            'called Main.do_select\n')
    testobj.parent().artists = [types.SimpleNamespace(id=1, first_name='a', last_name='b')]
    testobj.fields = [(mockqtw.MockLineEdit('x'), mockqtw.MockLineEdit('y'))]
    assert capsys.readouterr().out == ('called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n')
    testobj.submit()
    assert capsys.readouterr().out == (
            f'called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n'
            'called Application.setOverrideCursor with arg MockCursor\n'
            'called LineEdit.text\n'
            'called LineEdit.text\n'
            "called dmla.update_artists with args ([(1, 'x', 'y')],)\n"
            'called Application.restoreOverrideCursor\n'
            'called Main.get_all_artists\n'
            'called Main.do_select\n')
    # toevoeging t.b.v. full branch coverage
    testobj.parent().artists = [types.SimpleNamespace(id=1, first_name='a', last_name='b')]
    testobj.fields = [(mockqtw.MockLineEdit('a'), mockqtw.MockLineEdit('b'))]
    assert capsys.readouterr().out == ('called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n')
    testobj.submit()
    assert capsys.readouterr().out == (
            f'called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n'
            'called Application.setOverrideCursor with arg MockCursor\n'
            'called LineEdit.text\n'
            'called LineEdit.text\n'
            f'called MessageBox.information with args `{testobj}` `Albums` `Nothing changed`\n'
            'called Application.restoreOverrideCursor\n'
            'called Main.get_all_artists\n'
            'called Main.do_select\n')

def test_artists_new(monkeypatch, capsys):
    """unittest for albums_gui.Artists.new
    """
    def mock_add(num):
        """stub
        """
        print(f'called Artists.add_artist_line with arg `{num}`')
    testobj = setup_artists(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'add_artist_line', mock_add)
    highest = 5
    testobj.last_artistid = highest
    testobj.scrl = mockqtw.MockScrolledWidget()
    testobj.bar = mockqtw.MockScrollBar()
    testobj.new()
    assert testobj.last_artistid == highest + 1  # 6
    assert capsys.readouterr().out == ('called ScrolledWidget.__init__\n'
                                       'called ScrollBar.__init__\n'
                                       'called Artists.add_artist_line with arg `6`\n'
                                       'called Scrollbar.maximum\n'
                                       'called Scrollbar.setMaximum with value `133`\n'
                                       'called Scrollbar.maximum\n'
                                       'called Scrollbar.setValue with value `99`\n')

def test_artists_exit(monkeypatch, capsys):
    """unittest for albums_gui.Artists.exit
    """
    testobj = setup_artists(monkeypatch, capsys)
    testobj.exit()
    assert capsys.readouterr().out == 'called Main.close\n'


# New Artist Dialog
def test_artistdialog(monkeypatch, capsys, expected_output):
    """unittest for albums_gui.ArtistDialog
    """
    def mock_init(self, *args):
        """stub
        """
        print('called Widget.__init__')
    def mock_setLayout(self, widget):
        """stub
        """
        print(f'called Widget.setLayout with arg {type(widget).__name__}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setLayout)
    monkeypatch.setattr(testee.qtw, 'QDialog', mockqtw.MockDialog)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    testobj = testee.NewArtistDialog(testee.qtw.QWidget())
    bindings = {'reject': testobj.reject, 'update': testobj.update, 'testobj': testobj}
    assert capsys.readouterr().out == expected_output['artist_dialog'].format(**bindings)

def test_artistdialog_update(monkeypatch, capsys):
    """unittest for albums_gui.ArtistDialog.update
    """
    def mock_init(self, *args):
        """stub
        """
        print('called NewArtistDialog.__init__')
    def mock_accept(self, *args):
        """stub
        """
        print('called NewArtistDialog.accept')
    counter = 0
    def mock_text(*args):
        """stub
        """
        nonlocal counter
        counter += 1
        print('QLineEdit returns', ('', 'x', 'y')[counter])
    class mock_object:
        """stub
        """
        def save(self):
            """stub
            """
            print('called my.Act.save')
    monkeypatch.setattr(testee.NewArtistDialog, '__init__', mock_init)
    monkeypatch.setattr(testee.NewArtistDialog, 'accept', mock_accept)
    testobj = testee.NewArtistDialog()
    assert capsys.readouterr().out == 'called NewArtistDialog.__init__\n'
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text)
    testobj.first_name = mockqtw.MockLineEdit()
    testobj.last_name = mockqtw.MockLineEdit()
    assert capsys.readouterr().out == ('called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n')
    monkeypatch.setattr(testee.dmla.my.Act.objects, 'create', lambda *x: mock_object())
    testobj.update()
    assert capsys.readouterr().out == ('QLineEdit returns x\n'
                                       'QLineEdit returns y\n'
                                       'called my.Act.save\n'
                                       'called NewArtistDialog.accept\n')
