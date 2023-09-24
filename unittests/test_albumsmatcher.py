import types
import pytest
import apps.albumsmatcher as testee
import unittests.mockqtwidgets as mockqtw
from unittests.buildscreen_output_fixture import expected_output


# mock implementations of application classes
class MockMainFrame:
    next_icon = 'next_icon'  # nog even geen mockqtw.MockIcon()
    prev_icon = 'prev_icon'  # idem
    def __init__(self):
        print('called MainFrame.__init__')
        self.app = mockqtw.MockApplication()
        self.title = 'appname'
        self.artist_map = {}
        self.albums_map = {}


class MockNewArtistDialog:
    def __init__(self, parent, name):
        print('called NewArtistDialog.__init__'
              f' with parent of type `{type(parent)}` and name `{name}`')
    def exec_(self):
        return testee.qtw.QDialog.Rejected


class MockNewAlbumDialog:
    def __init__(self, parent, name, year):
        print('called NewAlbumDialog.__init__'
              f' with parent of type `{type(parent)}` and name `{name}`, year `{year}`')
    def exec_(self):
        return testee.qtw.QDialog.Rejected


class MockCmpArt:
    def __init__(self, arg):
        print(f'called CompareArtists.__init__ with arg `{arg}`')


class MockCmpAlb:
    def __init__(self, arg):
        print(f'called CompareAlbums.__init__ with arg `{arg}`')


class MockCmpTrk:
    def __init__(self, arg):
        print(f'called CompareTracks.__init__ with arg `{arg}`')


# tests for module level functions
def test_build_artist_name():
    assert testee.build_artist_name('', '') == ''
    assert testee.build_artist_name('', 'y') == 'y'
    assert testee.build_artist_name('x', '') == ', x'
    assert testee.build_artist_name('x', 'y') == 'y, x'


def test_build_album_name():
    def mock_text(arg):
        if arg == 0:
            return 'x'
        if arg == 1:
            return 'y'
    assert testee.build_album_name(types.SimpleNamespace(text=mock_text)) == 'x (y)'
    assert testee.build_album_name(types.SimpleNamespace(name='x', release_year='y')) == 'x (y)'
    assert testee.build_album_name(types.SimpleNamespace(name='x', release_year='')) == 'x'
    assert testee.build_album_name(types.SimpleNamespace(name='', release_year='y')) == ' (y)'
    assert testee.build_album_name(types.SimpleNamespace(name='', release_year='')) == ''


def test_save_appdata(monkeypatch, capsys, tmp_path):
    def mock_copy(*args):
        print('called shutil.copyfile with args', args)
    def mock_copy_2(*args):
        raise FileNotFoundError
    def mock_open(self, *args):
        print(f'called {self}.open with args', args)
        return open(str(self), *args)
    def mock_dump(*args):
        print('called json.dump with args', args)
    tmpfile = tmp_path / 'fname'
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee.json, 'dump', mock_dump)
    monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
    monkeypatch.setattr(testee, 'FNAME', tmpfile)
    testee.save_appdata('appdata')
    assert capsys.readouterr().out == ('called shutil.copyfile with args'
                                       f" ('{tmpfile}', '{tmpfile}.bak')\n"
                                       f"called {tmpfile}.open with args ('w',)\n"
                                       "called json.dump with args ('appdata', "
                                       f"<_io.TextIOWrapper name='{tmpfile}' mode='w'"
                                       " encoding='UTF-8'>)\n")
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy_2)
    testee.save_appdata('appdata')
    assert capsys.readouterr().out == (f"called {tmpfile}.open with args ('w',)\n"
                                       "called json.dump with args ('appdata', "
                                       f"<_io.TextIOWrapper name='{tmpfile}' mode='w'"
                                       " encoding='UTF-8'>)\n")


def test_load_appdata(monkeypatch, capsys, tmp_path):
    def mock_open(self, *args):
        print(f'called {self}.open with args', args)
        return open(str(self), *args)
    def mock_load(*args):
        print('called json.load with args', args)
        return 'appdata'
    tmpfile = tmp_path / 'fname'
    monkeypatch.setattr(testee.json, 'load', mock_load)
    monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
    monkeypatch.setattr(testee, 'FNAME', tmpfile)
    assert testee.load_appdata() is None
    assert capsys.readouterr().out == f"called {tmpfile}.open with args ()\n"
    tmpfile.touch()
    assert testee.load_appdata() == 'appdata'
    assert capsys.readouterr().out == (f"called {tmpfile}.open with args ()\n"
                                       f"called json.load with args (<_io.TextIOWrapper"
                                       f" name='{tmpfile}' mode='r' encoding='UTF-8'>,)\n")


def test_read_artists(monkeypatch, capsys):
    def mock_lista(*args):
        print('called dmla.list_artists with args', args)
        return [types.SimpleNamespace(first_name='x', last_name='y', id=1),
                types.SimpleNamespace(first_name='a', last_name='b', id=2)]
    def mock_listc(*args):
        print('called dmlc.list_artists with args', args)
        return [{'artist': 'x'}, {'artist': 'y'}]
    monkeypatch.setattr(testee.dmla, 'list_artists', mock_lista)
    monkeypatch.setattr(testee.dmlc, 'list_artists', mock_listc)
    assert testee.read_artists() == ([('x', 'y', '1'), ('a', 'b', '2')], ['x', 'y'])
    assert capsys.readouterr().out == ('called dmla.list_artists with args ()\n'
                                       'called dmlc.list_artists with args ()\n')


def test_update_artists(monkeypatch, capsys):
    def mock_list():
        print('called dmla.list_artists')
        return [types.SimpleNamespace(id=1), types.SimpleNamespace(id=2)]
    def mock_update(*args):
        print('called dmla.update_artists with args', args)
        return [types.SimpleNamespace(id=3, first_name='x', last_name='y '),
                types.SimpleNamespace(id=4, first_name='a', last_name='b')]
    monkeypatch.setattr(testee.dmla, 'list_artists', mock_list)
    monkeypatch.setattr(testee.dmla, 'update_artists', mock_update)
    result = testee.update_artists([('4', 'q', 'r'), ('7', 'x', 'y ')])
    assert result == {'x y': 3}
    assert capsys.readouterr().out == ("called dmla.list_artists\n"
                                       "called dmla.update_artists with args"
                                       " ([(0, 'q', 'r'), (0, 'x', 'y ')],)\n")


def test_read_artist_albums(monkeypatch, capsys):
    def mock_list_a_albums(*args):
        print('called dmla.list_albums_by_artist with args', args)
        return [types.SimpleNamespace(id='1', name='x', release_year=2),
                types.SimpleNamespace(id='2', name='a', release_year='b')]
    def mock_list_c_albums(*args):
        print('called dmlc.list_albums with args', args)
        return [{'album': 'q', 'year': 'r'}, {'album': 'a', 'year': 'b'}]
    monkeypatch.setattr(testee.dmla, 'list_albums_by_artist', mock_list_a_albums)
    monkeypatch.setattr(testee.dmlc, 'list_albums', mock_list_c_albums)
    result = testee.read_artist_albums('9', 'x x')
    assert result == ([('x', '2', '1'), ('a', 'b', '2')], [('q', 'r'), ('a', 'b')])
    assert capsys.readouterr().out == ("called dmla.list_albums_by_artist with args"
                                       " ('', '9', 'Jaar')\n"
                                       "called dmlc.list_albums with args ('x x',)\n")


def test_read_albums_tracks(monkeypatch, capsys):
    def mock_list_a_tracks(*args):
        print('called dmla.list_tracks with args', args)
        return [types.SimpleNamespace(name='x'), types.SimpleNamespace(name='a')]
    def mock_list_c_tracks(*args):
        print('called dmlc.list_tracks_for_album with args', args)
        return [{'track': 1, 'title': 'r'}, {'track': 2, 'title': 'b'}]
    monkeypatch.setattr(testee.dmla, 'list_tracks', mock_list_a_tracks)
    monkeypatch.setattr(testee.dmlc, 'list_tracks_for_album', mock_list_c_tracks)
    result = testee.read_album_tracks('9', 'x x', 'yyy')
    assert result == (['x', 'a'], ['r', 'b'])
    assert capsys.readouterr().out == ("called dmla.list_tracks with args ('9',)\n"
                                       "called dmlc.list_tracks_for_album with args ('x x', 'yyy')\n")


def test_popuptext(monkeypatch, capsys):
    def mock_text(num):
        print(f'called item.text with arg `{num}`')
        return f'text for {num}'
    def mock_text_2(num):
        print(f'called item.text with arg `{num}`')
        if num == 2:
            return ''
        return f'text for {num}'
    def mock_set(*args):
        print('called item.setToolTip with args', args)
    item = types.SimpleNamespace(text=mock_text, setToolTip=mock_set)
    testee.popuptext(item, 0)
    assert capsys.readouterr().out == 'called item.text with arg `2`\n'
    item = types.SimpleNamespace(text=mock_text, setToolTip=mock_set)
    testee.popuptext(item, 1)
    assert capsys.readouterr().out == ('called item.text with arg `2`\n'
                                       'called item.text with arg `1`\n'
                                       "called item.setToolTip with args (1, 'text for 1')\n")
    item = types.SimpleNamespace(text=mock_text, setToolTip=mock_set)
    testee.popuptext(item, 2)
    assert capsys.readouterr().out == 'called item.text with arg `2`\n'
    item = types.SimpleNamespace(text=mock_text_2, setToolTip=mock_set)
    testee.popuptext(item, 0)
    assert capsys.readouterr().out == ('called item.text with arg `2`\n'
                                       'called item.text with arg `0`\n'
                                       "called item.setToolTip with args (0, 'text for 0')\n")
    item = types.SimpleNamespace(text=mock_text_2, setToolTip=mock_set)
    testee.popuptext(item, 1)
    assert capsys.readouterr().out == 'called item.text with arg `2`\n'
    item = types.SimpleNamespace(text=mock_text_2, setToolTip=mock_set)
    testee.popuptext(item, 2)
    assert capsys.readouterr().out == 'called item.text with arg `2`\n'


def test_wait_cursor(monkeypatch, capsys):
    monkeypatch.setattr(testee.core.Qt, 'WaitCursor', 'waitcursor')
    monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
    win = types.SimpleNamespace(app=mockqtw.MockApplication())
    assert capsys.readouterr().out == "called QApplication.__init__\n"
    with testee.wait_cursor(win):  # testen als contextmanager
        pass
    assert capsys.readouterr().out == ("called QCursor with arg waitcursor\n"
                                       "called app.setOverrideCursor with arg of type"
                                       " <class 'unittests.mockqtwidgets.MockCursor'>\n"
                                       "called app.restoreOverrideCursor\n")


# tests for main application class
def setup_main(monkeypatch, capsys):
    monkeypatch.setattr(testee.MainFrame, '__init__', MockMainFrame.__init__)
    testobj = testee.MainFrame()
    assert capsys.readouterr().out == ('called MainFrame.__init__\n'
                                       'called QApplication.__init__\n')
    return testobj

def test_main_init(monkeypatch, capsys, expected_output):
    def mock_app_init(self, *args):
        print('called QApplication._init__')
    def mock_init(self, *args):
        print('called QMainWindow._init__ with args', args)
    def mock_check(self):
        print('called MainFrame.check_for_data')
        return ['x', 'y'], ['a', 'b']
    def mock_settabs(self):
        print('called MainFrame.settabs')
        return ['page1', 'page2']
    def mock_go(self, arg):
        print(f'called MainFrame.go with arg `{arg}`')
    monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QMainWindow, 'move', mockqtw.MockMainWindow.move)
    monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
    monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                        mockqtw.MockMainWindow.setWindowTitle)
    monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                        mockqtw.MockMainWindow.setCentralWidget)
    monkeypatch.setattr(testee.qtw.QMainWindow, 'addAction', mockqtw.MockMainWindow.addAction)
    monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
    monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
    monkeypatch.setattr(testee.qtw, 'QTabWidget', mockqtw.MockTabWidget)
    monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBox)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    monkeypatch.setattr(testee.qtw, 'QAction', mockqtw.MockAction)
    monkeypatch.setattr(testee.MainFrame, 'check_for_data', mock_check)
    monkeypatch.setattr(testee.MainFrame, 'setup_tabwidget', mock_settabs)
    monkeypatch.setattr(testee.MainFrame, 'go', mock_go)
    testobj = testee.MainFrame()
    assert isinstance(testobj.app, testee.qtw.QApplication)
    assert testobj.title == 'AlbumsMatcher'
    assert testobj.current == -1
    assert not testobj.not_again
    bindings = {'me': testobj, 'parent': None, 'page_changed': testobj.page_changed,
                'exit': testobj.exit, 'app': None}
    assert capsys.readouterr().out == expected_output['matcher_main'].format(**bindings)

    testobj = testee.MainFrame(parent='parent')
    assert isinstance(testobj.app, testee.qtw.QApplication)
    assert testobj.title == 'AlbumsMatcher'
    assert testobj.current == -1
    assert not testobj.not_again
    bindings = {'me': testobj, 'parent': "'parent'", 'page_changed': testobj.page_changed,
                'exit': testobj.exit, 'app': None}
    assert capsys.readouterr().out == expected_output['matcher_main'].format(**bindings)

    testobj = testee.MainFrame(app='app')
    assert testobj.app == 'app'
    assert testobj.title == 'AlbumsMatcher'
    assert testobj.current == -1
    assert not testobj.not_again
    bindings = {'me': testobj, 'parent': None, 'page_changed': testobj.page_changed,
                'exit': testobj.exit, 'app': 'app'}
    assert capsys.readouterr().out == expected_output['matcher_main_w_app'].format(**bindings)

def test_main_go(monkeypatch, capsys):
    testobj = setup_main(monkeypatch, capsys)
    testobj.go('app')
    assert capsys.readouterr().out == ''
    with pytest.raises(SystemExit):
        testobj.go('')
    assert capsys.readouterr().out == 'called QApplication.exec_\n'

def test_main_check_for_data(monkeypatch, capsys):
    counter = 0
    def mock_load():
        nonlocal counter
        if counter:
            print('called load_appdata') # negeren tijdens __init__
        counter += 1
        return 'x', 'y'
    monkeypatch.setattr(testee, 'load_appdata', mock_load)
    testobj = setup_main(monkeypatch, capsys)
    assert testobj.check_for_data() == ('x', 'y')
    monkeypatch.setattr(testee, 'load_appdata', lambda: None)
    testobj = setup_main(monkeypatch, capsys)
    assert testobj.check_for_data() == ({}, {})

