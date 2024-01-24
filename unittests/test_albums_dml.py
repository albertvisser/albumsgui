"""unittests for ./apps/albums_dml.py
"""
import sys
import os
import django
import pytest
sys.path.append('/home/albert/projects/albums')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albums.settings")
django.setup()
# from django.db.models import Q
# import albums.muziek.models as my
# from albums.muziek.helpers import s_keuzes, s_sorts, l_keuzes, l_sorts
import apps.albums_dml as testee


@pytest.mark.django_db
def test_get_artists_lists(monkeypatch, capsys):
    """unittest for albums_dml.get_artists_lists
    """
    def mock_list_artists():
        """stub
        """
        print('called dml.list_artists')
        # return [{'id': 2, 'first_name': 'a', 'last_name': 'band'},
        #         {'id': 1, 'first_name': '', 'last_name': 'players'}]
        artist = testee.my.Act.objects.create(first_name='a', last_name='band')
        artist2 = testee.my.Act.objects.create(last_name='players')
        artist3 = testee.my.Act.objects.create(first_name='Andy', last_name='Bendy')
        return (x for x in [artist, artist2, artist3])
    monkeypatch.setattr(testee, 'list_artists', mock_list_artists)
    assert testee.get_artists_lists() == ([1, 2, 3], ['a band', 'players', 'Andy Bendy'])
    assert capsys.readouterr().out == 'called dml.list_artists\n'


@pytest.mark.django_db
def test_list_artists():
    """unittest for albums_dml.list_artists
    """
    artist = testee.my.Act.objects.create(first_name='a', last_name='band')
    artist2 = testee.my.Act.objects.create(last_name='players')
    artist3 = testee.my.Act.objects.create(first_name='Andy', last_name='Bendy')
    assert list(testee.list_artists()) == [artist3, artist, artist2]
    assert list(testee.list_artists(sel="and")) == [artist3, artist]


def test_get_albums_lists(monkeypatch, capsys):
    """unittest for albums_dml.get_albums_lists
    """
    def mock_list_albums(arg):
        """stub
        """
        print(f'called dml.list_albums with arg `{arg}`')
        return [{'id': 2, 'name': 'a'}, {'id': 1, 'name': 'b'}]
    monkeypatch.setattr(testee, 'list_albums', mock_list_albums)
    assert testee.get_albums_lists('a') == ([2, 1], ['a', 'b'])
    assert capsys.readouterr().out == 'called dml.list_albums with arg `a`\n'


@pytest.mark.django_db
def test_list_albums():
    """unittest for albums_dml.list_albums
    """
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album1 = testee.my.Album.objects.create(artist=artist, name='Number one')
    album2 = testee.my.Album.objects.create(artist=artist, name='Number two')
    assert testee.list_albums(artist.id) == [{'id': album1.id, 'name': 'Number one'},
                                             {'id': album2.id, 'name': 'Number two'}]


@pytest.mark.django_db
def test_list_albums_by_artist(monkeypatch, capsys):
    """unittest for albums_dml.list_albums_by_artist
    """
    def mock_exclude(self, **args):
        """stub
        """
        print('called exclude() on queryset with args', args)
        return self
    def mock_filter(self, **args):
        """stub
        """
        print('called filter() on queryset with args', args)
        return self
    def mock_all(self):
        """stub
        """
        print('called all() on queryset')
        return self
    def mock_order_by(self, *args):
        """stub
        """
        print('called order_by() on queryset with args', args)
        return self
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'exclude', mock_exclude)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'filter', mock_filter)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'all', mock_all)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'order_by', mock_order_by)
    data = testee.list_albums_by_artist('studio', 1, 'Titel')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
                                       "called filter() on queryset with args {'artist': 1}\n"
                                       "called order_by() on queryset with args ('name',)\n")
    data = testee.list_albums_by_artist('live', 1, 'Locatie')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called filter() on queryset with args {'label': ''}\n"
                                       "called filter() on queryset with args {'artist': 1}\n"
                                       "called order_by() on queryset with args ('name',)\n")
    data = testee.list_albums_by_artist('', 1, 'Uitvoerende')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called filter() on queryset with args {'artist': 1}\n"
                                       "called order_by() on queryset with args ('artist',)\n")
    data = testee.list_albums_by_artist('', 1, 'Niet sorteren')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == "called filter() on queryset with args {'artist': 1}\n"
    data = testee.list_albums_by_artist('', 1, 'Jaar')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called filter() on queryset with args {'artist': 1}\n"
                                       "called order_by() on queryset with args ('release_year',)\n")


