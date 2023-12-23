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
        print(f"connecting to database identified by '{args[0]}'")
        return MockConnection(*args)
    monkeypatch.setattr(testee, 'DB', 'db')
    monkeypatch.setattr(testee.sqlite3, 'connect', mock_connect)
    # assert testee.retrieve('db', 'query', 'parms') == [{'x': 'a', 'y': 'b'}]
    assert testee.execute_query('query', 'parms') == [{'x': 'a', 'y': 'b'}]
    assert capsys.readouterr().out == ("connecting to database identified by 'db'\n"
                                       'executing query parms\n')
    # 'executing close\n')


def test_get_artists_lists(monkeypatch, capsys):
    def mock_execute_query(query, parms):
        print(f'called execute_query with args `{query}` `{parms}`')
        return [{'ArtistID': 2, 'Name': 'A'}, {'ArtistID': 1, 'Name': 'B'}]
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    assert testee.get_artists_lists() == ([2, 1], ['A', 'B'])
    assert capsys.readouterr().out == ("called execute_query with args `select ArtistID, Name"
                                       " from coreartists order by Name;` `()`\n")


def test_get_albums_lists(monkeypatch, capsys):
    def mock_execute_query(query, parms):
        print(f'called execute_query with args `{query}` `{parms}`')
        return [{'AlbumID': 2, 'Title': 'A'}, {'AlbumID': 1, 'Title': 'B'}]
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    assert testee.get_albums_lists('artist') == ([2, 1], ['A', 'B'])
    assert capsys.readouterr().out == ("called execute_query with args `select AlbumID, Title"
                                       " from corealbums where ArtistID = ?` `('artist',)`\n")


def test_get_album_cover(monkeypatch, capsys):
    def mock_execute_query(query, parms):
        print(f'called execute_query with args `{query}` `{parms}`')
        return [{'Name': 'X', 'Title': 'Y', 'ArtworkID': 'xxx'}]
    def mock_iterdir(*args):
        return [testee.pathlib.Path('here/where'), testee.pathlib.Path('here/there')]
    counter = 0
    def mock_exists(*args):
        print('called path.exists with args', args)
        nonlocal counter
        counter += 1
        return counter != 1  # False if counter == 1 else True
    def mock_is_dir(*args):
        print('called path.is_dir with args', args)
        nonlocal counter
        counter += 1
        return counter > 2  # False if counter <= 2 else True
    monkeypatch.setattr(testee, 'artworkpath', testee.pathlib.Path('here'))
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda *x: True)
    assert testee.get_album_cover() == 'here/xxx.jpg'
    assert capsys.readouterr().out == ("called execute_query with args"
            ' `select t1.Name, t2.Title, t2.ArtworkID from coreartists as t1'
            ' inner join corealbums as t2 on t1.ArtistID = t2.ArtistID'
            ' order by t1.Name, t2.Title` `()`\n')
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iterdir)
    monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists)
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_is_dir)
    assert testee.get_album_cover('artist', 'album') == 'here/there/xxx.jpg'
    assert capsys.readouterr().out == ("called execute_query with args"
            " `select t1.Name, t2.Title, t2.ArtworkID from coreartists as t1"
            " inner join corealbums as t2 on t1.ArtistID = t2.ArtistID"
            " where t2.AlbumID = ? and t1.ArtistID = ?` `('album', 'artist')`\n"
            "called path.exists with args (PosixPath('here/xxx.jpg'),)\n"
            "called path.is_dir with args (PosixPath('here/where'),)\n"
            "called path.is_dir with args (PosixPath('here/there'),)\n"
            "called path.exists with args (PosixPath('here/there/xxx.jpg'),)\n")
    counter = 0
    monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda *x: False)
    assert testee.get_album_cover('artist', 'album') == 'xxx.jpg'
    assert capsys.readouterr().out == ("called execute_query with args"
            " `select t1.Name, t2.Title, t2.ArtworkID from coreartists as t1"
            " inner join corealbums as t2 on t1.ArtistID = t2.ArtistID"
            " where t2.AlbumID = ? and t1.ArtistID = ?` `('album', 'artist')`\n"
            "called path.is_dir with args (PosixPath('here/where'),)\n"
            "called path.is_dir with args (PosixPath('here/there'),)\n")


def test_get_tracks_lists(monkeypatch, capsys):
    def mock_execute_query(query, parms):
        print(f'called execute_query with args `{query}` `{parms}`')
        return [{'TrackNumber': 1, 'Title': 'A'}, {'TrackNumber': 2, 'Title': 'B'}]
    monkeypatch.setattr(testee, 'execute_query', mock_execute_query)
    assert testee.get_tracks_lists('artist', 'album') == ([1, 2], ['A', 'B'])
    assert capsys.readouterr().out == ("called execute_query with args"
            " `select TrackNumber, Title from coretracks where AlbumID = ?"
            " order by Disc, TrackNumber` `('album',)`\n")