def test_main_setup_tabwidget(monkeypatch, capsys):
    monkeypatch.setattr(testee, 'CompareArtists', MockCmpArt)
    monkeypatch.setattr(testee, 'CompareAlbums', MockCmpAlb)
    monkeypatch.setattr(testee, 'CompareTracks', MockCmpTrk)
    testobj = setup_main(monkeypatch, capsys)
    testobj.nb = mockqtw.MockTabWidget()
    result = testobj.setup_tabwidget()
    assert len(result) == 3
    names = ['artists', 'albums', 'tracks']
    classes = [testee.CompareArtists, testee.CompareAlbums, testee.CompareTracks]
    for ix, item in enumerate(result.values()):
        assert item[0] == names[ix]
        assert isinstance(item[1], classes[ix])
        assert item[1].first_time
        assert item[1]._parent == testobj
    assert capsys.readouterr().out == ('called QTabWidget.__init__\n'
                                       f'called CompareArtists.__init__ with arg `{testobj}`\n'
                                       f'called CompareAlbums.__init__ with arg `{testobj}`\n'
                                       f'called CompareTracks.__init__ with arg `{testobj}`\n'
                                       f"called QTabWidget.addTab with args ({result[0][1]},"
                                       " 'Artists')\n"
                                       f"called QTabWidget.addTab with args ({result[1][1]},"
                                       " 'Albums')\n"
                                       f"called QTabWidget.addTab with args ({result[2][1]},"
                                       " 'Tracks')\n")

def test_main_page_changed(monkeypatch, capsys):
    def mock_check(page):
        print(f'called Main.check_oldpage with arg `{page}`')
        return True
    def mock_current():
        print('called QTabWidget.currentWidget')
        return types.SimpleNamespace(first_time=True, create_widgets=mock_createw,
                                     create_actions=mock_createa, refresh_screen=mock_refresh)
    def mock_current_2():
        print('called QTabWidget.currentWidget')
        return types.SimpleNamespace(first_time=False, create_widgets=mock_createw,
                                     create_actions=mock_createa, refresh_screen=mock_refresh_2)
    def mock_createw():
        print('called subscreen.create_widgets')
    def mock_createa():
        print('called subscreen.create_actions')
    def mock_refresh(arg):
        print(f'called subscreen.refresh_screen with arg `{arg}`')
    def mock_refresh_2(arg):
        return 'message'
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_main(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'check_oldpage', mock_check)
    testobj.nb = mockqtw.MockTabWidget()
    monkeypatch.setattr(testobj.nb, 'currentWidget', mock_current)
    assert capsys.readouterr().out == 'called QTabWidget.__init__\n'
    testobj.current = 0
    testobj.current_data = 'current data'
    testobj.not_again = True
    testobj.page_changed()
    assert not testobj.not_again
    assert capsys.readouterr().out == ''

    testobj.current = 1
    testobj.not_again = False
    testobj.page_changed()
    assert capsys.readouterr().out == ('called Main.check_oldpage with arg `1`\n'
                                       'called QTabWidget.currentIndex\n'
                                       'called QTabWidget.currentWidget\n'
                                       'called subscreen.create_widgets\n'
                                       'called subscreen.create_actions\n'
                                       'called subscreen.refresh_screen with arg `current data`\n')

    testobj.current = 1
    monkeypatch.setattr(testobj, 'check_oldpage', lambda *x: False)
    testobj.page_changed()
    assert testobj.not_again
    assert capsys.readouterr().out == 'called QTabWidget.setCurrentIndex with arg `1`\n'

    testobj.current = -1
    monkeypatch.setattr(testobj.nb, 'currentWidget', mock_current_2)
    testobj.page_changed()
    assert capsys.readouterr().out == ('called QTabWidget.currentIndex\n'
                                       'called QTabWidget.currentWidget\n'
                                       'called QMessageBox.information with args'
                                       ' `appname` `message`\n'
                                       'called QTabWidget.setCurrentIndex with arg `0`\n')

def test_main_check_oldpage(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_main(monkeypatch, capsys)
    testobj.pages = {0: ('', types.SimpleNamespace(modified=True)),
                     1: ('', types.SimpleNamespace(modified=True)),
                     2: ('', types.SimpleNamespace(modified=True)),
                     }
    for ix in range(2):
        assert not testobj.check_oldpage(ix)
        assert capsys.readouterr().out == ('called QMessageBox.information with args'
                                           f' `appname` `{testee.checkpage_messages[ix]}`\n')
    testobj.pages = {0: ('', types.SimpleNamespace(modified=False))}
    assert testobj.check_oldpage(0)
    assert capsys.readouterr().out == ''

def test_main_exit(monkeypatch, capsys):
    def mock_check(page):
        print(f'called Main.check_oldpage with arg `{page}`')
        return True
    def mock_close():
        print(f'called Main.close')
    testobj = setup_main(monkeypatch, capsys)
    testobj.current = 1
    monkeypatch.setattr(testobj, 'check_oldpage', mock_check)
    monkeypatch.setattr(testobj, 'close', mock_close)
    testobj.exit()
    assert capsys.readouterr().out == ('called Main.check_oldpage with arg `1`\n'
                                       'called Main.close\n')
    monkeypatch.setattr(testobj, 'check_oldpage', lambda *x: False)
    assert capsys.readouterr().out == ''


# tests for Compare Artists Tab
def setup_cmpart(monkeypatch, capsys, widgets=True):
    def mock_init(self, parent):
        print('called QWidget.__init__')
        self._parent = parent
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    testparent = MockMainFrame()
    testobj = testee.CompareArtists(testparent)
    # we gebruiken hier _parent dus dit is niet nodig
    # monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    output = 'called MainFrame.__init__\ncalled QApplication.__init__\ncalled QWidget.__init__\n'
    if widgets:
        testobj.clementine_artists = mockqtw.MockTree()
        testobj.albums_artists = mockqtw.MockTree()
        output += 'called QTreeWidget.__init__\ncalled QTreeWidget.__init__\n'
    assert capsys.readouterr().out == output
    return testobj

def test_cmpart_create_widgets(monkeypatch, capsys, expected_output):
    def mock_setlayout(layout):
        print(f'called QWidget.setLayout with arg of type {type(layout)}')
    def mock_popup():
        pass
    def mock_select():
        pass
    def mock_check():
        pass
    def focus_next():
        pass
    def focus_prev():
        pass
    def mock_find():
        pass
    def mock_delete():
        pass
    def mock_save():
        pass
    testobj = setup_cmpart(monkeypatch, capsys, widgets=False)
    monkeypatch.setattr(testobj, 'setLayout', mock_setlayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTree)
    monkeypatch.setattr(testee.qtw, 'QHeaderView', mockqtw.MockHeader)
    monkeypatch.setattr(testee.core, 'QSize', mockqtw.MockSize)
    monkeypatch.setattr(testee, 'popuptext', mock_popup)
    monkeypatch.setattr(testobj, 'select_and_go', mock_select)
    monkeypatch.setattr(testobj, 'check_deletable', mock_check)
    monkeypatch.setattr(testobj, 'find_artist', mock_find)
    monkeypatch.setattr(testobj, 'delete_artist', mock_delete)
    monkeypatch.setattr(testobj, 'save_all', mock_save)
    # breakpoint()
    testobj.create_widgets()
    assert testobj.appname == 'appname'
    bindings = {'me': testobj, 'popuptext': mock_popup, 'select_and_go': mock_select,
                'check_deletable': mock_check, 'help': testobj.help,
                'focus_next': testobj.focus_next, 'focus_prev': testobj.focus_prev,
                'find_artist': mock_find, 'delete_artist': mock_delete, 'save_all': mock_save}
    assert capsys.readouterr().out == expected_output['compare_artists'].format(**bindings)

def test_cmpart_create_actions(monkeypatch, capsys, expected_output):
    def mock_add(arg):
        print(f'called CompareArtists.addAction')
    monkeypatch.setattr(testee.qtw, 'QAction', mockqtw.MockAction)
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'addAction', mock_add)
    testobj.clementine_artists = mockqtw.MockTree()
    testobj.create_actions()
    bindings = {'me': testobj,
                'help': testobj.help,
                'setfocus': testobj.clementine_artists.setFocus,
                'find_artist': testobj.find_artist,
                'select_and_go': testobj.select_and_go,
                'focus_next': testobj.focus_next,
                'focus_prev': testobj.focus_prev,
                'delete_artist': testobj.delete_artist,
                'save_all': testobj.save_all}
    assert capsys.readouterr().out == expected_output['compare_artists_actions'].format(**bindings)

def test_cmpart_refresh_screen(monkeypatch, capsys, expected_output):
    def mock_read():
        print('called read_artists')
        return [('x', 'y ', '1'), ('a', 'b', '2')], ['xx', 'yy']
    def mock_focus(arg):
        print(f'called focus_artist with arg `{arg}`')
    def mock_set(value):
        print(f'called set_modified with arg `{value}`')
    monkeypatch.setattr(testee, 'read_artists', mock_read)
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'focus_artist', mock_focus)
    monkeypatch.setattr(testobj, 'set_modified', mock_set)
    # testobj._parent.artist_map = {}
    testobj.refresh_screen()
    assert testobj.new_artists == []
    assert testobj.new_matches == {}
    assert testobj.lookup == {'x y': '1', 'a b': '2'}
    assert testobj.finda == {'1': ('x', 'y '), '2': ('a', 'b')}
    assert testobj.artist_map == {'xx': '', 'yy': ''}
    assert testobj.max_artist == 2
    assert testobj.artist_buffer == ''
    assert capsys.readouterr().out == expected_output['compare_artists_refresh_1']

    # unittest failt als niet alles uit clementine in artist_map zit
    # testobj._parent.artist_map = {'qq': '1', 'yy': '2'}
    testobj._parent.artist_map = {'qq': '1', 'yy': '2', 'xx': ''}
    testobj.refresh_screen('artist')
    assert testobj.new_artists == []
    assert testobj.new_matches == {}
    assert testobj.lookup == {'x y': '1', 'a b': '2'}
    assert testobj.finda == {'1': ('x', 'y '), '2': ('a', 'b')}
    # assert testobj.artist_map == {'xx': '1', 'yy': '2'}
    assert testobj.artist_map == {'qq': '1', 'yy': '2', 'xx': ''}
    assert testobj.max_artist == 2
    assert testobj.artist_buffer == ''
    assert capsys.readouterr().out == expected_output['compare_artists_refresh_2']

def test_cmpart_set_modified(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.save_button = mockqtw.MockButton('')
    assert capsys.readouterr().out == "called PushButton.__init__ with args ('',)\n"
    testobj.set_modified(True)
    assert testobj.modified
    assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `True`\n'
    testobj.set_modified(False)
    assert not testobj.modified
    assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `False`\n'

def test_cmpart_focus_artist(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)

    monkeypatch.setattr(testee.core.Qt, 'MatchFixedString', 1)
    testobj.focus_artist('artist')
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       "called QTreeWidget.findItems with args ('artist', 1, 0)\n"
                                       'called QTreeWidget.setCurrentItem with arg'
                                       ' `TreeWidget.topLevelItem with index 0`\n')

    monkeypatch.setattr(testobj.clementine_artists , 'findItems', lambda *x: ['xx'])
    testobj.focus_artist()
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       'called QTreeWidget.setCurrentItem with arg `xx`\n')

def test_cmpart_focus_next(monkeypatch, capsys):
    def mock_focus(**kwargs):
        print('called CompareArtists.focus_item with args', kwargs)
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'focus_item', mock_focus)
    testobj.focus_next()
    assert capsys.readouterr().out == 'called CompareArtists.focus_item with args {}\n'

def test_cmpart_focus_prev(monkeypatch, capsys):
    def mock_focus(**kwargs):
        print('called CompareArtists.focus_item with args', kwargs)
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'focus_item', mock_focus)
    testobj.focus_prev()
    assert capsys.readouterr().out == ("called CompareArtists.focus_item with args"
                                       " {'forward': False}\n")

def test_cmpart_focus_item(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj.clementine_artists, 'currentIndex',
                        lambda: types.SimpleNamespace(row=lambda: 0))
    monkeypatch.setattr(testee.core.Qt, 'MatchFixedString', 1)
    testobj.focus_item()
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       "called QTreeWidget.findItems with args ('', 1, 1)\n"
                                       'called QMessageBox.information with args'
                                       ' `appname` `No more unmatched items this way`\n')
    monkeypatch.setattr(testobj.clementine_artists, 'findItems', lambda *x: ['xx'])
    monkeypatch.setattr(testobj.clementine_artists, 'indexFromItem',
                        lambda x: types.SimpleNamespace(row=lambda: 0))
    testobj.focus_item()
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       'called QMessageBox.information with args'
                                       ' `appname` `No more unmatched items this way`\n')
    currentindex = types.SimpleNamespace(row=lambda: 1)
    monkeypatch.setattr(testobj.clementine_artists, 'indexFromItem',
                        lambda *x: currentindex)
    testobj.focus_item()
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       "called QTreeWidget.setCurrentItem with arg `xx`\n"
                                       "called QTreeWidget.setCurrentIndex with arg"
                                       f" `{currentindex}`\n")
    monkeypatch.setattr(testobj.clementine_artists, 'indexFromItem',
                        lambda x: types.SimpleNamespace(row=lambda: 1))
    testobj.focus_item(forward=False)
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       'called QMessageBox.information with args'
                                       ' `appname` `No more unmatched items this way`\n')
    monkeypatch.setattr(testobj.clementine_artists, 'currentIndex',
                        lambda: types.SimpleNamespace(row=lambda: 1))
    currentindex = types.SimpleNamespace(row=lambda: 0)
    monkeypatch.setattr(testobj.clementine_artists, 'indexFromItem',
                        lambda *x: currentindex)
    testobj.focus_item(forward=False)
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       "called QTreeWidget.setCurrentItem with arg `xx`\n"
                                       "called QTreeWidget.setCurrentIndex with arg"
                                       f" `{currentindex}`\n")

