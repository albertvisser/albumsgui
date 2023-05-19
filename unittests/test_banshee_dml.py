import pytest
import apps.banshee_dml as testee


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


def test_execute_query(monkeypatch, capsys):
    def mock_connect(*args):
        print("connecting to database identified by '{}'".format(args[0]))
        return MockConnection(*args)
    monkeypatch.setattr(testee.sqlite3, 'connect', mock_connect)
    # assert testee.retrieve('db', 'query', 'parms') == [{'x': 'a', 'y': 'b'}]
    assert testee.execute_query('db', 'query') == [{'x': 'a', 'y': 'b'}]
    assert capsys.readouterr().out == ("connecting to database identified by 'db'\n"
                                       'executing query\n')
    # 'executing close\n')


def mock_execute_query(db, query):
    return f'called execute_query with args `{db}`, `{query}`'


def test_list_artists(monkeypatch):
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    assert testee.list_artists('db') == ("called execute_query with args `db`,"
                                         " `select ArtistID, Name from coreartists order by Name;`")


def test_list_albums(monkeypatch):
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    assert testee.list_albums('db', 'artist') == ("called execute_query with args `db`,"
                                                  " `select AlbumID, Title from corealbums"
                                                  " where ArtistID = artist`")


def test_list_album_covers(monkeypatch):
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    assert testee.list_album_covers('db') == (
            "called execute_query with args `db`,"
            ' `select t1.Name, t2.Title, t2.ArtworkID from coreartists as t1'
            ' inner join corealbums as t2 on t1.ArtistID = t2.ArtistID'
            ' order by t1.Name, t2.Title`')
    assert testee.list_album_covers('db', 'artist', 'album') == (
            "called execute_query with args `db`,"
            ' `select t1.Name, t2.Title, t2.ArtworkID from coreartists as t1'
            ' inner join corealbums as t2 on t1.ArtistID = t2.ArtistID'
            ' where t2.AlbumID = album and t1.ArtistID = artist`')


def test_list_tracks(monkeypatch):
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    assert testee.list_tracks('db', 'album') == ("called execute_query with args `db`,"
                                                 " `select TrackNumber, Title from coretracks"
                                                 " where AlbumID = album order by Disc, TrackNumber`")
