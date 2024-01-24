"""unittests for ./apps/clementine_dml.py
"""
import apps.clementine_dml as testee


class MockCursor(testee.sqlite3.Cursor):
    """stub for sqlite3.Cursor
    """
    def execute(self, *args):
        """stub
        """
        print('executing', *args)
        return ({'x': 'a', 'y': 'b'},)


class MockConnection(testee.sqlite3.Connection):
    """stub for sqlite3.Connetion
    """
    def cursor(self, *args, **kwargs):
        """stub
        """
        return MockCursor(self, *args, **kwargs)
    def commit(self, *args):
        """stub
        """
        print('executing commit')
    def close(self, *args):
        """stub
        """
        print('executing close')


def test_retrieve(monkeypatch, capsys):
    """unittest for clementine_dml.retrieve
    """
    def mock_connect(*args):
        """stub
        """
        print(f"connecting to database identified by '{args[0]}'")
        return MockConnection(*args)
    monkeypatch.setattr(testee, 'DB', 'db')
    monkeypatch.setattr(testee.sqlite3, 'connect', mock_connect)
    assert testee.retrieve('query', 'parms') == [{'x': 'a', 'y': 'b'}]
    assert capsys.readouterr().out == ("connecting to database identified by 'db'\n"
                                       'executing query parms\n')


# implicitely tests list_artists function
def test_get_artists_lists(monkeypatch, capsys):
    """unittest for clementine_dml.get_artists_lists
    """
    def mock_retrieve(query, parms):
        """stub
        """
        print(f'called retrieve with args `{query}`, {parms}')
        return [{'artist': 2}, {'artist': 1}]
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.get_artists_lists() == ([2, 1], [2, 1])
    assert capsys.readouterr().out == ("called retrieve with args"
            " `select distinct artist from songs where unavailable = '0' order by artist;`, ()\n")


# implicitely tests list_albums function
def test_get_albums_lists(monkeypatch, capsys):
    """unittest for clementine_dml.get_albums_lists
    """
    def mock_retrieve(query, parms):
        """stub
        """
        print(f'called retrieve with args `{query}`, {parms}')
        return [{'album': 2}, {'album': 1}]
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.get_albums_lists('artist') == ([2, 1], [2, 1])
    assert capsys.readouterr().out == ("called retrieve with args"
            " `select distinct album, year from songs where artist = ? and unavailable = '0';`,"
            " ('artist',)\n")


def test_get_album_cover(monkeypatch, capsys):
    """unittest for clementine_dml.get_album_cover
    """
    def mock_retrieve(query, parms):
        """stub
        """
        print(f'called retrieve with args `{query}`, {parms}')
        return [{'art_manual': 'x', 'art_automatic': 'y'}]
    def mock_retrieve_man_only(query, parms):
        """stub
        """
        print(f'called retrieve with args `{query}`, {parms}')
        return [{'art_manual': 'x', 'art_automatic': ''}]
    def mock_retrieve_auto_only(query, parms):
        """stub
        """
        print(f'called retrieve with args `{query}`, {parms}')
        return [{'art_manual': '', 'art_automatic': 'y'}]
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.get_album_cover() == 'x'
    assert capsys.readouterr().out == ('called retrieve with args'
            ' `select distinct artist, album, art_automatic, art_manual from songs'
            ' order by artist, album`, []\n')
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve_man_only)
    assert testee.get_album_cover('artist', 'album', True) == 'x'
    assert capsys.readouterr().out == ('called retrieve with args'
            ' `select artist, album, track, art_automatic, art_manual from songs'
            " where artist = ? and album = ?`, ['artist', 'album']\n")
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve_auto_only)
    assert testee.get_album_cover('artist', 'album', True) == 'y'
    assert capsys.readouterr().out == ('called retrieve with args'
            ' `select artist, album, track, art_automatic, art_manual from songs'
            " where artist = ? and album = ?`, ['artist', 'album']\n")


def test_list_tracks_for_artist(monkeypatch, capsys):
    """unittest for clementine_dml.list_tracks_for_artist
    """
    def mock_retrieve(query, parms):
        """stub
        """
        print(f'called retrieve with args `{query}`, {parms}')
        return [{'album': 2, 'title': 'A'}, {'album': 1, 'title': 'B'}]
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.list_tracks_for_artist('artist') == ([2, 1], ['A', 'B'])
    assert capsys.readouterr().out == ("called retrieve with args"
            " `select rowid, album, disc, track, title, filename from songs where "
            "artist = ? order by album, disc, track;`, ('artist',)\n")


# implicitely tests list_tracks function
def test_get_tracks_lists(monkeypatch, capsys):
    """unittest for clementine_dml.get_tracks_lists
    """
    def mock_retrieve(query, parms):
        """stub
        """
        print(f'called retrieve with args `{query}`, {parms}')
        return [{'title': 'A'}, {'title': 'B'}]
    monkeypatch.setattr(testee, 'retrieve', mock_retrieve)
    assert testee.get_tracks_lists('artist', 'album') == (['A', 'B'], ['A', 'B'])
    assert capsys.readouterr().out == ("called retrieve with args"
            " `select rowid, track, title from songs where artist = ? and album = ? "
            "and unavailable = '0' order by disc, track;`, ('artist', 'album')\n")