def test_cmpart_check_deletable(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.delete_button = mockqtw.MockButton('')
    assert capsys.readouterr().out == "called PushButton.__init__ with args ('',)\n"
    testobj.new_artists = []
    testobj.check_deletable()
    assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `False`\n'
    # item = mockqtw.MockTreeItem('x')
    testobj.new_artists = ['TreeWidget.currentItem']
    # monkeypatch.setattr(testobj.albums_artists, 'currentItem', lambda *x: item)
    testobj.check_deletable()
    assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `True`\n'

def test_cmpart_select_and_go(monkeypatch, capsys):
    def mock_current():
        print('called QTreeWidget.currentItem')
        return None
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj._parent.nb = mockqtw.MockTabWidget()
    currentitem = mockqtw.MockTreeItem('x', 'y', 'z')
    assert capsys.readouterr().out == ('called QTabWidget.__init__\n'
                                       "called QTreeWidgetItem.__init__ with args ('x', 'y', 'z')\n")
    monkeypatch.setattr(testobj.clementine_artists, 'currentItem', mock_current)
    testobj.select_and_go()
    assert capsys.readouterr().out == 'called QTreeWidget.currentItem\n'
    monkeypatch.setattr(testobj.clementine_artists, 'currentItem', lambda *x: currentitem)
    testobj.artist_map = {'x': ''}
    testobj.appname = 'appname'
    testobj.select_and_go()
    assert capsys.readouterr().out == ("called QTreeWidgetItem.text for col 0\n"
                                       "called QMessageBox.information with args"
                                       " `appname` `Not possible - artist hasn't been matched yet`\n")
    testobj.artist_map = {'x': 'y'}
    testobj.select_and_go()
    assert testobj._parent.current_data == 'x'
    assert capsys.readouterr().out == ('called QTreeWidgetItem.text for col 0\n'
                                       'called QTabWidget.setCurrentIndex with arg `1`\n')

def test_cmpart_find_artist(monkeypatch, capsys):
    def mock_add():
        print('called CompareArtists.add_artist')
    def mock_text(arg):
        print(f'called currentItem.text with arg `{arg}`')
        return 'some_text'
    def mock_update(*args):
        print('called CompareArtists.update_item with args', args)
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.appname = 'appname'
    monkeypatch.setattr(testobj, 'determine_search_arg_and_find', lambda *x: '')
    monkeypatch.setattr(testobj, 'filter_matched', lambda *x: ([], []))
    monkeypatch.setattr(testobj, 'update_item', mock_update)
    monkeypatch.setattr(testobj, 'add_artist', mock_add)
    monkeypatch.setattr(testobj.clementine_artists, 'currentItem', lambda: None)
    testobj.find_artist()
    assert capsys.readouterr().out == ''

    testobj.artist_map = {'some_text': ''}  # ook kijken wat er gebeurt als ik een KeyError toesta
    curr_item = types.SimpleNamespace(text=mock_text)
    monkeypatch.setattr(testobj.clementine_artists, 'currentItem', lambda: curr_item)
    testobj.find_artist()
    assert testobj._parent.current_data == 'some_text'
    assert capsys.readouterr().out == ('called currentItem.text with arg `0`\n'
                                       'called CompareArtists.add_artist\n')

    testobj.artist_map = {'some_text': 'x'}
    testobj.find_artist()
    assert testobj._parent.current_data == 'some_text'
    assert testobj.artist_map == {'some_text': 'x'}
    assert capsys.readouterr().out == ('called currentItem.text with arg `0`\n'
                                       'called QMessageBox.question with args `appname`'
                                       ' `Artist already has a match - do you want to reassign?`'
                                       ' `12` `8`\n')

    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', lambda *x: mockqtw.MockMessageBox.Yes)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testobj, 'determine_search_arg_and_find', lambda *x: '1')
    testobj.artist_map = {'some_text': 'x'}
    monkeypatch.setattr(testee.core.Qt, 'MatchFixedString', 1)
    monkeypatch.setattr(testobj.albums_artists, 'findItems', lambda *x: ['xx'])
    testobj.find_artist()
    assert testobj._parent.current_data == 'some_text'
    assert testobj.artist_map == {'some_text': ''}
    assert capsys.readouterr().out == ('called currentItem.text with arg `0`\n'
                                       'called InputDialog.getItem with args'
                                       " ('appname', 'Select Artist', []) {'editable': False}\n"
                                       'called CompareArtists.add_artist\n')
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', lambda *x, **y: ('y', True))
    item_a = types.SimpleNamespace(text=lambda x: ['c', 'd', 'e'][x])
    item_b = types.SimpleNamespace(text=lambda x: ['f', 'g', 'h'][x])
    monkeypatch.setattr(testobj, 'filter_matched', lambda *x: (['x', 'y'], [item_a, item_b]))
    testobj.find_artist()
    assert testobj._parent.current_data == 'some_text'
    assert testobj.artist_map == {'some_text': ''}
    assert capsys.readouterr().out == ('called currentItem.text with arg `0`\n'
                                       "called CompareArtists.update_item with args (" +
                                       repr(item_b) + ', ' + repr(curr_item) + ')\n')

def test_cmpart_determine_search_arg(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.lookup = {'y': 'z'}
    # assert testobj.determine_search_arg('') is False
    assert testobj.determine_search_arg_and_find('x, y') == 'z'
    assert testobj.determine_search_arg_and_find('y') == 'z'
    testobj.lookup = {'q': 'z'}
    assert testobj.determine_search_arg_and_find('y') is False
    testobj.lookup = {'x': 'z'}
    assert testobj.determine_search_arg_and_find('x, y') is False

def test_cmpart_filter_matched(monkeypatch, capsys):
    def mock_text(arg):
        print(f'called TreeItem.text with arg `{arg}`')
        return {0: 'text_0', 1: 'text_1', 2: 'text_2'}[arg]
    def mock_text_2(arg):
        return {0: 'text_0', 1: 'text_1', 2: 'q'}[arg]
    monkeypatch.setattr(testee, 'build_artist_name', lambda x, y: f'{x} - {y}')
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.artist_map = {'x': 'y', 'p': 'q'}
    search_item = types.SimpleNamespace(text=mock_text)
    assert testobj.filter_matched([search_item]) == (['text_0 - text_1'], [search_item])
    assert capsys.readouterr().out == ('called TreeItem.text with arg `2`\n'
                                       'called TreeItem.text with arg `0`\n'
                                       'called TreeItem.text with arg `1`\n')
    search_item = types.SimpleNamespace(text=mock_text_2)
    assert testobj.filter_matched([search_item]) == ([], [])

def test_cmpart_update_item(monkeypatch, capsys):
    def mock_set(arg):
        print(f'called CompareArtists.set_modified to {arg}')
    mockitem = mockqtw.MockTreeItem('x')
    assert capsys.readouterr().out == "called QTreeWidgetItem.__init__ with args ('x',)\n"
    def mock_itembelow(arg):
        print(f'called TreeWidget.itemBelow with arg {arg}')
        return mockitem
    mockcurrent = mockqtw.MockTreeItem('y')
    assert capsys.readouterr().out == "called QTreeWidgetItem.__init__ with args ('y',)\n"
    def mock_current():
        print(f'called TreeWidget.currentItem')
        return mockcurrent
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'set_modified', mock_set)
    from_item = mockqtw.MockTreeItem('a', 'b', 'c')
    new_item = mockqtw.MockTreeItem('x', 'y', 'z')
    testobj.artist_map = {}
    testobj.new_matches = {}
    assert capsys.readouterr().out == ("called QTreeWidgetItem.__init__ with args ('a', 'b', 'c')\n"
                                       "called QTreeWidgetItem.__init__ with args ('x', 'y', 'z')\n")
    monkeypatch.setattr(testobj.clementine_artists, 'itemBelow', mock_itembelow)
    monkeypatch.setattr(testobj.clementine_artists, 'currentItem', mock_current)
    testobj.update_item(new_item, from_item)
    assert capsys.readouterr().out == (f'called QTreeWidget.setCurrentItem with arg `{new_item}`\n'
                                       f'called QTreeWidget.scrollToItem with arg `{new_item}`\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called QTreeWidgetItem.setText to `X for col 1\n'
                                       'called CompareArtists.set_modified to True\n'
                                       "called TreeWidget.currentItem\n"
                                       f'called TreeWidget.itemBelow with arg {mockcurrent}\n'
                                       f'called QTreeWidget.setCurrentItem with arg `{mockitem}`\n')
    monkeypatch.setattr(testobj.clementine_artists, 'itemBelow', lambda *x: None)
    testobj.update_item(new_item, from_item)
    assert capsys.readouterr().out == (f'called QTreeWidget.setCurrentItem with arg `{new_item}`\n'
                                       f'called QTreeWidget.scrollToItem with arg `{new_item}`\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called QTreeWidgetItem.setText to `X for col 1\n'
                                       'called CompareArtists.set_modified to True\n'
                                       "called TreeWidget.currentItem\n")

def test_cmpart_copy_artist(monkeypatch, capsys):
    assert capsys.readouterr().out == ''
    testobj = setup_cmpart(monkeypatch, capsys)
    item = mockqtw.MockTreeItem('x')
    assert capsys.readouterr().out == "called QTreeWidgetItem.__init__ with args ('x',)\n"
    monkeypatch.setattr(testobj.albums_artists, 'currentItem', lambda *x: item)
    testobj.copy_artist()
    assert testobj.artist_buffer == 'TreeWidget.currentItem'
    assert capsys.readouterr().out == ''

def test_cmpart_add_artist(monkeypatch, capsys):
    def mock_finditems_yes(*args):
        print("called QTreeWidget.findItems with args", args)
        return ['x']
    def mock_finditems_no(*args):
        print("called QTreeWidget.findItems with args", args)
        return []
    mock_data = types.SimpleNamespace(text=lambda y: str(y))
    def mock_finditems_data(*args):
        print("called QTreeWidget.findItems with args", args)
        return [mock_data]
    def mock_update(*args):
        print('called CompareArtists.update_item with args', args)
    def mock_build(*args):
        print('called build_artist_name with args', args)
        return ', '.join(args)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
    monkeypatch.setattr(testee, 'NewArtistDialog', MockNewArtistDialog)
    monkeypatch.setattr(testee, 'build_artist_name', mock_build)
    monkeypatch.setattr(testee.core.Qt, 'MatchFixedString', 1)
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_item', mock_update)
    testobj.appname = 'appname'
    testobj.artist_buffer = ''
    testobj.data = ('f_name', 'l_name')
    testobj.max_artist = 0
    testobj.new_artists = []

    # test 1: NewAristDialog canceled
    testobj.add_artist()
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name ``\n")

    # test 2: nothing selected (in artist_buffer or through findItems)
    monkeypatch.setattr(MockNewArtistDialog, 'exec_', lambda *x: testee.qtw.QDialog.Accepted)
    monkeypatch.setattr(testee, 'NewArtistDialog', MockNewArtistDialog)
    testobj.add_artist()
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name ``\n"
                                       "called QTreeWidget.findItems with args"
                                       " ('f_name l_name', 1, 0)\n"
                                       "called QMessageBox.information with args"
                                       " `appname` `Artist doesn't exist on the Clementine side`\n")
    # test3a: no artistbuffer, present on the clementine side but not on the albums side
    testobj.artist_buffer = None
    monkeypatch.setattr(testobj.clementine_artists, 'findItems', mock_finditems_yes)
    testobj.add_artist()
    assert testobj.max_artist == 1
    assert len(testobj.new_artists) == 1
    assert isinstance(testobj.new_artists[0], testee.qtw.QTreeWidgetItem)
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name ``\n"
                                       "called QTreeWidget.findItems with args"
                                       " ('f_name l_name', 1, 0)\n"
                                       "called QTreeWidget.findItems with args ('l_name', 1, 1)\n"
                                       "called QTreeWidgetItem.__init__ with args"
                                       " (['f_name', 'l_name', '1'],)\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       # " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       " `<class 'unittests.mockqtwidgets.MockTreeItem'>`\n"
                                       "called CompareArtists.update_item with args"
                                       f" ({testobj.new_artists[0]}, 'x')\n")

    # test3b: not in artistbuffer, present on the clementine side but not on the albums side
    testobj.max_artist = 0
    testobj.new_artists = []
    testobj.artist_buffer = types.SimpleNamespace(text=lambda x: 'some_name')
    monkeypatch.setattr(testobj.albums_artists, 'findItems',  mock_finditems_no)
    testobj.add_artist()
    assert testobj.max_artist == 1
    assert len(testobj.new_artists) == 1
    assert isinstance(testobj.new_artists[0], testee.qtw.QTreeWidgetItem)
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name `some_name`\n"
                                       "called QTreeWidget.findItems with args ('l_name', 1, 1)\n"
                                       "called QTreeWidgetItem.__init__ with args"
                                       " (['f_name', 'l_name', '1'],)\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       # " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       " `<class 'unittests.mockqtwidgets.MockTreeItem'>`\n"
                                       "called CompareArtists.update_item with args"
                                       f" ({testobj.new_artists[0]}, {testobj.artist_buffer})\n")

    # test4: in artistbuffer, but not present on the albums side
    testobj.max_artist = 0
    testobj.new_artists = []
    monkeypatch.setattr(testobj.albums_artists, 'findItems', mock_finditems_data)
    testobj.add_artist()
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name `some_name`\n"
                                       "called QTreeWidget.findItems with args ('l_name', 1, 1)\n"
                                       "called build_artist_name with args ('0', '1')\n"
                                       "called InputDialog.getItem with args"
                                       " ('appname', 'Select Artist', ['0, 1']) {'editable': False}\n"
                                       "called QTreeWidgetItem.__init__ with args"
                                       " (['f_name', 'l_name', '1'],)\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       # " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       " `<class 'unittests.mockqtwidgets.MockTreeItem'>`\n"
                                       "called CompareArtists.update_item with args"
                                       f" ({testobj.new_artists[0]}, {testobj.artist_buffer})\n")

    # test5: in artistbuffer, present on the albums side, getitem dialog canceled
    testobj.data = ('f_name', '0, 1')
    testobj.add_artist()
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name `some_name`\n"
                                       "called QTreeWidget.findItems with args ('0, 1', 1, 1)\n"
                                       "called build_artist_name with args ('0', '1')\n"
                                       "called InputDialog.getItem with args"
                                       " ('appname', 'Select Artist', ['0, 1']) {'editable': False}\n"
                                       "called QTreeWidgetItem.__init__ with args"
                                       " (['f_name', '0, 1', '2'],)\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       # " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       " `<class 'unittests.mockqtwidgets.MockTreeItem'>`\n"
                                       "called CompareArtists.update_item with args"
                                       f" ({testobj.new_artists[-1]}, {testobj.artist_buffer})\n")
    # test6: in artistbuffer, present on the albums side, getitem dialog confirmed
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', lambda *x, **y: ('0, 1', True))
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    # testobj.data = ('f_name', '0, 1')
    testobj.add_artist()
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name `some_name`\n"
                                       "called QTreeWidget.findItems with args ('0, 1', 1, 1)\n"
                                       "called build_artist_name with args ('0', '1')\n"
                                       "called CompareArtists.update_item with args"
                                       f" ({mock_data}, {testobj.artist_buffer})\n")
    return
    # r 448 - zou in de tests met gemockte clementine_artists. findItems true moeten zitten
    testobj.add_artist()
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__ with parent of type '
                                       f"`{type(testobj)}` and name ``\n")

