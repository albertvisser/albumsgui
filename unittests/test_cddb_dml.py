"""testroutines voor dml voor CDDB database (winamp 5)
"""
import types
import pytest
import apps.cddb_dml as testee


def test_readstr():
    data = b'\x41\x48\x41\x00\x41\x41\x48\x00'
    assert testee.readstr(data, 0) == ('AHA', 4)
    assert testee.readstr(data, 1) == ('HA', 4)
    assert testee.readstr(data, 2) == ('A', 4)
    assert testee.readstr(data, 3) == ('', 4)
    assert testee.readstr(data, 4) == ('AAH', 8)


def test_disc(monkeypatch, capsys):
    counter = 0
    def mock_read(data, pos):
        nonlocal counter
        print(f'called readstr with args `{data}`, `{pos}`')
        counter += 1
        return [(), ('one', 2), ('two', 3), ('three', 4), ('four', 5),
                ('five', 6), ('six', 7), ('seven', 8)][counter]
    def mock_unpack(*args):
        print('called struct.unpack with args', args)
        return 2, 4
    monkeypatch.setattr(testee, 'readstr', mock_read)
    monkeypatch.setattr(testee.struct, 'unpack', mock_unpack)
    assert testee.disc('stufferdestuff', 1) == ('two',
                                                testee.Album(cddbid='three', title='one', jaar='',
                                                             genre=''),
                                                ['four', 'five'])
    assert capsys.readouterr().out == ("called readstr with args `stufferdestuff`, `1`\n"
                                       "called readstr with args `stufferdestuff`, `2`\n"
                                       "called readstr with args `stufferdestuff`, `3`\n"
                                       "called struct.unpack with args ('=L', 'ferd')\n"
                                       "called readstr with args `stufferdestuff`, `8`\n"
                                       "called readstr with args `stufferdestuff`, `5`\n")
    counter = 0
    assert testee.disc('stufferdestuff', 1, True) == ('two',
                                                      testee.Album(cddbid='five', title='one',
                                                                   jaar='four',
                                                                   genre='three'),
                                                      ['six', 'seven'])
    assert capsys.readouterr().out == ("called readstr with args `stufferdestuff`, `1`\n"
                                       "called readstr with args `stufferdestuff`, `2`\n"
                                       "called readstr with args `stufferdestuff`, `3`\n"
                                       "called readstr with args `stufferdestuff`, `4`\n"
                                       "called readstr with args `stufferdestuff`, `5`\n"
                                       "called struct.unpack with args ('=L', 'rdes')\n"
                                       "called readstr with args `stufferdestuff`, `10`\n"
                                       "called readstr with args `stufferdestuff`, `7`\n")


def test_cdinfo(monkeypatch, capsys):
    def mock_unpack(*args):
        print('called struct.unpack with args', args)
        return 'cdid', 1
    monkeypatch.setattr(testee.struct, 'unpack', mock_unpack)
    assert testee.cdinfo('testerdetest', 7) == ('cdid', 13)
    assert capsys.readouterr().out == "called struct.unpack with args ('=QL', 'etest')\n"


def test_cddbdata_init(monkeypatch, capsys):
    def mock_read(self, arg):
        print(f'called CDDBData.read with arg `{arg}`')
        return 'error_or_empty_string'
    monkeypatch.setattr(testee.CDDBData, 'read', mock_read)
    testobj = testee.CDDBData('filenaam')
    assert testobj.artists == {}
    assert testobj.albums == {}
    assert testobj.tracks == {}
    assert isinstance(testobj.artists, testee.collections.defaultdict)
    assert testobj.error == 'error_or_empty_string'
    assert capsys.readouterr().out == 'called CDDBData.read with arg `filenaam`\n'


