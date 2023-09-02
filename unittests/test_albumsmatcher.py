import types
import pytest
import apps.albumsmatcher as testee
import unittests.mockqtwidgets as mockqtw
from unittests.buildscreen_output_fixture import expected_output


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


class MockMainFrame:
    next_icon = 'next_icon'  # nog even geen mockqtw.MockIcon()
    prev_icon = 'prev_icon'  # idem
    def __init__(self):
        print('called MainFrame.__init__')
        self.app = mockqtw.MockApplication()
        self.title = 'appname'


class MockNewArtistDialog:
    def __init__(self, parent, name):
        print('called NewArtistDialog.__init__'
              f' with parent of type `{type(parent)}` and name `{name}`')
    def exec_(self):
        return testee.qtw.QDialog.Rejected

def setup_cmpart(monkeypatch, capsys, widgets=True):
    def mock_init(self, parent):
        print('called QWidget.__init__')
        self._parent = parent
    # def mock_setlayout(self, layout):
    #     print(f'called QWidget.setLayout with arg of type {type(layout)}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    # monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
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
    testobj._parent.artist_map = {}
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
    assert capsys.readouterr().out == ('called TreeWidget.topLevelItem\n'
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


def _test_newart___init__(monkeypatch, capsys):
    testobj = testee.NewArtistDialog(parent, name='')

def _test_newart_update(monkeypatch, capsys):
    testobj.update()


def setup_cmpalb(monkeypatch, capsys):
    testobj = testee.CompareAlbums()
    return testobj

def _test_cmpalb_create_widgets(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.create_widgets()

def _test_cmpalb_create_actions(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.create_actions()

def _test_cmpalb_refresh_screen(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.refresh_screen(artist=None)

def _test_cmpalb_set_modified(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.set_modified(value)

def _test_cmpalb_update_navigation_buttons(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.update_navigation_buttons()

def _test_cmpalb_get_albums(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.get_albums()

def _test_cmpalb_focus_albums(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.focus_albums()

def _test_cmpalb_next_artist(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.next_artist()

def _test_cmpalb_prev_artist(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.prev_artist()

def _test_cmpalb_find_album(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.find_album()

def _test_cmpalb_add_album(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.add_album()

def _test_cmpalb_save_all(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.save_all()

def _test_cmpalb_help(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.help()


def _test_newalb___init__():
    testobj = testee.NewAlbumDialog(parent, name='', year='')

def _test_newalb_update(monkeypatch, capsys):
    testobj.update()


def setup_cmptrk(monkeypatch, capsys):
    testobj = testee.CompareTracks
    return testobj

def _test_cmptrk_create_widgets(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.create_widgets()

def _test_cmptrk_create_actions(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.create_actions()

def _test_cmptrk_refresh_screen(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.refresh_screen(artist=None, album=None, modifyoff=True)

def _test_cmptrk_get_albums(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.get_albums()

def _test_cmptrk_update_navigation_buttons(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.update_navigation_buttons()

def _test_cmptrk_get_tracks(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.get_tracks()

def _test_cmptrk_next_artist(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.next_artist()

def _test_cmptrk_prev_artist(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.prev_artist()

def _test_cmptrk_next_album(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.next_album()

def _test_cmptrk_prev_album(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.prev_album()

def _test_cmptrk_copy_tracks(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.copy_tracks()

def _test_cmptrk_unlink(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.unlink()

def _test_cmptrk_save_all(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.save_all()

def _test_cmptrk_help(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.help()


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


def setup_main(monkeypatch, capsys):
    monkeypatch.setattr(testee.MainFrame, '__init__', MockMainFrame.__init__)
    testobj = testee.MainFrame()
    assert capsys.readouterr().out == ('called MainFrame.__init__\n'
                                       'called QApplication.__init__\n')
    return testobj

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

class MockCmpArt:
    def __init__(self, arg):
        print(f'called CompareArtists.__init__ with arg `{arg}`')

class MockCmpAlb:
    def __init__(self, arg):
        print(f'called CompareAlbums.__init__ with arg `{arg}`')

class MockCmpTrk:
    def __init__(self, arg):
        print(f'called CompareTracks.__init__ with arg `{arg}`')

def test_setup_tabwidget(monkeypatch, capsys):
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