def test_cmpart_delete_artist(monkeypatch, capsys):
    def mock_set(value):
        print(f'called CompareArtists.set_modified with arg `{value}`')
    def mock_settext(*args):
        print('called TreeItem.setText with args', args)
    def mock_find(*args):
        print(f'called CompareArtists.find_items with args', args)
        return [types.SimpleNamespace(setText=mock_settext)]
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'set_modified', mock_set)
    monkeypatch.setattr(testobj.albums_artists, 'currentItem', lambda: None)
    monkeypatch.setattr(testobj.clementine_artists, 'findItems', mock_find)
    testobj.delete_artist()
    assert capsys.readouterr().out == ''

    curr_item = types.SimpleNamespace(text=lambda x: str(x))
    monkeypatch.setattr(testobj.albums_artists, 'currentItem', lambda: curr_item)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj.appname = 'appname'
    testobj.delete_artist()
    assert capsys.readouterr().out == ('called QMessageBox.question with args'
                                       ' `appname` `Ok to delete artist `1, 0`?` `3` `1`\n')

    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', lambda *x: testee.qtw.QMessageBox.Ok)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj.new_artists = [curr_item]
    testobj.new_matches = {}
    testobj.artist_map = {'xx': 'q'}
    testobj.delete_artist()
    assert testobj.new_artists == []
    assert testobj.new_matches == {}
    assert testobj.artist_map == {'xx': 'q'}
    assert capsys.readouterr().out == ('called TreeWidget.currentIndex\n'
                                       'called CompareArtists.set_modified with arg `False`\n')

    testobj.new_artists = [curr_item]
    testobj.new_matches = {'2': 'xx'}
    testobj.artist_map = {'xx': 'z'}
    testobj.delete_artist()
    assert testobj.new_artists == []
    assert testobj.new_matches == {}
    assert testobj.artist_map == {'xx': 'z'}
    assert capsys.readouterr().out == ('called TreeWidget.currentIndex\n'
                                       'called CompareArtists.set_modified with arg `False`\n')

    testobj.new_artists = [curr_item]
    testobj.new_matches = {'1': 'qq', '2': 'xx'}
    testobj.artist_map = {'xx': '2'}
    testobj.delete_artist()
    assert testobj.new_artists == []
    assert testobj.new_matches == {'1': 'qq'}
    assert testobj.artist_map == {'xx': ''}
    assert capsys.readouterr().out == ('called TreeWidget.currentIndex\n'
                                       "called CompareArtists.find_items with args ('xx', 8, 0)\n"
                                       "called TreeItem.setText with args (1, '')\n"
                                       'called CompareArtists.set_modified with arg `True`\n')

def test_cmpart_save_all(monkeypatch, capsys):
    def mock_update(arg):
        print(f'called update_artists with arg `{arg}`)')
        return {'x': 'y'}
    def mock_save(arg):
        print(f'called save_appdata with arg `{arg}`)')
    mockitem = mockqtw.MockTreeItem('x')
    def mock_current():
        print('called TreeWidget.currentItem')
        return mockitem
    assert capsys.readouterr().out == "called QTreeWidgetItem.__init__ with args ('x',)\n"
    def mock_refresh(arg):
        print(f'called CompareArtists.refresh_appdata with arg `{arg}`)')
    def mock_count():
        return 2
    mockitems = [mockqtw.MockTreeItem('a', 'b', '1'), mockqtw.MockTreeItem('x', 'y', '2')]
    assert capsys.readouterr().out == ("called QTreeWidgetItem.__init__ with args ('a', 'b', '1')\n"
                                       "called QTreeWidgetItem.__init__ with args ('x', 'y', '2')\n")
    def mock_item(num):
        return mockitems[num]
    monkeypatch.setattr(testee, 'update_artists', mock_update)
    monkeypatch.setattr(testee, 'save_appdata', mock_save)
    testobj = setup_cmpart(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    monkeypatch.setattr(testobj.clementine_artists, 'currentItem', mock_current)
    testobj.artist_map = {}
    testobj._parent.albums_map = {}
    testobj.save_all()
    assert testobj.artist_map == {'x': 'y'}
    assert testobj._parent.artist_map == {'x': 'y'}
    assert capsys.readouterr().out == ('called TreeWidget.topLevelItemCount\n'
                                       'called update_artists with arg `[]`)\n'
                                       "called save_appdata with arg `[{'x': 'y'}, {}]`)\n"
                                       'called TreeWidget.currentItem\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called CompareArtists.refresh_appdata with arg `x`)\n')
    monkeypatch.setattr(testobj.albums_artists, 'topLevelItemCount', mock_count)
    monkeypatch.setattr(testobj.albums_artists, 'topLevelItem', mock_item)
    testobj.save_all()
    assert capsys.readouterr().out == ("called QTreeWidgetItem.text for col 2\n"
                                       "called QTreeWidgetItem.text for col 0\n"
                                       "called QTreeWidgetItem.text for col 1\n"
                                       "called QTreeWidgetItem.text for col 2\n"
                                       "called QTreeWidgetItem.text for col 0\n"
                                       "called QTreeWidgetItem.text for col 1\n"
                                       "called update_artists with arg"
                                       " `[(1, 'a', 'b'), (2, 'x', 'y')]`)\n"
                                       "called save_appdata with arg `[{'x': 'y'}, {}]`)\n"
                                       'called TreeWidget.currentItem\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called CompareArtists.refresh_appdata with arg `x`)\n')

def test_cmpart_help(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee, 'workflows', {'cmpart': 'wf'})
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.help()
    assert capsys.readouterr().out == "called QMessageBox.information with args `appname` `wf`\n"


# tests for New Artist Dialog
def test_newart_init(monkeypatch, capsys, expected_output):
    def mock_init(self, *args):
        print('called QWidget.__init__')
    def mock_setLayout(self, widget):
        print(f'called QWidget.setLayout with arg of type {type(widget)}')
    def mock_setTitle(self, text):
        print(f'called QDialog.setWindowTitle with arg `{text}`')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setLayout)
    monkeypatch.setattr(testee.qtw.QWidget, 'setWindowTitle', mock_setTitle)
    parent = testee.qtw.QWidget()
    assert capsys.readouterr().out == 'called QWidget.__init__\n'
    parent.appname = 'appname'
    monkeypatch.setattr(testee.qtw, 'QDialog', mockqtw.MockDialog)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGrid)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    testobj = testee.NewArtistDialog(parent)
    bindings = {'reject': testobj.reject, 'update': testobj.update, 'me': testobj, 'text': ''}
    assert capsys.readouterr().out == expected_output['new_artist'].format(**bindings)

    testobj = testee.NewArtistDialog(parent, name='x')
    bindings = {'reject': testobj.reject, 'update': testobj.update, 'me': testobj, 'text': ''}
    assert capsys.readouterr().out == expected_output['new_artist'].format(**bindings)

def test_newart_update(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called NewArtistDialog.__init__')
    def mock_accept(self, *args):
        print('called NewArtistDialog.accept')
    counter = 0
    def mock_text_alles(*args):
        nonlocal counter
        counter += 1
        print('called QLineEdit.text')
        return ('', 'x', 'y')[counter]
    def mock_text_niks(*args):
        return ''
    def mock_text_lname(*args):
        nonlocal counter
        counter += 1
        return ('', '', 'y')[counter]
    def mock_text_fname(*args):
        nonlocal counter
        counter += 1
        return ('', 'x', '')[counter]
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee.NewArtistDialog, '__init__', mock_init)
    monkeypatch.setattr(testee.NewArtistDialog, 'accept', mock_accept)
    testobj = testee.NewArtistDialog()
    mock_parent = types.SimpleNamespace(data=())
    monkeypatch.setattr(testobj, 'parent', lambda *x: mock_parent)
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_alles)
    testobj.first_name = mockqtw.MockLineEdit()
    testobj.last_name = mockqtw.MockLineEdit()
    assert capsys.readouterr().out == ('called NewArtistDialog.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n')
    testobj.update()
    assert testobj.parent().data == ('x', 'y')
    assert capsys.readouterr().out == ('called QLineEdit.text\n'
                                       'called QLineEdit.text\n'
                                       'called NewArtistDialog.accept\n')

    testobj.parent().data = ()
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_niks)
    testobj.update()
    assert testobj.parent().data == ()
    assert capsys.readouterr().out == ('called QMessageBox.information with args `AlbumsMatcher`'
                                       ' `Enter at least one name or press `Cancel``\n')

    counter = 0
    testobj.parent().data = ()
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_fname)
    testobj.update()
    assert testobj.parent().data == ('x', '')
    assert capsys.readouterr().out == 'called NewArtistDialog.accept\n'

    counter = 0
    testobj.parent().data = ()
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_lname)
    testobj.update()
    assert testobj.parent().data == ('', 'y')
    assert capsys.readouterr().out == 'called NewArtistDialog.accept\n'


# tests for Compare Albums Tab
def setup_cmpalb(monkeypatch, capsys, widgets=True):
    def mock_init(self, parent):
        print('called QWidget.__init__')
        self._parent = parent
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    testparent = MockMainFrame()
    testobj = testee.CompareAlbums(testparent)
    output = 'called MainFrame.__init__\ncalled QApplication.__init__\ncalled QWidget.__init__\n'
    if widgets:
        testobj.artist_list = mockqtw.MockComboBox()
        testobj.clementine_albums = mockqtw.MockTree()
        testobj.albums_albums = mockqtw.MockTree()
        output += ('called ComboBox.__init__\ncalled QTreeWidget.__init__\n'
                   'called QTreeWidget.__init__\n')
    assert capsys.readouterr().out == output
    return testobj

def test_cmpalb_create_widgets(monkeypatch, capsys, expected_output):
    def mock_get(*args):
        pass
    def mock_popup(*args):
        pass
    def mock_setlayout(win):
        print(f'called CompareAlbums.setLayout with arg of type {type(win)}')
    def mock_save(*args):
        pass
    def mock_next(*args):
        pass
    def mock_prev(*args):
        pass
    def mock_help(*args):
        pass
    def mock_find(*args):
        pass
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBox)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTree)
    monkeypatch.setattr(testee.qtw, 'QHeaderView', mockqtw.MockHeader)
    monkeypatch.setattr(testee.core, 'QSize', mockqtw.MockSize)
    monkeypatch.setattr(testee, 'popuptext', mock_popup)
    testobj = setup_cmpalb(monkeypatch, capsys, widgets=False)
    testobj._parent.title = 'apptitle'
    testobj._parent.down_icon = 'down_icon'
    testobj._parent.up_icon = 'up_icon'
    monkeypatch.setattr(testobj, 'setLayout', mock_setlayout)
    monkeypatch.setattr(testobj, 'get_albums', mock_get)
    monkeypatch.setattr(testobj, 'save_all', mock_save)
    monkeypatch.setattr(testobj, 'next_artist', mock_next)
    monkeypatch.setattr(testobj, 'prev_artist', mock_prev)
    monkeypatch.setattr(testobj, 'help', mock_help)
    monkeypatch.setattr(testobj, 'find_album', mock_find)
    testobj.create_widgets()
    bindings = {'me': testobj,
                'get_albums': testobj.get_albums,
                'popuptext': testee.popuptext,
                'save_all': testobj.save_all,
                'next_artist': testobj.next_artist,
                'prev_artist': testobj.prev_artist,
                'help': testobj.help,
                'find_album': testobj.find_album
                }
    assert capsys.readouterr().out == expected_output['compare_albums'].format(**bindings)

def test_cmpalb_create_actions(monkeypatch, capsys, expected_output):
    def mock_add(arg):
        print(f'called CompareArtists.addAction')
    monkeypatch.setattr(testee.qtw, 'QAction', mockqtw.MockAction)
    testobj = setup_cmpalb(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'addAction', mock_add)
    testobj.artist_list = mockqtw.MockTree()
    testobj.create_actions()
    bindings = {'me': testobj,
                'help': testobj.help,
                'select': testobj.artist_list.setFocus,
                'focus': testobj.focus_albums,
                'next': testobj.next_artist,
                'prev': testobj.prev_artist,
                'find': testobj.find_album,
                'save': testobj.save_all}
    assert capsys.readouterr().out == expected_output['compare_albums_actions'].format(**bindings)