def test_cddbdata_read(monkeypatch, capsys, tmp_path):
    counter = 0
    def mock_unpack(formatcode, data):
        nonlocal counter
        print(f'called struct_unpack with args (`{formatcode}`, `{data}`)')
        counter += 1
        if counter == 1:
            return (13, 240, 239, 190)
        return ((counter - 2) * 12,)
    def mock_unpack_2(formatcode, data):
        nonlocal counter
        print(f'called struct_unpack with args (`{formatcode}`, `{data}`)')
        counter += 1
        if counter == 1:
            return (14, 240, 239, 190)
        return ((counter - 1) * 12,)
    def mock_unpack_3(formatcode, data):
        nonlocal counter
        print(f'called struct_unpack with args (`{formatcode}`, `{data}`)')
        counter += 1
        if counter == 1:
            return (1, 1, 1, 1)
        return (counter * 12,)
    def mock_cdinfo(*args):
        print('called cdinfo with args', args)
        return int(args[1] / 12), args[1]
    def mock_disc(*args):
        print('called disc with args', args)
        return 'artist', types.SimpleNamespace(title='album'), 'tracklist'
    monkeypatch.setattr(testee.struct, 'unpack', mock_unpack)
    monkeypatch.setattr(testee, 'cdinfo', mock_cdinfo)
    monkeypatch.setattr(testee, 'disc', mock_disc)
    (tmp_path / 'albumsguitest').mkdir()
    cddbfile = (tmp_path / 'albumsguitest' / 'cddbdata')
    cddbfile.write_text('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    testobj = testee.CDDBData(str(cddbfile))
    assert testobj.error == ''
    assert testobj.artists == {'artist': [0, 1, 2]}
    assert testobj.albums == {0: 'album', 1: 'album', 2: 'album'}
    assert testobj.tracks == {0: 'tracklist', 1: 'tracklist', 2: 'tracklist'}
    assert capsys.readouterr().out == (
        "called struct_unpack with args (`4B`, `b'aaaa'`)\n"
        "called struct_unpack with args (`=L`, `b'aaaa'`)\n"
        "called cdinfo with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 0)\n"
        "called cdinfo with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 12)\n"
        "called cdinfo with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 24)\n"
        "called disc with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 0, False)\n"
        "called disc with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 12, False)\n"
        "called disc with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 24, False)\n")
    counter = 0
    monkeypatch.setattr(testee.struct, 'unpack', mock_unpack_2)
    testobj = testee.CDDBData(str(cddbfile))
    assert testobj.error == ''
    assert testobj.artists == {'artist': [ 1, 2]}
    assert testobj.albums == {1: 'album', 2: 'album'}
    assert testobj.tracks == {1: 'tracklist', 2: 'tracklist'}
    assert capsys.readouterr().out == (
        "called struct_unpack with args (`4B`, `b'aaaa'`)\n"
        "called struct_unpack with args (`=L`, `b'aaaa'`)\n"
        "called cdinfo with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 12)\n"
        "called cdinfo with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 24)\n"
        "called disc with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 12, True)\n"
        "called disc with args (b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 24, True)\n")
    counter = 0
    monkeypatch.setattr(testee.struct, 'unpack', mock_unpack_3)
    testobj = testee.CDDBData(str(cddbfile))
    assert testobj.error == 'Beginning of file does not look ok'
    assert testobj.artists == {}
    assert testobj.albums == {}
    assert testobj.tracks == {}
    assert capsys.readouterr().out == "called struct_unpack with args (`4B`, `b'aaaa'`)\n"

def test_cddbdata_list_artists(monkeypatch, capsys):
    def mock_read(self, arg):
        print(f'called CDDBData.read with arg `{arg}`')
    monkeypatch.setattr(testee.CDDBData, 'read', mock_read)
    testobj = testee.CDDBData('filenaam')
    testobj.artists = {'x': [1, 2, 3], 'y': [9, 8, 7]}
    assert testobj.list_artists() == ['x', 'y']
    assert capsys.readouterr().out == 'called CDDBData.read with arg `filenaam`\n'

def test_cddbdata_list_albums(monkeypatch, capsys):
    def mock_read(self, arg):
        print(f'called CDDBData.read with arg `{arg}`')
    monkeypatch.setattr(testee.CDDBData, 'read', mock_read)
    testobj = testee.CDDBData('filenaam')
    testobj.artists = {'x': [1, 2, 3], 'y': [9, 8, 7]}
    testobj.albums = {1: 'aaa', 2: 'bbb', 3: 'ccc', 7: 'ddd', 8: 'eee', 9: 'fff'}
    assert testobj.list_albums('x') == [(1, 'aaa'), (2, 'bbb'), (3, 'ccc')]
    assert capsys.readouterr().out == 'called CDDBData.read with arg `filenaam`\n'

def test_cddbdata_list_tracks(monkeypatch, capsys):
    def mock_read(self, arg):
        print(f'called CDDBData.read with arg `{arg}`')
    monkeypatch.setattr(testee.CDDBData, 'read', mock_read)
    testobj = testee.CDDBData('filenaam')
    testobj.tracks = {1: ['xxx', 'yyy', 'zzz'], 2: ['aaa', 'bbb']}
    assert testobj.list_tracks(1) == ['xxx', 'yyy', 'zzz']
    assert capsys.readouterr().out == 'called CDDBData.read with arg `filenaam`\n'


def test_get_artists_lists(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called CDDBData.__init__ with args', args)
    def mock_list(self):
        print('called CDDBData.list_artists')
        return ['x', 'y']
    monkeypatch.setattr(testee, 'DB', 'connect-string')
    monkeypatch.setattr(testee.CDDBData,'__init__', mock_init)
    monkeypatch.setattr(testee.CDDBData,'list_artists', mock_list)
    assert testee.get_artists_lists() == (['x', 'y'], ['x', 'y'])
    assert capsys.readouterr().out == ("called CDDBData.__init__ with args ('connect-string',)\n"
                                       "called CDDBData.list_artists\n")

def test_get_albums_lists(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called CDDBData.__init__ with args', args)
    def mock_list(self, *args):
        print('called CDDBData.list_albums with args', args)
        return [['x', 'xxx'], ['y', 'yyy']]
    monkeypatch.setattr(testee, 'DB', 'connect-string')
    monkeypatch.setattr(testee.CDDBData,'__init__', mock_init)
    monkeypatch.setattr(testee.CDDBData,'list_albums', mock_list)
    assert testee.get_albums_lists('qqq') == (['x', 'y'], ['xxx', 'yyy'])
    assert capsys.readouterr().out == ("called CDDBData.__init__ with args ('connect-string',)\n"
                                       "called CDDBData.list_albums with args ('qqq',)\n")

def test_get_tracks_lists(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called CDDBData.__init__ with args', args)
    def mock_list(self, *args):
        print('called CDDBData.list_tracks with args', args)
        return ['xxx', 'yyy', 'zzz']
    monkeypatch.setattr(testee, 'DB', 'connect-string')
    monkeypatch.setattr(testee.CDDBData,'__init__', mock_init)
    monkeypatch.setattr(testee.CDDBData,'list_tracks', mock_list)
    assert testee.get_tracks_lists('qqq', 'rrr') == ([0, 1, 2], ['xxx', 'yyy', 'zzz'])
    assert capsys.readouterr().out == ("called CDDBData.__init__ with args ('connect-string',)\n"
                                       "called CDDBData.list_tracks with args ('rrr',)\n")