@pytest.mark.django_db
def test_list_albums_by_search(monkeypatch, capsys):
    """unittest for albums_dml.list_albums_by_search
    """
    def mock_exclude(self, **args):
        """stub
        """
        print('called exclude() on queryset with args', args)
        return self
    def mock_filter(self, **args):
        """stub
        """
        print('called filter() on queryset with args', args)
        return self
    def mock_all(self):
        """stub
        """
        print('called all() on queryset')
        return self
    def mock_order_by(self, *args):
        """stub
        """
        print('called order_by() on queryset with args', args)
        return self
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'exclude', mock_exclude)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'filter', mock_filter)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'all', mock_all)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'order_by', mock_order_by)
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='Number one', produced_by='xxx',
                                    credits='yyy', bezetting='zzz')
    data = testee.list_albums_by_search('studio', 'name', 'x', 'Titel')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
                                       "called filter() on queryset with args"
                                       " {'name__icontains': 'x'}\n"
                                       "called order_by() on queryset with args ('name',)\n")
    data = testee.list_albums_by_search('live', 'name', 'x', 'Locatie')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called filter() on queryset with args {'label': ''}\n"
                                       "called filter() on queryset with args"
                                       " {'name__icontains': 'x'}\n"
                                       "called order_by() on queryset with args ('name',)\n")
    data = testee.list_albums_by_search('studio', 'produced_by', 'x', 'Uitvoerende')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
                                       "called filter() on queryset with args"
                                       " {'produced_by__icontains': 'x'}\n"
                                       "called order_by() on queryset with args ('artist',)\n")
    data = testee.list_albums_by_search('studio', 'credits', 'x', 'Jaar')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
                                       "called filter() on queryset with args"
                                       " {'credits__icontains': 'x'}\n"
                                       "called order_by() on queryset with args ('release_year',)\n")
    data = testee.list_albums_by_search('studio', 'bezetting', 'x', 'Niet sorteren')
    assert isinstance(data, testee.django.db.models.query.QuerySet)
    assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
                                       "called filter() on queryset with args"
                                       " {'bezetting__icontains': 'x'}\n")


@pytest.mark.django_db
def test_list_album_details():
    """unittest for albums_dml.list_album_details
    """
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='Number one')
    assert testee.list_album_details(album.id) == album


@pytest.mark.django_db
def test_get_tracks_lists(monkeypatch, capsys):
    """unittest for albums_dml.get_tracks_lists
    """
    def mock_list_tracks(*args):
        """stub
        """
        print('called dml.list_tracks with args', args)
        # return [{'volgnr': 2, 'name': 'a'}, {'volgnr': 1, 'name': 'b'}]
        # album = testee.my.Album.objects.create(artist=artist, name='Number one')
        track1 = testee.my.Song.objects.create(volgnr=2, name='track 1')
        track2 = testee.my.Song.objects.create(volgnr=1, name='track 2')
        return (x for x in [track1, track2])
    monkeypatch.setattr(testee, 'list_tracks', mock_list_tracks)
    assert testee.get_tracks_lists('x', 'y') == ([2, 1], ['track 1', 'track 2'])
    assert capsys.readouterr().out == "called dml.list_tracks with args ('y',)\n"


@pytest.mark.django_db
def test_list_tracks():
    """unittest for albums_dml.list_tracks
    """
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='Number one')
    track1 = testee.my.Song.objects.create(volgnr=2, name='track 1')
    track2 = testee.my.Song.objects.create(volgnr=1, name='track 2')
    album.tracks.add(track1, track2)
    assert list(testee.list_tracks(album.id)) == [track2, track1]


@pytest.mark.django_db
def test_list_recordings():
    """unittest for albums_dml.list_recordings
    """
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='Number one')
    opname1 = testee.my.Opname.objects.create(type='x', oms='opname 1')
    opname2 = testee.my.Opname.objects.create(type='y', oms='opname 2')
    album.opnames.add(opname1, opname2)
    assert list(testee.list_recordings(album.id)) == [opname1, opname2]