def test_cmpalb_refresh_screen(monkeypatch, capsys, expected_output):
    def mock_set(value):
        print(f'called CompareAlbums.set_modified with arg `{value}`')
    def mock_update():
        print(f'called CompareAlbums.update_navigation_buttons')
    def mock_text(num):
        print(f'called TreeWidgetItem.text with arg `{num}`')
        return 'X' if num == 1 else 'qq'
    def mock_settext(*args):
        print(f'called TreeWidgetItem.setText with args', args)
    def mock_getitem(num):
        print(f'called TreeWidget.topLevelItem with arg `{num}`')
        return types.SimpleNamespace(text=mock_text, setText=mock_settext)

    testobj = setup_cmpalb(monkeypatch, capsys, widgets=True)
    # in setup opzetten combobox artist_list en tree clementine_albums
    monkeypatch.setattr(testobj, 'set_modified', mock_set)
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    # testobj._parent.artist_map = {}
    # testobj._parent.albums_map = {}
    assert testobj.refresh_screen() == 'Please match some artists first'
    assert testobj.artist_map == {}
    assert testobj.albums_map == {}
    assert capsys.readouterr().out == 'called CompareAlbums.set_modified with arg `False`\n'

    monkeypatch.setattr(testee.dmlc, 'list_artists', lambda: [{'artist': 'a'}])
    testobj._parent.artist_map = {'a': 'y'}
    testobj._parent.albums_map = {'x': {'qq': ('r', 's')}}
    testobj.c_artist = 'x'
    assert testobj.refresh_screen() == ''
    assert testobj.artist_map == {'a': 'y'}
    assert testobj.albums_map == {'x': {'qq': ('r', 's')}}
    assert testobj.c_artists == ['a']
    assert capsys.readouterr().out == ("called CompareAlbums.set_modified with arg `False`\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `['a']`\n"
                                       "called TreeWidget.topLevelItemCount\n"
                                       "called CompareAlbums.update_navigation_buttons\n")
    monkeypatch.setattr(testobj.clementine_albums, 'topLevelItemCount', lambda: 1)
    monkeypatch.setattr(testobj.clementine_albums, 'topLevelItem', mock_getitem)
    testobj._parent.artist_map = {'a': 'y'}
    testobj._parent.albums_map = {'x': {'qq': ('r', 's')}}
    testobj.c_artist = 'x'
    assert testobj.refresh_screen('artist') == ''
    assert testobj.artist_map == {'a': 'y'}
    assert testobj.albums_map == {'x': {'qq': ('r', 's')}}
    assert testobj.c_artists == ['a']
    assert capsys.readouterr().out == ("called CompareAlbums.set_modified with arg `False`\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `['a']`\n"
                                       "called TreeWidget.topLevelItem with arg `0`\n"
                                       "called TreeWidgetItem.text with arg `1`\n"
                                       "called TreeWidgetItem.text with arg `0`\n"
                                       "called TreeWidgetItem.setText with args (1, 's')\n"
                                       "called ComboBox.setCurrentIndex to `artist`\n"
                                       "called CompareAlbums.update_navigation_buttons\n")
    # nog situaties: dat ik bij setCurrentIndex de eerste keer een TypeError krijg en dan
    # bij de volgende een ValueError of niet
    counter = 0
    def mock_setindex(number):
        nonlocal counter
        counter += 1
        if counter == 1:
            raise TypeError
        print(f'called ComboBox.setCurrentIndex with arg `{number}`')
    monkeypatch.setattr(testobj.artist_list, 'setCurrentIndex', mock_setindex)
    monkeypatch.setattr(testee.dmlc, 'list_artists', lambda: [{'artist': 'b'}])
    testobj._parent.artist_map = {'b': 'y'}
    testobj._parent.albums_map = {'x': {'qq': ('r', 's')}}
    testobj.c_artist = 'x'
    assert testobj.refresh_screen('artist') == 'This artist has not been matched yet'
    assert testobj.artist_map == {'b': 'y'}
    assert testobj.albums_map == {'x': {'qq': ('r', 's')}}
    assert testobj.c_artists == ['b']
    assert capsys.readouterr().out == ("called CompareAlbums.set_modified with arg `False`\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `['b']`\n"
                                       "called TreeWidget.topLevelItem with arg `0`\n"
                                       "called TreeWidgetItem.text with arg `1`\n"
                                       "called TreeWidgetItem.text with arg `0`\n"
                                       "called TreeWidgetItem.setText with args (1, 's')\n")
    counter = 0
    monkeypatch.setattr(testee.dmlc, 'list_artists', lambda: [{'artist': 1}])
    testobj._parent.artist_map = {1: 'y'}
    testobj._parent.albums_map = {'x': {'qq': ('r', 's')}}
    testobj.c_artist = 'x'
    assert testobj.refresh_screen(1) == ''
    assert testobj.artist_map == {1: 'y'}
    assert testobj.albums_map == {'x': {'qq': ('r', 's')}}
    assert testobj.c_artists == [1]
    assert capsys.readouterr().out == ("called CompareAlbums.set_modified with arg `False`\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `[1]`\n"
                                       "called TreeWidget.topLevelItem with arg `0`\n"
                                       "called TreeWidgetItem.text with arg `1`\n"
                                       "called TreeWidgetItem.text with arg `0`\n"
                                       "called TreeWidgetItem.setText with args (1, 's')\n"
                                       "called ComboBox.setCurrentIndex with arg `0`\n"
                                       "called CompareAlbums.update_navigation_buttons\n")

def test_cmpalb_set_modified(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.save_button = mockqtw.MockButton()
    assert capsys.readouterr().out == 'called PushButton.__init__ with args ()\n'
    testobj.set_modified(True)
    assert testobj.modified is True
    assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `True`\n'
    testobj.set_modified(False)
    assert testobj.modified is False
    assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `False`\n'

def test_cmpalb_update_navigation_buttons(monkeypatch, capsys):
    def mock_focus():
        print('called CompareAlbums.focus_albums')
    testobj = setup_cmpalb(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'focus_albums', mock_focus)
    testobj.artist_list = mockqtw.MockComboBox()
    testobj.prev_artist_button = mockqtw.MockButton()
    testobj.next_artist_button = mockqtw.MockButton()
    assert capsys.readouterr().out == ('called ComboBox.__init__\n'
                                       'called PushButton.__init__ with args ()\n'
                                       'called PushButton.__init__ with args ()\n')
    monkeypatch.setattr(testobj.artist_list, 'currentIndex', lambda: 0)
    testobj.c_artists = []
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ('called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `False`\n'
                                       'called CompareAlbums.focus_albums\n')
    monkeypatch.setattr(testobj.artist_list, 'currentIndex', lambda: 0)
    testobj.c_artists = ['x']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ('called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `False`\n'
                                       'called PushButton.setEnabled with arg `False`\n'
                                       'called CompareAlbums.focus_albums\n')
    testobj.c_artists = ['x', 'y']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ('called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `False`\n'
                                       'called CompareAlbums.focus_albums\n')
    monkeypatch.setattr(testobj.artist_list, 'currentIndex', lambda: 1)
    testobj.c_artists = []
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ('called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `True`\n'
                                       'called CompareAlbums.focus_albums\n')
    testobj.c_artists = ['x']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ('called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `True`\n'
                                       'called CompareAlbums.focus_albums\n')
    testobj.c_artists = ['x', 'y']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ('called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `False`\n'
                                       'called CompareAlbums.focus_albums\n')
    testobj.c_artists = ['x', 'y', 'z']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ('called PushButton.setEnabled with arg `True`\n'
                                       'called PushButton.setEnabled with arg `True`\n'
                                       'called CompareAlbums.focus_albums\n')

def test_cmpalb_get_albums(monkeypatch, capsys):
    def mock_read(*args):
        print('called read_artist_albums with args', *args)
        return [], []
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.get_albums()
    assert capsys.readouterr().out == 'called ComboBox.count\n'

    monkeypatch.setattr(testobj.artist_list, 'count', lambda *x: 1)
    testobj.artist_map = {'.': '..'}
    testobj.albums_map = {}
    monkeypatch.setattr(testee, 'read_artist_albums', mock_read)
    testobj.albums_to_save = {'.': []}
    monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
    monkeypatch.setattr(testee.core.Qt, 'UserRole', 'x')
    testobj.get_albums()
    assert testobj.c_artist == '.'
    assert testobj._parent.current_data == '.'
    assert testobj.a_artist == '..'
    assert testobj.lookup == {}
    assert testobj.tracks == {}
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called read_artist_albums with args .. .\n'
                                       'called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n')
    testobj.albums_to_save = {'.': [('x', 'None', 1, 'q', 'r')]}
    monkeypatch.setattr(testee, 'read_artist_albums', lambda *x: ([], [('x', 1)]))
    testobj.get_albums()
    assert testobj.c_artist == '.'
    assert testobj._parent.current_data == '.'
    assert testobj.a_artist == '..'
    assert testobj.lookup == {'x': ['1']}
    assert testobj.tracks == {}
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called QTreeWidget.clear\n'
                                       "called QTreeWidgetItem.__init__ with args (['x'],)\n"
                                       "called QTreeWidgetItem.setData to"
                                        " `1` with role x for col 0\n"
                                        "called QTreeWidget.addTopLevelItem with arg of type"
                                        " `<class 'unittests.mockqtwidgets.MockTreeItem'>`\n"
                                        "called QTreeWidget.clear\n"
                                        "called QTreeWidgetItem.__init__ with args"
                                       " (['x', '', '1'],)\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'unittests.mockqtwidgets.MockTreeItem'>`\n")

def test_cmpalb_focus_albums(monkeypatch, capsys):
    def mock_text_0(num):
        print(f'called TreeItem.text for column {num}')
        return str(num)
    def mock_text_1(num):
        print(f'called TreeItem.text for column {num}')
        return ''
    item_0 = types.SimpleNamespace(text=mock_text_0)
    item_1 = types.SimpleNamespace(text=mock_text_1)
    def mock_getitem(num):
        print(f'called TreeWidget.topLevelItem with index {num}')
        return item_0 if num == 0 else item_1
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.focus_albums()
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       'called TreeWidget.topLevelItemCount\n'
                                       'called QTreeWidget.setCurrentItem with arg'
                                       ' `TreeWidget.topLevelItem with index 0`\n')
    monkeypatch.setattr(testobj.clementine_albums, 'topLevelItem', mock_getitem)
    monkeypatch.setattr(testobj.clementine_albums, 'topLevelItemCount', lambda: 1)
    testobj.focus_albums()
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       'called TreeWidget.topLevelItem with index 0\n'
                                       'called TreeItem.text for column 1\n'
                                       'called TreeWidget.topLevelItem with index 0\n'
                                       f'called QTreeWidget.setCurrentItem with arg `{item_0}`\n')
    monkeypatch.setattr(testobj.clementine_albums, 'topLevelItemCount', lambda: 2)
    testobj.focus_albums()
    assert capsys.readouterr().out == ('called QTreeWidget.setFocus\n'
                                       'called TreeWidget.topLevelItem with index 0\n'
                                       'called TreeItem.text for column 1\n'
                                       'called TreeWidget.topLevelItem with index 1\n'
                                       'called TreeItem.text for column 1\n'
                                       f'called QTreeWidget.setCurrentItem with arg `{item_1}`\n')

def test_cmpalb_next_artist(monkeypatch, capsys):
    def mock_update():
        print(f'called CompareAlbums.update_navigation_buttons')
    testobj = setup_cmpalb(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    testobj.next_artist()
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.count\n')
    monkeypatch.setattr(testobj.artist_list, 'count', lambda: 3)
    testobj.next_artist()
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.setCurrentIndex to `2`\n'
                                       'called CompareAlbums.update_navigation_buttons\n')

