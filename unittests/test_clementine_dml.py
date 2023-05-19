import pytest
import apps.clementine_dml as testee


class MockCursor(testee.sqlite3.Cursor):
    def execute(self, *args):
        print('executing', *args)
        return ({'x': 'a', 'y': 'b'},)


class MockConnection(testee.sqlite3.Connection):
    def cursor(self, *args, **kwargs):
        return MockCursor(self, *args, **kwargs)
    def commit(self, *args):
        print('executing commit')
    def close(self, *args):
        print('executing close')


def test_retrieve(monkeypatch, capsys):
    def mock_connect(*args):
        print("connecting to database identified by '{}'".format(args[0]))
        return MockConnection(*args)
    monkeypatch.setattr(testee.sqlite3, 'connect', mock_connect)
    assert testee.retrieve('db', 'query', 'parms') == [{'x': 'a', 'y': 'b'}]
    assert capsys.readouterr().out == ("connecting to database identified by 'db'\n"
                                       'executing query parms\n')


def mock_retrieve(db, query, parms):
    return f'called retrieve with args `{db}`, `{query}`, {parms}'

def test_list_artists(monkeypatch):
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.list_artists('db') == (
            "called retrieve with args `db`,"
            " `select distinct artist from songs where unavailable = '0' order by artist;`, ()")


def test_list_albums(monkeypatch):
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.list_albums('db', 'artist') == (
            "called retrieve with args `db`,"
            " `select distinct album, year from songs where artist = ? and unavailable = '0';`,"
            " ('artist',)")


def test_list_album_covers(monkeypatch, capsys):
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.list_album_covers('db') == (
            'called retrieve with args `db`,'
            ' `select distinct artist, album, art_automatic, art_manual from songs'
            ' order by artist, album`, []')
    assert testee.list_album_covers('db', 'artist', 'album', True) == (
            'called retrieve with args `db`,'
            ' `select artist, album, track, art_automatic, art_manual from songs'
            ' where artist = ? and album = ?`,'
            " ['artist', 'album']")


def test_list_tracks_for_artist(monkeypatch):
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.list_tracks_for_artist('db', 'artist') == (
            "called retrieve with args `db`,"
            " `select rowid, album, disc, track, title, filename from songs where "
            "artist = ? order by album, disc, track;`, ('artist',)")


def test_list_tracks_for_album(monkeypatch):
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.list_tracks_for_album('db', 'artist', 'album') == (
            "called retrieve with args `db`,"
            " `select rowid, track, title from songs where artist = ? and album = ? "
            "and unavailable = '0' order by disc, track;`, ('artist', 'album')")