@pytest.mark.django_db
def test_update_album_details():
    """unittest for albums_dml.update_album_details
    """
    artist1 = testee.my.Act.objects.create(last_name='bladibla')
    artist2 = testee.my.Act.objects.create(last_name='gargl')
    album1 = testee.my.Album.objects.create(artist=artist1, name='One', label='q', release_year=1)
    album2 = testee.my.Album.objects.create(artist=artist1, name='Two', label='q', release_year=1)
    album3 = testee.my.Album.objects.create(artist=artist1, name='Next', label='q', release_year=1)
    albumcount = len([album1, album2, album3])
    albumdata = {'artist': artist1, 'titel': 'y', 'details': [('Label/jaar:', 'r')]}
    data, ok = testee.update_album_details(album1.id, albumdata)
    assert ok
    assert testee.my.Album.objects.count() == albumcount  # 3
    assert (data.artist, data.name, data.label, data.release_year) == (artist1, 'y', 'r', 1)
    albumdata = {'artist': artist1, 'titel': 'Two', 'details': [('Label/jaar:', '2')]}
    data, ok = testee.update_album_details(album2.id, albumdata)
    assert ok
    assert testee.my.Album.objects.count() == albumcount  # 3
    assert (data.artist, data.name, data.label, data.release_year) == (artist1, 'Two', 'q', 2)
    albumdata = {'artist': artist2, 'titel': 'y', 'details': [('Label/jaar:', '')]}
    data, ok = testee.update_album_details(album3.id, albumdata)
    assert ok
    assert testee.my.Album.objects.count() == albumcount  # 3
    # assert (data.artist, data.name, data.label, data.release_year) == (artist2, 'y', '', 0)
    assert (data.artist, data.name, data.label, data.release_year) == (artist2, 'y', '', 1)

    albumdata = {'artist': artist2, 'titel': 'y', 'details': [('Label/jaar:', "z, 9"),
                                                              ('Produced by:', 'a'),
                                                              ('Credits:', 'b'),
                                                              ('Bezetting:', 'c'),
                                                              ('Tevens met:', 'd')]}
    data, ok = testee.update_album_details(0, albumdata)
    assert ok
    albumcount += 1
    assert testee.my.Album.objects.count() == albumcount  # 4
    assert isinstance(data, testee.my.Album)
    assert (data.artist, data.name, data.label, data.release_year) == (artist2, 'y', 'z', 9)
    assert (data.produced_by, data.credits, data.bezetting, data.additional) == ('a', 'b', 'c', 'd')


@pytest.mark.django_db
def test_update_album_tracks():
    """unittest for albums_dml.update_album_tracks
    """
    myartist = testee.my.Act.objects.create(last_name='bladibla')
    myalbum = testee.my.Album.objects.create(artist=myartist, name='x', label='q', release_year=1)
    mytrack1 = testee.my.Song.objects.create(volgnr=5)
    mytrack2 = testee.my.Song.objects.create(volgnr=1)
    mytrack3 = testee.my.Song.objects.create(volgnr=2)
    myalbum.tracks.add(mytrack1, mytrack2, mytrack3)
    assert testee.update_album_tracks(myalbum.id, [(2, ('a', 'b', 'c')), (3, ('c', 'd', 'e'))])
    data = list(myalbum.tracks.all())
    assert len(data) == len([1, 2, 3, 5])  # 4
    assert isinstance(data[3], testee.my.Song)
    assert (data[2].name, data[2].written_by, data[2].credits) == ('a', 'b', 'c')
    assert (data[3].volgnr, data[3].name) == (3, 'c')
    assert (data[3].written_by, data[3].credits) == ('d', 'e')


@pytest.mark.django_db
def test_update_album_recordings():
    """unittest for albums_dml.update_album_recordings
    """
    myartist = testee.my.Act.objects.create(last_name='bladibla')
    myalbum = testee.my.Album.objects.create(artist=myartist, name='x', label='q', release_year=1)
    myopname1 = testee.my.Opname.objects.create(type='x', oms='q')
    myopname2 = testee.my.Opname.objects.create(type='y', oms='r')
    myopname3 = testee.my.Opname.objects.create(type='z', oms='s')
    myalbum.opnames.add(myopname1, myopname2, myopname3)
    assert testee.update_album_recordings(myalbum.id, [(2, ('a', 'b')), (3, ('c', 'd'))])
    data = list(myalbum.opnames.all())
    assert len(data) == len(['q', 'r', 'b', 'c'])  # 4
    assert isinstance(data[3], testee.my.Opname)
    assert (data[2].type, data[2].oms) == ('a', 'b')
    assert (data[3].type, data[3].oms) == ('c', 'd')


@pytest.mark.django_db
def test_update_artists():
    """unittest for albums_dml.update_artists
    """
    artist = testee.my.Act.objects.create(last_name='bladibla')
    data = testee.update_artists([(artist.id, 'x', 'y')])[0]
    assert (data.first_name, data.last_name) == ('x', 'y')
    artistcount = len([artist])
    assert testee.my.Act.objects.count() == artistcount  # 1
    data = testee.update_artists([(0, 'a', 'b')])[0]
    artistcount += 1
    assert (data.first_name, data.last_name) == ('a', 'b')
    assert testee.my.Act.objects.count() == artistcount  # 2