def test_cmpalb_prev_artist(monkeypatch, capsys):
    def mock_update():
        print(f'called CompareAlbums.update_navigation_buttons')
    testobj = setup_cmpalb(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    testobj.prev_artist()
    assert capsys.readouterr().out == ('called ComboBox.currentIndex\n'
                                       'called ComboBox.setCurrentIndex to `0`\n'
                                       'called CompareAlbums.update_navigation_buttons\n')
    monkeypatch.setattr(testobj.artist_list, 'currentIndex', lambda: 0)
    testobj.prev_artist()
    assert capsys.readouterr().out == ''

def test_cmpalb_find_album(monkeypatch, capsys):
    def get_text(col):
        print(f'called TreeWidgetItem.text for column {col}')
        return 'xix'
    currentitem = types.SimpleNamespace(text=get_text)
    def mock_current(*args):
        print('called TreeWidget.currentItem')
        return currentitem
    counter = 0
    def mock_current_2(*args):
        nonlocal counter
        print('called TreeWidget.currentItem')
        counter += 1
        if counter == 1:
            return None
        return currentitem
    def mock_focus():
        print('called CompareAlbums.focus_albums')
    def mock_add(*args):
        print('called CompareAlbums.add_album with args', args)
    def mock_check(*args):
        print('called CompareAlbums.check_if_new_album with args', arg)
        return None
    def mock_prepare(*args):
        print('called CompareAlbums.prepare_album_for_update with args', args)
    def mock_list(*args):
        print('called dmla.list_albums_by_artist with args', args)
        return []
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.appname = 'app'
    monkeypatch.setattr(testobj.clementine_albums, 'currentItem', mock_current)
    monkeypatch.setattr(testobj, 'focus_albums', mock_focus)
    monkeypatch.setattr(testobj, 'add_album', mock_add)
    monkeypatch.setattr(testobj, 'check_if_new_album', mock_check)
    monkeypatch.setattr(testobj, 'prepare_album_for_update', mock_prepare)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    monkeypatch.setattr(testee.dmla, 'list_albums_by_artist', mock_list)
    testobj.c_artist = 'x'
    testobj.albums_map = {'x': {'xix': 2}}
    testobj.find_album()
    assert capsys.readouterr().out == ('called TreeWidget.currentItem\n'
                                       'called TreeWidgetItem.text for column 0\n'
                                       'called QMessageBox.question with args `app`'
                                       ' `Album already has a match - do you want to reassign?`'
                                       ' `12` `4`\n')
    monkeypatch.setattr(testobj.clementine_albums, 'currentItem', mock_current_2)
    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', lambda *x: testee.qtw.QMessageBox.Ok)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj.c_artist = 'x'
    testobj.a_artist = 2
    testobj.albums_map = {'x': {'xix': 2}}
    testobj.find_album()
    assert testobj.albums_map == {'x': {}}
    assert capsys.readouterr().out == ('called TreeWidget.currentItem\n'
                                       'called CompareAlbums.focus_albums\n'
                                       'called TreeWidget.currentItem\n'
                                       'called TreeWidgetItem.text for column 0\n'
                                       'called TreeWidgetItem.text for column 0\n'
                                       "called dmla.list_albums_by_artist with args"
                                       " ('', 2, 'Titel')\n"
                                       'called CompareAlbums.add_album with args ()\n')
    monkeypatch.setattr(testobj.clementine_albums, 'currentItem', mock_current)
    monkeypatch.setattr(testee.dmla, 'list_albums_by_artist', lambda *x: [('qq', 'rr')])
    monkeypatch.setattr(testobj, 'check_if_new_album', lambda x: ('a_name', 'albumid'))
    testobj.find_album()
    assert testobj.albums_map == {'x': {}}
    assert capsys.readouterr().out == ('called TreeWidget.currentItem\n'
                                       'called TreeWidgetItem.text for column 0\n'
                                       "called InputDialog.getItem with args"
                                       " ('app', 'Select Album', ['a_name']) {'editable': False}\n"
                                       'called CompareAlbums.add_album with args ()\n')
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', lambda *args, **kwargs: ('a_name', True))
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    testobj.find_album()
    assert testobj.albums_map == {'x': {}}
    assert capsys.readouterr().out == ('called TreeWidget.currentItem\n'
                                       'called TreeWidgetItem.text for column 0\n'
                                       "called CompareAlbums.prepare_album_for_update with args"
                                       f" ({currentitem}, ('a_name', 'albumid'))\n")

def test_cmpalb_check_new_album(monkeypatch, capsys):
    monkeypatch.setattr(testee, 'build_album_name', lambda x: x.name)
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.c_artist = 'xx'
    testobj.albums_map = {}
    with pytest.raises(KeyError):
        testobj.check_if_new_album(types.SimpleNamespace(id=1, name='hello')) == ('hello', 1)
    testobj.albums_map = {'xx': {}}
    assert testobj.check_if_new_album(types.SimpleNamespace(id=1, name='hello')) == ('hello', 1)
    testobj.albums_map = {'xx': {'y': ()}}
    with pytest.raises(IndexError):
        testobj.check_if_new_album(types.SimpleNamespace(id=1, name='hello')) == ('hello', 1)
    testobj.albums_map = {'xx': {'y': ('a', 0), 'z': ('b', 1)}}
    assert testobj.check_if_new_album(types.SimpleNamespace(id=1, name='hello')) is None

def test_cmpalb_prepare_for_update(monkeypatch, capsys):
    def mock_text(col):
        print(f'called QTreeWidgetItem.text for col {col}')
        return '9'
    def mock_set(col, text):
        print(f'called QTreeWidgetItem.setText for col {col} with arg `{text}`')
    def mock_data(col, role):
        print(f'called QTreeWidgetItem.data for col {col} role {role}')
        return ''
    def mock_update(*args):
        print('called CompareAlbums.update_item with args', args)
    a_item = types.SimpleNamespace(text=mock_text, setText=mock_set)
    def mock_find(*args):
        return [a_item]
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee.core.Qt, 'MatchFixedString', 2)
    monkeypatch.setattr(testee.core.Qt, 'UserRole', 5)
    testobj = setup_cmpalb(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_item', mock_update)
    monkeypatch.setattr(testobj.albums_albums, 'findItems', mock_find)
    testobj.appname = 'app'
    testobj.c_artist = 'x'
    testobj.albums_to_update = {'x': []}
    c_item = types.SimpleNamespace(data=mock_data)
    testobj.prepare_album_for_update(c_item, ('title', 1))
    assert testobj.albums_to_update == {'x': [('9', '9', 9, False, [])]}
    assert capsys.readouterr().out == ('called QTreeWidgetItem.data for col 0 role 5\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 1\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called CompareAlbums.update_item with args'
                                       f" ({a_item}, {c_item})\n")
    testobj.albums_to_update = {'x': []}
    c_item = types.SimpleNamespace(data=lambda *x: '9')
    testobj.prepare_album_for_update(c_item, ('title', 1))
    assert testobj.albums_to_update == {'x': [('9', '9', 9, False, [])]}
    assert capsys.readouterr().out == ('called QTreeWidgetItem.text for col 1\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 1\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called CompareAlbums.update_item with args'
                                       f" ({a_item}, {c_item})\n")
    testobj.albums_to_update = {'x': []}
    c_item = types.SimpleNamespace(data=lambda *x: '8')
    testobj.prepare_album_for_update(c_item, ('title', 1))
    assert testobj.albums_to_update == {'x': [('9', '9', 9, False, [])]}
    assert capsys.readouterr().out == ('called QTreeWidgetItem.text for col 1\n'
                                       'called QMessageBox.question with args'
                                       ' `app` `Clementine year (8) differs from Albums year (9),'
                                       ' replace?` `12` `4`\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 1\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called CompareAlbums.update_item with args'
                                       f" ({a_item}, {c_item})\n")
    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', lambda *x: testee.qtw.QMessageBox.Yes)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testobj.albums_to_update = {'x': []}
    c_item = types.SimpleNamespace(data=lambda *x: '8')
    testobj.prepare_album_for_update(c_item, ('title', 1))
    assert testobj.albums_to_update == {'x': [('9', '9', 9, False, [])]}
    assert capsys.readouterr().out == ('called QTreeWidgetItem.text for col 1\n'
                                       'called QTreeWidgetItem.setText for col 1 with arg `8`\n'
                                       'called QTreeWidgetItem.text for col 0\n'
                                       'called QTreeWidgetItem.text for col 1\n'
                                       'called QTreeWidgetItem.text for col 2\n'
                                       'called CompareAlbums.update_item with args'
                                       f" ({a_item}, {c_item})\n")

def test_cmpalb_add_album(monkeypatch, capsys):
    def mock_text(col):
        print(f'called QTreeWidgetItem.text for col {col}')
        return 'x'
    def mock_data(col, role):
        print(f'called QTreeWidgetItem.data for col {col} role {role}')
        return '9999'
    def mock_current():
        print('called TreeWidget.currentItem')
        return None
    #    return types.SimpleNamespace(text=mock_text, data=mock_data)
    def mock_build(*args):
        print('called CompareAlbums.build_album_name with args', args)
        return args[0]
    def mock_prepare(*args):
        print('called CompareAlbums.prepare_album_for_saving with args', args)
    def mock_update(*args):
        print('called CompareAlbums.update_item with args', args)
    monkeypatch.setattr(testee, 'NewAlbumDialog', MockNewAlbumDialog)
    monkeypatch.setattr(testee, 'build_album_name', mock_build)
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    monkeypatch.setattr(testee.core.Qt, 'MatchFixedString', 2)
    monkeypatch.setattr(testee.core.Qt, 'UserRole', 5)
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.appname = 'app'
    monkeypatch.setattr(testobj, 'prepare_album_for_saving', mock_prepare)
    monkeypatch.setattr(testobj, 'update_item', mock_update)
    # nog doen: geen currentitem maar dialog levert accepted
    monkeypatch.setattr(testobj.clementine_albums, 'currentItem', mock_current)
    testobj.add_album()
    assert capsys.readouterr().out == ("called TreeWidget.currentItem\n"
                                       "called NewAlbumDialog.__init__ with parent of type"
                                       " `<class 'apps.albumsmatcher.CompareAlbums'>`"
                                       " and name ``, year ``\n")
    monkeypatch.setattr(MockNewAlbumDialog, 'exec_', lambda *x: testee.qtw.QDialog.Accepted)
    monkeypatch.setattr(testobj.clementine_albums, 'currentItem', lambda *x: None)
    testobj.data = ('xx', '1111', 'true/false')
    testobj.add_album()
    assert capsys.readouterr().out == ("called NewAlbumDialog.__init__ with parent of type"
                                       " `<class 'apps.albumsmatcher.CompareAlbums'>`"
                                       " and name ``, year ``\n"
                                       "called QTreeWidget.findItems with args ('xx', 2, 0)\n"
                                       "called QMessageBox.information with args"
                                       " `app` `Album doesn't exist on the Clementine side`\n")
    monkeypatch.setattr(testobj.clementine_albums, 'currentItem', mock_current)
    monkeypatch.setattr(testee, 'NewAlbumDialog', MockNewAlbumDialog)
    testobj.add_album()
    assert capsys.readouterr().out == ("called TreeWidget.currentItem\n"
                                       "called NewAlbumDialog.__init__ with parent of type"
                                       " `<class 'apps.albumsmatcher.CompareAlbums'>`"
                                       " and name ``, year ``\n"
                                       "called QTreeWidget.findItems with args ('xx', 2, 0)\n"
                                       "called QMessageBox.information with args"
                                       " `app` `Album doesn't exist on the Clementine side`\n")
    monkeypatch.setattr(testobj.clementine_albums, 'findItems', lambda *x: 'c_item')
    testobj.add_album()
    assert capsys.readouterr().out == ("called TreeWidget.currentItem\n"
                                       "called NewAlbumDialog.__init__ with parent of type"
                                       " `<class 'apps.albumsmatcher.CompareAlbums'>`"
                                       " and name ``, year ``\n"
                                       "called QTreeWidget.findItems with args ('xx', 2, 0)\n"
                                       "called CompareAlbums.prepare_album_for_saving with args"
                                       " ('c', 'xx', '1111', 'true/false')\n"
                                       "called CompareAlbums.update_item with args (None, 'c')\n")
    monkeypatch.setattr(testobj.albums_albums, 'findItems', lambda *x: ['a_item'])
    testobj.add_album()
    assert capsys.readouterr().out == ("called TreeWidget.currentItem\n"
                                       "called NewAlbumDialog.__init__ with parent of type"
                                       " `<class 'apps.albumsmatcher.CompareAlbums'>`"
                                       " and name ``, year ``\n"
                                       "called CompareAlbums.build_album_name with args ('a_item',)\n"
                                       "called InputDialog.getItem with args"
                                       " ('app', 'Select Album', ['a_item']) {'editable': False}\n"
                                       "called CompareAlbums.prepare_album_for_saving with args"
                                       " ('c', 'xx', '1111', 'true/false')\n"
                                       "called CompareAlbums.update_item with args (None, 'c')\n")
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', lambda *x, **y: ('a_item', True))
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    # breakpoint()
    testobj.add_album()
    assert capsys.readouterr().out == ("called TreeWidget.currentItem\n"
                                       "called NewAlbumDialog.__init__ with parent of type"
                                       " `<class 'apps.albumsmatcher.CompareAlbums'>`"
                                       " and name ``, year ``\n"
                                       "called CompareAlbums.build_album_name with args ('a_item',)\n"
                                       "called CompareAlbums.update_item with args ('a_item', 'c')\n")


def test_cmpalb_prepare_for_saving(monkeypatch, capsys):
    def mock_list(*args):
        print('called dmlc.list_tracks_for_album with args', args)
        return [{'track': 0, 'title': 'xxx'}, {'track': -1, 'title': 'yyy'}]
    def mock_text(num):
        print(f'called TreeItem.text with arg `{num}`')
        return 'name'
    monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
    monkeypatch.setattr(testee.dmlc, 'list_tracks_for_album', mock_list)
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.c_artist = 'x'
    testobj.albums_to_save = {'x': []}
    c_item = types.SimpleNamespace(text=mock_text)
    testobj.prepare_album_for_saving(c_item, 'albumname', 9999, 'true/false')
    assert testobj.albums_to_save == {'x': [('albumname', 9999, 'X', 'true/false', [(1, 'xxx')])]}
    assert capsys.readouterr().out == ("called QTreeWidgetItem.__init__ with args"
                                       " (['albumname', 9999, '0'],)\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'unittests.mockqtwidgets.MockTreeItem'>`\n"
                                       "called TreeItem.text with arg `0`\n"
                                       "called dmlc.list_tracks_for_album with args ('x', 'name')\n")

def test_cmpalb_update_item(monkeypatch, capsys):
    def mock_build(arg):
        print(f'called build_album_name with arg `{arg}`')
        return 'name'
    def mock_set(value):
        print(f'called CompareAlbums.set_modified with arg `{value}`')
    def mock_settext(num, text):
        print(f'called TreeItem.settext with args `{num}` `{text}`')
    monkeypatch.setattr(testee, 'build_album_name', mock_build)
    testobj = setup_cmpalb(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'set_modified', mock_set)
    testobj.c_artist = 'artist'
    testobj.albums_map = {'artist': {'20': ''}}
    new_item = types.SimpleNamespace(text=lambda x: str(x + 10))
    from_item = types.SimpleNamespace(text=lambda x: str(x + 20), setText=mock_settext)
    testobj.update_item(new_item, from_item)
    assert testobj.albums_map == {'artist': {'20': ('name', 12)}}
    assert capsys.readouterr().out == (f'called QTreeWidget.setCurrentItem with arg `{new_item}`\n'
                                       f'called QTreeWidget.scrollToItem with arg `{new_item}`\n'
                                       f'called build_album_name with arg `{new_item}`\n'
                                       'called TreeItem.settext with args `1` `X`\n'
                                       'called CompareAlbums.set_modified with arg `True`\n'
                                       'called TreeWidget.itemBelow with arg TreeWidget.currentItem\n'
                                       'called QTreeWidget.setCurrentItem with arg `x`\n')
    monkeypatch.setattr(testobj.clementine_albums, 'itemBelow', lambda *x: None)
    testobj.update_item(new_item, from_item)
    assert testobj.albums_map == {'artist': {'20': ('name', 12)}}
    assert capsys.readouterr().out == (f'called QTreeWidget.setCurrentItem with arg `{new_item}`\n'
                                       f'called QTreeWidget.scrollToItem with arg `{new_item}`\n'
                                       f'called build_album_name with arg `{new_item}`\n'
                                       'called TreeItem.settext with args `1` `X`\n'
                                       'called CompareAlbums.set_modified with arg `True`\n')

def test_cmpalb_save_all(monkeypatch, capsys):
    def mock_save(*args):
        print('called save_appdata with args', args)
    def mock_refresh(*args):
        print('called CompareAlbums.refresh_screen with args', args)
    def mock_update(*args):
        print('called dmla.update_albums_by_artist with args', args)
        return [types.SimpleNamespace(id=1, title='xxx', year=2000)]
    def mock_build(arg):
        print(f'called build_album_name for `{arg}`')
        return f'{arg.title}, {arg.year}'
    monkeypatch.setattr(testee, 'save_appdata', mock_save)
    monkeypatch.setattr(testee, 'build_album_name', mock_build)
    monkeypatch.setattr(testee.dmla, 'update_albums_by_artist', mock_update)
    monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
    testobj = setup_cmpalb(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    # testobj._parent.artist_map = {}
    # testobj._parent.albums_map = {}
    testobj.albums_map = {}
    testobj.albums_to_save = {}
    testobj.albums_to_update = {}
    testobj.save_all()
    assert testobj.albums_map == {}
    assert testobj.albums_to_save == {}
    assert testobj.albums_to_update == {}
    assert capsys.readouterr().out == ("called QCursor with arg 3\n"
                                       "called app.setOverrideCursor with arg of type"
                                       " <class 'unittests.mockqtwidgets.MockCursor'>\n"
                                       "called app.restoreOverrideCursor\n"
                                       "called save_appdata with args ([{}, {}],)\n"
                                       "called ComboBox.currentIndex\n"
                                       "called CompareAlbums.refresh_screen with args (1,)\n")

    testobj.albums_map = {'x': {'cname': ('aname', 11)}}
    testobj.artist_map = {'x': 5, 'z': 9}
    testobj.albums_to_save = {'x': [], 'z': []}
    testobj.albums_to_update = {'x': [('aa', 1, 15, True, []), ('bb', 2, 'X', False, [])], 'z': []}
    testobj.save_all()
    assert testobj.albums_map == {'x': {'cname': ('aname', 11)}}
    assert testobj.albums_to_save == {}
    assert testobj.albums_to_update == {}
    assert capsys.readouterr().out == ("called QCursor with arg 3\n"
                                       "called app.setOverrideCursor with arg of type"
                                       " <class 'unittests.mockqtwidgets.MockCursor'>\n"
                                       "called dmla.update_albums_by_artist with args"
                                       " (5, [(15, 'aa', 1, True, []), (0, 'bb', 2, False, [])])\n"
                                       "called build_album_name for"
                                       " `namespace(id=1, title='xxx', year=2000)`\n"
                                       "called app.restoreOverrideCursor\n"
                                       "called save_appdata with args"
                                       " ([{}, {'x': {'cname': ('aname', 11)}}],)\n"
                                       "called ComboBox.currentIndex\n"
                                       "called CompareAlbums.refresh_screen with args (1,)\n")

    testobj.albums_map = {'x': {'cname': ('xxx, 2000', 10)}}
    testobj.artist_map = {'x': 5, 'z': 9}
    testobj.albums_to_save = {'x': [], 'z': []}
    testobj.albums_to_update = {'x': [('aa', 1, 15, True, []), ('bb', 2, 'X', False, [])], 'z': []}
    testobj.save_all()
    assert testobj.albums_map == {'x': {'cname': ('xxx, 2000', 1)}}
    assert testobj.albums_to_save == {}
    assert testobj.albums_to_update == {}
    assert capsys.readouterr().out == ("called QCursor with arg 3\n"
                                       "called app.setOverrideCursor with arg of type"
                                       " <class 'unittests.mockqtwidgets.MockCursor'>\n"
                                       "called dmla.update_albums_by_artist with args"
                                       " (5, [(15, 'aa', 1, True, []), (0, 'bb', 2, False, [])])\n"
                                       "called build_album_name for"
                                       " `namespace(id=1, title='xxx', year=2000)`\n"
                                       "called app.restoreOverrideCursor\n"
                                       "called save_appdata with args"
                                       " ([{}, {'x': {'cname': ('xxx, 2000', 1)}}],)\n"
                                       "called ComboBox.currentIndex\n"
                                       "called CompareAlbums.refresh_screen with args (1,)\n")

    monkeypatch.setattr(testee.dmla, 'update_albums_by_artist',
                        lambda *x: [types.SimpleNamespace(id=10, title='xxx', year=2000)])
    testobj.albums_map = {'x': {'cname': ('xxx, 2000', 10)}}
    testobj.artist_map = {'x': 5, 'z': 9}
    testobj.albums_to_save = {'x': [], 'z': []}
    testobj.albums_to_update = {'x': [('aa', 1, 15, True, []), ('bb', 2, 'X', False, [])], 'z': []}
    testobj.save_all()
    assert testobj.albums_map == {'x': {'cname': ('xxx, 2000', 10)}}
    assert testobj.albums_to_save == {}
    assert testobj.albums_to_update == {}
    assert capsys.readouterr().out == ("called QCursor with arg 3\n"
                                       "called app.setOverrideCursor with arg of type"
                                       " <class 'unittests.mockqtwidgets.MockCursor'>\n"
                                       # "called dmla.update_albums_by_artist with args"
                                       # " (5, [(15, 'aa', 1, True, []), (0, 'bb', 2, False, [])])\n"
                                       "called build_album_name for"
                                       " `namespace(id=10, title='xxx', year=2000)`\n"
                                       "called app.restoreOverrideCursor\n"
                                       "called save_appdata with args"
                                       " ([{}, {'x': {'cname': ('xxx, 2000', 10)}}],)\n"
                                       "called ComboBox.currentIndex\n"
                                       "called CompareAlbums.refresh_screen with args (1,)\n")

def test_cmpalb_help(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee, 'workflows', {'cmpalb': 'wf'})
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.help()
    assert capsys.readouterr().out == "called QMessageBox.information with args `appname` `wf`\n"


# tests for new album dialog
def test_newalb_init(monkeypatch, capsys, expected_output):
    def mock_init(self, *args):
        print('called QWidget.__init__')
    def mock_setLayout(self, widget):
        print(f'called QWidget.setLayout with arg of type {type(widget)}')
    def mock_setTitle(self, text):
        print(f'called QDialog.setWindowTitle with arg `{text}`')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setLayout)
    monkeypatch.setattr(testee.qtw.QWidget, 'setWindowTitle', mock_setTitle)
    parent = testee.qtw.QWidget()
    assert capsys.readouterr().out == 'called QWidget.__init__\n'
    parent.appname = 'appname'
    monkeypatch.setattr(testee.qtw, 'QDialog', mockqtw.MockDialog)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGrid)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
    testobj = testee.NewAlbumDialog(parent)
    bindings = {'reject': testobj.reject, 'update': testobj.update, 'me': testobj, 'text_n': '',
                'text_y': ''}
    assert capsys.readouterr().out == expected_output['new_album'].format(**bindings)

    testobj = testee.NewAlbumDialog(parent, name='x')
    bindings = {'reject': testobj.reject, 'update': testobj.update, 'me': testobj, 'text_n': 'x',
                'text_y': ''}
    assert capsys.readouterr().out == expected_output['new_album'].format(**bindings)

    testobj = testee.NewAlbumDialog(parent, year='x')
    bindings = {'reject': testobj.reject, 'update': testobj.update, 'me': testobj, 'text_n': '',
                'text_y': 'x'}
    assert capsys.readouterr().out == expected_output['new_album'].format(**bindings)

