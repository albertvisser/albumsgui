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

def setup_cmpart(monkeypatch, capsys):
    def mock_init(self, parent):
        print('called QWidget.__init__')
        self._parent = parent
    # def mock_setlayout(self, layout):
    #     print(f'called QWidget.setLayout with arg of type {type(layout)}')
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    # monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mock_setlayout)
    testparent = MockMainFrame()
    testobj = testee.CompareArtists(testparent)
    # we gebruiken hier _parent
    # monkeypatch.setattr(testobj, 'parent', lambda *x: testparent)
    assert capsys.readouterr().out == ('called MainFrame.__init__\n'
                                       'called QApplication.__init__\n'
                                       'called QWidget.__init__\n')
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
    testobj = setup_cmpart(monkeypatch, capsys)
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
#
def _test_cmpart_create_actions(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.create_actions()
#         for text, callback, keys in actions:
#
def _test_cmpart_refresh_screen(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.refresh_screen(artist=None)
#         for item in self.artist_list_c:
#             if item:
#         for item in self.artist_list_a:
#
def _test_cmpart_set_modified(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.set_modified(value)
#
def _test_cmpart_focus_artist(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.focus_artist(artist=None)
#         """select given artist or first unhandled one in left-hand side list
#         """
#         if artist:
#         else:
#         if test:
#         else:
#
def _test_cmpart_focus_next(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.focus_next()
#
def _test_cmpart_focus_prev(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.focus_prev()
#
def _test_cmpart_focus_item(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.focus_item(forward=True)
#         if test:
#             if not forward:
#             for item in test:
#                 if forward and index.row() > current.row()
#                 elif not forward and index.row() < current.row()
#         else:
#         if item:
#         else:
#
def _test_cmpart_check_deletable(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.check_deletable()
#         if item in self.new_artists:
#
def _test_cmpart_select_and_go(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.select_and_go()
#         if not item:
#         if not self.artist_map[search]:
#
def _test_cmpart_find_artist(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.find_artist()
#         if not item:
#             return
#         if self.artist_map[item.text(0)]:
#             if ok == qtw.QMessageBox.No:
#                 return
#         try:
#             found = self.lookup[search]
#         except KeyError:
#             if len(test) == 1:
#             else:
#                 try:
#                     found = self.lookup[search]
#                 except KeyError:
#         if found:
#             for a_item in find:  # only keep unmatched artists
#                 if a_item.text(2) in self.artist_map.values()
#                     continue
#             if ok:
#                 return
#
def _test_cmpart_update_item(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.update_item(new_item, from_item)
#         if nxt:
#
def _test_cmpart_copy_artist(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.copy_artist()
#
def _test_cmpart_add_artist(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.add_artist()
#         if dlg != qtw.QDialog.Accepted:
#             return
#         if not item:
#             if result:
#         if not item:
#             return
#
#         if results:
#             if ok:
#         if not a_item:
#
def _test_cmpart_delete_artist(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.delete_artist()
#         if item is None:
#         if ok != qtw.QMessageBox.Ok:
#         try:
#             name = self.new_matches.pop(a_itemkey)
#         except KeyError:
#         if name and self.artist_map[name] == a_itemkey:
#
def _test_cmpart_save_all(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.save_all()
#         for i in range(self.albums_artists.topLevelItemCount()):
#         for key, value in new_keys.items()
#
def _test_cmpart_help(monkeypatch, capsys):
    testobj = setup_cmpart(monkeypatch, capsys)
    testobj.help()
#
#
def _test_newart___init__(monkeypatch, capsys):
    testobj = testee.NewArtistDialog(parent, name='')
#
def _test_newart_update(monkeypatch, capsys):
    testobj.update()
#         if not fname and not lname:
#
#
def setup_cmpalb(monkeypatch, capsys):
    testobj = testee.CompareAlbums()
    return testobj

def _test_cmpalb_create_widgets(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.create_widgets()
#
def _test_cmpalb_create_actions(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.create_actions()
#         for text, callback, keys in actions:
#
def _test_cmpalb_refresh_screen(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.refresh_screen(artist=None)
#         if self._parent.artist_map:
#         else:
#             return "Please match some artists first"
#         for ix in range(self.clementine_albums.topLevelItemCount()):
#             if item.text(1) == 'X':
#         if artist:
#             try:
#                 self.artist_list.setCurrentIndex(artist)
#             except TypeError:
#                 try:
#                     indx = self.c_artists.index(artist)
#                 except ValueError:
#                     qtw.QMessageBox.information(self._parent.title, "This "
#                                                 "artist has not been matched yet")
#                     return
#
def _test_cmpalb_set_modified(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.set_modified(value)
#
def _test_cmpalb_update_navigation_buttons(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.update_navigation_buttons()
#         if test == 0:
#         if test == len(self.c_artists) - 1:
#
def _test_cmpalb_get_albums(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.get_albums()
#         if self.artist_list.count() == 0:   # this happens when the panel is reshown
#         for name, year, id, *rest in self.albums_to_save[self.c_artist]:
#         for item, year in c_albums:
#             try:
#                 new.setText(1, str(self.albums_map[self.c_artist][item][1]))
#             except KeyError:
#         for item in a_albums:
#
def _test_cmpalb_focus_albums(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.focus_albums()
#         for ix in range(self.clementine_albums.topLevelItemCount()):
#             if not item.text(1):
#         else:
#
def _test_cmpalb_next_artist(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.next_artist()
#         if test < self.artist_list.count()
#
def _test_cmpalb_prev_artist(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.prev_artist()
#         if test >= 0:
#
def _test_cmpalb_find_album(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.find_album()
#         if not item:
#         if item.text(0) in self.albums_map[self.c_artist]:
#             if ok == qtw.QMessageBox.No:
#         for album in albums:
#             for a_item in self.albums_map[self.c_artist].values()
#                 if a_item[1] == test:
#             if not found:
#         if album_list:
#             if ok:
#                 if c_year:
#                     if c_year != a_year:
#                         if ok == qtw.QMessageBox.Yes:
#
def _test_cmpalb_update_item(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.update_item(new_item, from_item)
#         if nxt:
#
def _test_cmpalb_add_album(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.add_album()
#         if dlg != qtw.QDialog.Accepted:
#         if not item:
#             if result:
#         if not item:
#
#         if results:
#             if ok:
#         if not a_item:
#
def _test_cmpalb_save_all(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.save_all()
#         """save changes (additions) to Albums database
#         """
#         for key, albums in self.albums_to_update.items()
#         with wait_cursor(self._parent):
#             for artist, albumdata in self.albums_to_save.items()
#                 if not albumdata:
#                 for name, year, key, is_live, tracks in albumdata:
#                     if key == 'X':
#                 for c_name, value in self.albums_map[artist].items()
#                     try:
#                         test = albums_map_lookup[a_name]
#                     except KeyError:
#                     if id != test:
#
def _test_cmpalb_help(monkeypatch, capsys):
    testobj = setup_cmpalb(monkeypatch, capsys)
    testobj.help()
#
#
def _test_newalb___init__():
    testobj = testee.NewAlbumDialog(parent, name='', year='')
#
def _test_newalb_update(monkeypatch, capsys):
    testobj.update()
#         if not name:
#
#
def setup_cmptrk(monkeypatch, capsys):
    testobj = testee.CompareTracks
    return testobj

def _test_cmptrk_create_widgets(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.create_widgets()
#
def _test_cmptrk_create_actions(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.create_actions()
#         for text, callback, keys in actions:
#
def _test_cmptrk_refresh_screen(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.refresh_screen(artist=None, album=None, modifyoff=True)
#         if modifyoff:
#         if self._parent.artist_map:
#         else:
#         if artist:
#             try:
#                 self.artists_list.setCurrentIndex(artist)
#             except TypeError:
#                 try:
#                     indx = self.c_artists.index(artist)
#                 except ValueError:
#                     qtw.QMessageBox.information(self._parent.title, "This "
#                                                 "artist has not been matched yet")
#                     return
#         if album:
#         return ''
#
def _test_cmptrk_get_albums(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.get_albums()
#
def _test_cmptrk_update_navigation_buttons(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.update_navigation_buttons()
#         if test == 0:
#         if test == len(self.c_artists) - 1:
#         if test == 0:
#         if test == len(self.c_albums) - 1:
#
def _test_cmptrk_get_tracks(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.get_tracks()
#         if self.artists_list.count() == 0:  # this happens when the panel is reshown
#         if self.albums_list.count() == 0:   # this happens during screen buildup
#         if not self.albums_map[self.artist]:
#         try:
#             self.a_album = self.albums_map[self.artist][self.c_album][1]
#         except KeyError:
#         for item in c_tracks:
#         for item in a_tracks:
#         if len(c_tracks) != len(a_tracks):
#         else:
#             for ix, item in enumerate(a_tracks):
#                 try:
#                     if not (item.startswith(c_tracks[ix][0]) or c_tracks[ix][0].startswith(item)):
#                 except IndexError:
#
def _test_cmptrk_next_artist(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.next_artist()
#         if test < self.artists_list.count()
#
def _test_cmptrk_prev_artist(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.prev_artist()
#         if test >= 0:
#
def _test_cmptrk_next_album(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.next_album()
#         if test < self.albums_list.count()
#
def _test_cmptrk_prev_album(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.prev_album()
#         if test >= 0:
#
def _test_cmptrk_copy_tracks(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.copy_tracks()
#         for ix in range(self.clementine_tracks.topLevelItemCount()):
#         with wait_cursor(self._parent):
#
def _test_cmptrk_unlink(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.unlink()
#         for item in self.albums_map[self.artist].values()
#             if item[1] == album_id:
#         if not still_present:
#
def _test_cmptrk_save_all(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.save_all()
#
def _test_cmptrk_help(monkeypatch, capsys):
    testobj = setup_cmptrk(monkeypatch, capsys)
    testobj.help()
#
#
# class MainFrame(qtw.QMainWindow):
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