@pytest.mark.django_db
def test_update_albums_by_artist_no_changes(monkeypatch):
    """unittest for albums_dml.update_albums_by_artist: no changes
    """
    monkeypatch.setattr(testee, 'c_type', 'z')
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='One', label='q', release_year=1)
    opname = testee.my.Opname.objects.create(type='z', oms='s')
    opname2 = testee.my.Opname.objects.create(type='x', oms='s')
    album.opnames.add(opname, opname2)
    changes = [(album.id, 'One', 1, False, [(1, 'track')])]
    result = testee.update_albums_by_artist(artist.id, changes)
    assert result == [album]
    assert not list(result[0].tracks.all())


@pytest.mark.django_db
def test_update_albums_by_artist_add_reg(monkeypatch):
    """unittest for albums_dml.update_albums_by_artist: add opname
    """
    monkeypatch.setattr(testee, 'c_type', 'z')
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='One', label='q', release_year=1)
    # opname = testee.my.Opname.objects.create(type='z', oms='s')
    opname = testee.my.Opname.objects.create(type='x', oms='s')
    album.opnames.add(opname)
    opnamecount = len([opname])
    changes = [(album.id, 'One', 1, False, [])]
    # breakpoint()
    result = testee.update_albums_by_artist(artist.id, changes)
    opnamecount += 1
    assert result == [album]
    assert not list(result[0].tracks.all())
    data = list(result[0].opnames.all())
    assert len(data) == opnamecount  # 2
    assert data[1].type == testee.c_type


@pytest.mark.django_db
def test_update_albums_by_artist_changes(monkeypatch):
    """unittest for albums_dml.update_albums_by_artist: changes
    """
    monkeypatch.setattr(testee, 'c_type', 'z')
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='One', label='q', release_year=1)
    opname = testee.my.Opname.objects.create(type='z', oms='s')
    album.opnames.add(opname)
    changes = [(album.id, 'Not One', 2, False, [])]
    result = testee.update_albums_by_artist(artist.id, changes)
    assert result == [album]
    assert (result[0].name, result[0].label, result[0].release_year) == ('Not One', 'q', 2)
    assert not list(result[0].tracks.all())
    assert list(result[0].opnames.all()) == [opname]


@pytest.mark.django_db
def test_update_albums_by_artist_new_album(monkeypatch):
    """unittest for albums_dml.update_albums_by_artist: new album
    """
    monkeypatch.setattr(testee, 'c_type', 'z')
    artist = testee.my.Act.objects.create(last_name='bladibla')
    changes = [(0, 'One', 1, False, [(1, 'track')])]
    result = testee.update_albums_by_artist(artist.id, changes)
    assert len(result) == 1
    assert isinstance(result[0], testee.my.Album)
    assert (result[0].name, result[0].label, result[0].release_year) == ('One', '(unknown)', 1)
    data = list(result[0].tracks.all())
    assert len(data) == 1
    assert (data[0].volgnr, data[0].name) == (1, 'track')
    data = list(result[0].opnames.all())
    assert len(data) == 1
    assert data[0].type == testee.c_type


@pytest.mark.django_db
def test_update_album_tracknames():
    """unittest for albums_dml.update_album_tracknames
    """
    # but this routine shuffles track *numbers*, not names
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='this')
    track1 = testee.my.Song.objects.create(volgnr=2, name='One')
    track2 = testee.my.Song.objects.create(volgnr=1, name='Two')
    album.tracks.add(track1, track2)
    trackcount = len([track1, track2])
    testee.update_album_tracknames(album.id, ((0, 'One'), (1, 'Two'), (2, 'Three')))
    trackcount += 1
    data = list(album.tracks.all())
    assert len(data) == trackcount  # 3
    assert (data[0].volgnr, data[0].name) == (0, 'One')
    assert (data[1].volgnr, data[1].name) == (1, 'Two')
    assert (data[2].volgnr, data[2].name) == (2, 'Three')


@pytest.mark.django_db
def test_unlink_album(monkeypatch):
    """unittest for albums_dml.unlink_album
    """
    monkeypatch.setattr(testee, 'c_type', 'z')
    artist = testee.my.Act.objects.create(last_name='bladibla')
    album = testee.my.Album.objects.create(artist=artist, name='One', label='q', release_year=1)
    opname = testee.my.Opname.objects.create(type='z', oms='s')
    opname2 = testee.my.Opname.objects.create(type='x', oms='s')
    album.opnames.add(opname, opname2)
    opnamecount = len([opname, opname2])
    assert album.opnames.count() == opnamecount  # 2
    testee.unlink_album(album.id)
    opnamecount -= 1
    assert album.opnames.count() == opnamecount  # 1