def test_newalb_update(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called NewAlbumDialog.__init__')
    def mock_accept(self, *args):
        print('called NewAlbumDialog.accept')
    counter = 0
    def mock_text_alles(*args):
        nonlocal counter
        counter += 1
        print('called QLineEdit.text')
        return ('', 'x', 'y')[counter]
    def mock_text_niks(*args):
        return ''
    def mock_text_year(*args):
        nonlocal counter
        counter += 1
        return ('', '', 'y')[counter]
    def mock_text_name(*args):
        nonlocal counter
        counter += 1
        return ('', 'x', '')[counter]
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee.NewAlbumDialog, '__init__', mock_init)
    monkeypatch.setattr(testee.NewAlbumDialog, 'accept', mock_accept)
    testobj = testee.NewAlbumDialog()
    mock_parent = types.SimpleNamespace(data=())
    monkeypatch.setattr(testobj, 'parent', lambda *x: mock_parent)
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_alles)
    testobj.first_name = mockqtw.MockLineEdit()
    testobj.last_name = mockqtw.MockLineEdit()
    testobj.is_concert = mockqtw.MockCheckBox()
    assert capsys.readouterr().out == ('called NewAlbumDialog.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called LineEdit.__init__\n'
                                       'called CheckBox.__init__\n')
    testobj.update()
    assert testobj.parent().data == ('x', 'y', False)
    assert capsys.readouterr().out == ('called QLineEdit.text\n'
                                       'called QLineEdit.text\n'
                                       'called CheckBox.isChecked\n'
                                       'called NewAlbumDialog.accept\n')

    testobj.parent().data = ()
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_niks)
    monkeypatch.setattr(mockqtw.MockCheckBox, 'isChecked', lambda *x: True)
    testobj.update()
    assert testobj.parent().data == ()
    assert capsys.readouterr().out == ('called QMessageBox.information with args `AlbumsMatcher`'
                                       ' `Enter at least the name or press `Cancel``\n')

    counter = 0
    testobj.parent().data = ()
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_name)
    testobj.update()
    assert testobj.parent().data == ('x', '', True)
    assert capsys.readouterr().out == 'called NewAlbumDialog.accept\n'

    counter = 0
    testobj.parent().data = ()
    monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text_year)
    testobj.update()
    assert testobj.parent().data == ()
    assert capsys.readouterr().out == ('called QMessageBox.information with args `AlbumsMatcher`'
                                       ' `Enter at least the name or press `Cancel``\n')


# tests for compare tracks tab
def setup_cmptrk(monkeypatch, capsys, widgets=True):
    def mock_init(self, parent):
        print('called QWidget.__init__')
        self._parent = parent
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    testparent = MockMainFrame()
    testobj = testee.CompareTracks(testparent)
    output = 'called MainFrame.__init__\ncalled QApplication.__init__\ncalled QWidget.__init__\n'
    if widgets:
        testobj.artists_list = mockqtw.MockComboBox()
        testobj.albums_list = mockqtw.MockComboBox()
        testobj.clementine_tracks = mockqtw.MockTree()
        testobj.albums_tracks = mockqtw.MockTree()
        output += ('called ComboBox.__init__\ncalled ComboBox.__init__\n'
                   'called QTreeWidget.__init__\ncalled QTreeWidget.__init__\n')
    assert capsys.readouterr().out == output
    return testobj

def test_cmptrk_create_widgets(monkeypatch, capsys, expected_output):
    def mock_get(*args):
        pass
    def mock_get_t(*args):
        pass
    def mock_popup(*args):
        pass
    def mock_setlayout(win):
        print(f'called CompareAlbums.setLayout with arg of type {type(win)}')
    def mock_save(*args):
        pass
    def mock_copy(*args):
        pass
    def mock_unlink(*args):
        pass
    def mock_next(*args):
        pass
    def mock_next_2(*args):
        pass
    def mock_prev(*args):
        pass
    def mock_prev_2(*args):
        pass
    def mock_help(*args):
        pass
    # def mock_find(*args):
    #     pass
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBox)
    monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBox)
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGrid)
    monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockButton)
    monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
    monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTree)
    monkeypatch.setattr(testee.qtw, 'QHeaderView', mockqtw.MockHeader)
    monkeypatch.setattr(testee.core, 'QSize', mockqtw.MockSize)
    monkeypatch.setattr(testee, 'popuptext', mock_popup)
    testobj = setup_cmptrk(monkeypatch, capsys, widgets=False)
    testobj._parent.title = 'apptitle'
    testobj._parent.down_icon = 'down_icon'
    testobj._parent.up_icon = 'up_icon'
    monkeypatch.setattr(testobj, 'setLayout', mock_setlayout)
    monkeypatch.setattr(testobj, 'get_albums', mock_get)
    monkeypatch.setattr(testobj, 'get_tracks', mock_get_t)
    monkeypatch.setattr(testobj, 'save_all', mock_save)
    monkeypatch.setattr(testobj, 'copy_tracks', mock_copy)
    monkeypatch.setattr(testobj, 'unlink', mock_unlink)
    monkeypatch.setattr(testobj, 'next_artist', mock_next)
    monkeypatch.setattr(testobj, 'next_album', mock_next_2)
    monkeypatch.setattr(testobj, 'prev_artist', mock_prev)
    monkeypatch.setattr(testobj, 'prev_album', mock_prev_2)
    monkeypatch.setattr(testobj, 'help', mock_help)
    # monkeypatch.setattr(testobj, 'find_album', mock_find)
    testobj.create_widgets()
    assert testobj.artist_index == 0
    assert testobj.album_index == 0
    bindings = {'me': testobj,
                'get_albums': testobj.get_albums,
                'get_tracks': testobj.get_tracks,
                'popuptext': testee.popuptext,
                'copy_tracks': testobj.copy_tracks,
                'unlink': testobj.unlink,
                'save_all': testobj.save_all,
                'next_artist': testobj.next_artist,
                'next_album': testobj.next_album,
                'prev_artist': testobj.prev_artist,
                'prev_album': testobj.prev_album,
                'help': testobj.help,
                # 'find_album': testobj.find_album
                }
    assert capsys.readouterr().out == expected_output['compare_tracks'].format(**bindings)

def test_cmptrk_create_actions(monkeypatch, capsys, expected_output):
    def mock_add(arg):
        print(f'called CompareArtists.addAction')
    monkeypatch.setattr(testee.qtw, 'QAction', mockqtw.MockAction)
    testobj = setup_cmptrk(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'addAction', mock_add)
    testobj.create_actions()
    bindings = {'me': testobj,
                'help': testobj.help,
                'selart': testobj.artists_list.setFocus,
                'selalb': testobj.albums_list.setFocus,
                'nextart': testobj.next_artist,
                'nextalb': testobj.next_album,
                'prevart': testobj.prev_artist,
                'prevalb': testobj.prev_album,
                'copy': testobj.copy_tracks,
                'unlink': testobj.unlink,
                'save': testobj.save_all}
    assert capsys.readouterr().out == expected_output['compare_tracks_actions'].format(**bindings)

def test_cmptrk_refresh_screen(monkeypatch, capsys):
    def mock_artists():
        print('called dmlc.list_artists')
        return [{'artist': 'xx', 'id': 'qq'}]
    counter = 0
    def mock_setindex(num):
        nonlocal counter
        counter += 1
        if counter == 1:
            print('called TreeWidget.setCurrentIndex')
            raise TypeError
        else:
            print(f'called TreeWidget.setCurrentIndex with arg `{num}`')
    def mock_index(*args):
        raise ValueError
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.b_save = mockqtw.MockButton()
    assert capsys.readouterr().out == 'called PushButton.__init__ with args ()\n'
    testobj._parent.artist_map = {}
    testobj._parent.albums_map = {}
    assert testobj.refresh_screen() == 'Please match some artists and albums first'
    assert not testobj.modified
    assert capsys.readouterr().out == 'called PushButton.setEnabled with arg `False`\n'
    monkeypatch.setattr(testee.dmlc, 'list_artists', mock_artists)
    testobj.modified = True
    testobj._parent.artist_map = {'xx': 'yy'}
    testobj._parent.albums_map = {'xx': ['zz']}
    assert testobj.refresh_screen(modifyoff=False) == ''
    assert testobj.modified
    assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                       "called dmlc.list_artists\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `['xx']`\n")
    testobj.modified = False
    assert testobj.refresh_screen(album='yy', modifyoff=False) == ''
    assert not testobj.modified
    assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n"
                                       "called dmlc.list_artists\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `['xx']`\n"
                                       "called ComboBox.setCurrentIndex to `yy`\n")
    monkeypatch.setattr(testobj.artists_list, 'setCurrentIndex', mock_setindex)
    assert testobj.refresh_screen(artist='xx') == ''
    assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n"
                                       "called dmlc.list_artists\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `['xx']`\n"
                                       "called TreeWidget.setCurrentIndex\n"
                                       "called TreeWidget.setCurrentIndex with arg `0`\n")
    monkeypatch.setattr(testee.dmlc, 'list_artists', lambda *x: [])
    counter = 0
    assert testobj.refresh_screen(artist='xx') == 'This artist has not been matched yet'
    assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n"
                                       "called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `[]`\n"
                                       "called TreeWidget.setCurrentIndex\n")

def test_cmptrk_get_albums(monkeypatch, capsys):
    def mock_update():
        print('called CompareTracks.update_navigation_buttons')
    testobj = setup_cmptrk(monkeypatch, capsys)
    monkeypatch.setattr(testee.dmlc, 'list_albums', lambda *x: [])
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    testobj.get_albums()
    assert testobj.artist == '.'
    assert testobj.c_albums == []
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called ComboBox.clear\n'
                                       'called ComboBox.addItems with arg `[]`\n'
                                       'called CompareTracks.update_navigation_buttons\n')

    testobj.albums_map = {'xx': 'yy', 'aa': 'bb'}
    monkeypatch.setattr(testobj.artists_list, 'currentText', lambda *x: 'xx')
    monkeypatch.setattr(testee.dmlc, 'list_albums', lambda *x: [{'album': 'yy'}, {'album': 'zz'}])
    testobj.get_albums()
    assert testobj.artist == 'xx'
    assert testobj.c_albums == ['yy', 'zz']
    assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                       "called ComboBox.addItems with arg `['yy', 'zz']`\n"
                                       "called CompareTracks.update_navigation_buttons\n")

def test_cmptrk_update_navigation_buttons(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.next_artist_button = mockqtw.MockButton()
    testobj.prev_artist_button = mockqtw.MockButton()
    testobj.next_album_button = mockqtw.MockButton()
    testobj.prev_album_button = mockqtw.MockButton()
    assert capsys.readouterr().out == ('called PushButton.__init__ with args ()\n'
                                       'called PushButton.__init__ with args ()\n'
                                       'called PushButton.__init__ with args ()\n'
                                       'called PushButton.__init__ with args ()\n')
    monkeypatch.setattr(testobj.artists_list, 'currentIndex', lambda *x: 0)
    monkeypatch.setattr(testobj.albums_list, 'currentIndex', lambda *x: 0)
    testobj.c_artists = ['x', 'y']
    testobj.c_albums = ['a', 'b']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `False`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `False`\n")

    monkeypatch.setattr(testobj.artists_list, 'currentIndex', lambda *x: 1)
    monkeypatch.setattr(testobj.albums_list, 'currentIndex', lambda *x: 1)
    testobj.c_artists = ['x']
    testobj.c_albums = ['y']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `True`\n")

    testobj.c_artists = ['x', 'y']
    testobj.c_albums = ['a', 'b']
    testobj.update_navigation_buttons()
    assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `False`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `True`\n"
                                       "called PushButton.setEnabled with arg `False`\n")

def test_cmptrk_get_tracks(monkeypatch, capsys):
    def mock_infobox(*args):
        print('called MessageBox.information with args', args)
    def mock_read(*args):
        print('called read_album_tracks with args', args)
        return ['a_track'], ['c_track']
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_infobox)
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.b_copy = mockqtw.MockButton()
    assert capsys.readouterr().out == 'called PushButton.__init__ with args ()\n'
    testobj.a_album = 'x'
    testobj.get_tracks()
    assert testobj.c_album == '.'
    assert testobj.a_album == 'x'
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       'called ComboBox.count\n')
    monkeypatch.setattr(testobj.artists_list, 'count', lambda *x: 1)
    testobj.get_tracks()
    assert testobj.c_album == '.'
    assert testobj.a_album == 'x'
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       'called ComboBox.count\n')
    monkeypatch.setattr(testobj.albums_list, 'count', lambda *x: 1)
    testobj.artist = 'xx'
    testobj.albums_map = {'xx': {}}
    testobj.get_tracks()
    assert testobj.c_album == '.'
    assert testobj.a_album == 'x'
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       f"called MessageBox.information with args ({testobj},"
                                       " 'appname', 'No (matched) albums for this artist')\n")
    testobj.albums_map = {'xx': {'yy': ()}}
    testobj.get_tracks()
    assert testobj.c_album == '.'
    assert testobj.a_album == 'x'
    assert capsys.readouterr().out == ('called ComboBox.currentText\n'
                                       'called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       f"called MessageBox.information with args ({testobj},"
                                       " 'appname', 'This album has not been matched yet')\n")
    monkeypatch.setattr(testobj.albums_list, 'currentText', lambda *x: 'yy')
    testobj.albums_map = {'xx': {'yy': ('aa', 'bb')}}
    monkeypatch.setattr(testee, 'read_album_tracks', mock_read)
    testobj.get_tracks()
    assert testobj.c_album == 'yy'
    assert testobj.a_album == 'bb'
    assert capsys.readouterr().out == ('called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       "called read_album_tracks with args ('bb', 'xx', 'yy')\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       'called PushButton.setEnabled with arg `True`\n')
    # 1180: len(c_tracks) != len(a_tracks)
    monkeypatch.setattr(testee, 'read_album_tracks', lambda *x: (['a'], []))
    testobj.get_tracks()
    assert testobj.c_album == 'yy'
    assert testobj.a_album == 'bb'
    assert capsys.readouterr().out == ('called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       'called PushButton.setEnabled with arg `True`\n')
    # 1190-91: IndexError (not found) bij vergelijking r. 1185
    # volgens mij kan dit niet (meer)
    # monkeypatch.setattr(testee, 'read_album_tracks', lambda *x: (['a', 'b'], ['c']))
    # breakpoint()
    # testobj.get_tracks()
    # assert testobj.c_album == 'yy'
    # assert testobj.a_album == 'bb'
    # assert capsys.readouterr().out == ('called QTreeWidget.clear\n'
    #                                    'called QTreeWidget.clear\n'
    #                                    'called PushButton.setEnabled with arg `False`\n')
    # conditie op r. 1188 deel 1:  a begint met volledige c  geeft True
    monkeypatch.setattr(testee, 'read_album_tracks', lambda *x: (['aa'], ['a']))
    testobj.get_tracks()
    assert testobj.c_album == 'yy'
    assert testobj.a_album == 'bb'
    assert capsys.readouterr().out == ('called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       'called PushButton.setEnabled with arg `False`\n')
    # conditie op r. 1188 deel 2:  eerste letter van c is volledige a  geeft True
    monkeypatch.setattr(testee, 'read_album_tracks', lambda *x: (['a'], ['aa']))
    testobj.get_tracks()
    assert testobj.c_album == 'yy'
    assert testobj.a_album == 'bb'
    assert capsys.readouterr().out == ('called QTreeWidget.clear\n'
                                       'called QTreeWidget.clear\n'
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       "called QTreeWidget.addTopLevelItem with arg of type"
                                       " `<class 'PyQt5.QtWidgets.QTreeWidgetItem'>`\n"
                                       'called PushButton.setEnabled with arg `False`\n')

def test_cmptrk_next_artist(monkeypatch, capsys):
    def mock_update():
        print('called CompareTracks.update_navigation_buttons')
    testobj = setup_cmptrk(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    monkeypatch.setattr(testobj.artists_list, 'count', lambda *x: 2)
    monkeypatch.setattr(testobj.artists_list, 'currentIndex', lambda *x: 0)
    testobj.next_artist()
    assert capsys.readouterr().out == ('called ComboBox.setCurrentIndex to `1`\n'
                                       'called CompareTracks.update_navigation_buttons\n')
    monkeypatch.setattr(testobj.artists_list, 'currentIndex', lambda *x: 1)
    testobj.next_artist()
    assert capsys.readouterr().out == ''

def test_cmptrk_prev_artist(monkeypatch, capsys):
    def mock_update():
        print('called CompareTracks.update_navigation_buttons')
    testobj = setup_cmptrk(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    monkeypatch.setattr(testobj.artists_list, 'count', lambda *x: 1)
    monkeypatch.setattr(testobj.artists_list, 'currentIndex', lambda *x: 1)
    testobj.prev_artist()
    assert capsys.readouterr().out == ('called ComboBox.setCurrentIndex to `0`\n'
                                       'called CompareTracks.update_navigation_buttons\n')
    monkeypatch.setattr(testobj.artists_list, 'currentIndex', lambda *x: 0)
    testobj.prev_artist()
    assert capsys.readouterr().out == ''

def test_cmptrk_next_album(monkeypatch, capsys):
    def mock_update():
        print('called CompareTracks.update_navigation_buttons')
    testobj = setup_cmptrk(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    monkeypatch.setattr(testobj.albums_list, 'count', lambda *x: 2)
    monkeypatch.setattr(testobj.albums_list, 'currentIndex', lambda *x: 0)
    testobj.next_album()
    assert capsys.readouterr().out == ('called ComboBox.setCurrentIndex to `1`\n'
                                       'called CompareTracks.update_navigation_buttons\n')
    monkeypatch.setattr(testobj.albums_list, 'currentIndex', lambda *x: 1)
    testobj.next_album()
    assert capsys.readouterr().out == ''

def test_cmptrk_prev_album(monkeypatch, capsys):
    def mock_update():
        print('called CompareTracks.update_navigation_buttons')
    testobj = setup_cmptrk(monkeypatch, capsys)
    monkeypatch.setattr(testobj, 'update_navigation_buttons', mock_update)
    monkeypatch.setattr(testobj.albums_list, 'count', lambda *x: 1)
    monkeypatch.setattr(testobj.albums_list, 'currentIndex', lambda *x: 1)
    testobj.prev_album()
    assert capsys.readouterr().out == ('called ComboBox.setCurrentIndex to `0`\n'
                                       'called CompareTracks.update_navigation_buttons\n')
    monkeypatch.setattr(testobj.albums_list, 'currentIndex', lambda *x: 0)
    testobj.prev_album()
    assert capsys.readouterr().out == ''

def test_cmptrk_copy_tracks(monkeypatch, capsys):
    def mock_update(*args):
        print('called dmla.update_album_tracknames with args', args)
    def mock_text(*args):
        return 'itemtext'
    def mock_getitem(arg):
        print(f'called TreeWidget.topLevelItem with index {arg}')
        return types.SimpleNamespace(text=mock_text)
    def mock_refresh(*args):
        print(f'called CompareTracks.refresh_screen with args', args)
    monkeypatch.setattr(testee.dmla, 'update_album_tracknames', mock_update)
    monkeypatch.setattr(testee.core.Qt, 'WaitCursor', 'waitcursor')
    monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.a_album = {'x': 'y'}
    testobj.copy_tracks()
    assert capsys.readouterr().out == 'called TreeWidget.topLevelItemCount\n'
    monkeypatch.setattr(testobj.clementine_tracks, 'topLevelItemCount', lambda *x: 1)
    monkeypatch.setattr(testobj.clementine_tracks, 'topLevelItem', mock_getitem)
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    testobj.copy_tracks()
    assert capsys.readouterr().out == ('called TreeWidget.topLevelItem with index 0\n'
                                       'called QCursor with arg waitcursor\n'
                                       'called app.setOverrideCursor with arg of type'
                                       " <class 'unittests.mockqtwidgets.MockCursor'>\n"
                                       'called dmla.update_album_tracknames with args'
                                       " ({'x': 'y'}, [(1, 'itemtext')])\n"
                                       'called app.restoreOverrideCursor\n'
                                       'called ComboBox.currentIndex\n'
                                       'called ComboBox.currentIndex\n'
                                       'called CompareTracks.refresh_screen with args (1, 1)\n')

def test_cmptrk_unlink(monkeypatch, capsys):
    def mock_unlink(*args):
        print('called dmla.unlink_album with args', args)
    def mock_refresh(*args, **kwargs):
        print(f'called CompareTracks.refresh_screen with args', args, kwargs)
    monkeypatch.setattr(testee.dmla, 'unlink_album', mock_unlink)
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.artist = 'xx'
    testobj.c_album = 'yy'
    testobj.a_album = 'zz'
    testobj.albums_map = {'xx': {'yy': ('aa', 'bb')}}
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    testobj.unlink()
    assert testobj.albums_map == {'xx': {}}
    assert testobj.modified
    assert capsys.readouterr().out == ("called dmla.unlink_album with args ('zz',)\n"
                                       "called ComboBox.currentIndex\n"
                                       "called ComboBox.currentIndex\n"
                                       "called CompareTracks.refresh_screen with args"
                                       " (1, 1) {'modifyoff': False}\n")
    testobj.albums_map = {'xx': {'yy': ('aa', 'bb'), 'zz': ('qq', 'bb')}}
    testobj.unlink()
    assert testobj.albums_map == {'xx': {'zz': ('qq', 'bb')}}
    assert testobj.modified
    assert capsys.readouterr().out == ("called ComboBox.currentIndex\n"
                                       "called ComboBox.currentIndex\n"
                                       "called CompareTracks.refresh_screen with args"
                                       " (1, 1) {'modifyoff': False}\n")

def test_cmptrk_save_all(monkeypatch, capsys):
    def mock_save(*args):
        print('called save_appdata with args', args)
    def mock_refresh(*args):
        print('called CompareTracks.refresh_screen with args', args)
    testobj = setup_cmptrk(monkeypatch, capsys)
    monkeypatch.setattr(testee, 'save_appdata', mock_save)
    monkeypatch.setattr(testobj, 'refresh_screen', mock_refresh)
    testobj._parent.artist_map = {'q': 'r'}
    testobj.albums_map = {'x': {'y': 'z'}, 'a': {}, 'b': None}
    testobj.save_all()
    assert testobj._parent.albums_map == {'x': {'y': 'z'}, 'a': {}, 'b': {}}
    assert capsys.readouterr().out == ("called save_appdata with args"
                                       " ([{'q': 'r'}, {'x': {'y': 'z'}, 'a': {}, 'b': {}}],)\n"
                                       "called ComboBox.currentIndex\n"
                                       "called ComboBox.currentIndex\n"
                                       "called CompareTracks.refresh_screen with args (1, 1)\n")

def test_cmptrk_help(monkeypatch, capsys):
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    monkeypatch.setattr(testee, 'workflows', {'cmptrk': 'wf'})
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.help()
    assert capsys.readouterr().out == "called QMessageBox.information with args `appname` `wf`\n"
