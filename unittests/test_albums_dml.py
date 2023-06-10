"""Data manipulation routines for albums_gui
"""
import sys
import os
import django
import pytest
sys.path.append('/home/albert/projects/albums')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albums.settings")
django.setup()
# from django.db.models import Q
import albums.muziek.models as my
# from albums.muziek.helpers import s_keuzes, s_sorts, l_keuzes, l_sorts
import apps.albums_dml as testee


def test_get_artists_lists(monkeypatch, capsys):
    def mock_list_artists():
        print('called dml.list_artists')
        return [{'id': 2, 'first_name': 'a', 'last_name': 'band'},
                {'id': 1, 'first_name': '', 'last_name': 'players'}]
    monkeypatch.setattr(testee, 'list_artists', mock_list_artists)
    assert testee.get_artists_lists() == ([2, 1], ['a band', 'players'])
    assert capsys.readouterr().out == 'called dml.list_artists\n'


@pytest.mark.django_db
def test_list_artists():
    artist = my.Act.objects.create(first_name='a', last_name='band')
    artist2 = my.Act.objects.create(last_name='players')
    artist3 = my.Act.objects.create(first_name='Andy', last_name='Bendy')
    assert list(testee.list_artists()) == [artist3, artist, artist2]
    assert list(testee.list_artists(sel="and")) == [artist3, artist]


def test_get_albums_lists(monkeypatch, capsys):
    def mock_list_albums(arg):
        print(f'called dml.list_albums with arg `{arg}`')
        return [{'id': 2, 'name': 'a'}, {'id': 1, 'name': 'b'}]
    monkeypatch.setattr(testee, 'list_albums', mock_list_albums)
    assert testee.get_albums_lists('a') == ([2, 1], ['a', 'b'])
    assert capsys.readouterr().out == 'called dml.list_albums with arg `a`\n'


@pytest.mark.django_db
def test_list_albums():
    artist = my.Act.objects.create(last_name='bladibla')
    album1 = my.Album.objects.create(artist=artist, name='Number one')
    album2 = my.Album.objects.create(artist=artist, name='Number two')
    assert testee.list_albums(artist.id) == [{'id': album1.id, 'name': 'Number one'},
                                             {'id': album2.id, 'name': 'Number two'}]


@pytest.mark.django_db
def test_list_albums_by_artist(monkeypatch, capsys):
    def mock_exclude(self, **args):
        print('called exclude() on queryset with args', args)
        return self
    def mock_filter(self, **args):
        print('called filter() on queryset with args', args)
        return self
    def mock_all(self):
        print('called all() on queryset')
        return self
    def mock_order_by(self, *args):
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
    def mock_exclude(self, **args):
        print('called exclude() on queryset with args', args)
        return self
    def mock_filter(self, **args):
        print('called filter() on queryset with args', args)
        return self
    def mock_all(self):
        print('called all() on queryset')
        return self
    def mock_order_by(self, *args):
        print('called order_by() on queryset with args', args)
        return self
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'exclude', mock_exclude)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'filter', mock_filter)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'all', mock_all)
    monkeypatch.setattr(testee.django.db.models.query.QuerySet, 'order_by', mock_order_by)
    artist = my.Act.objects.create(last_name='bladibla')
    album = my.Album.objects.create(artist=artist, name='Number one', produced_by='xxx',
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
    # data = testee.list_albums_by_search('', 'produced_by', 'x', 'Uitvoerende')
    # assert isinstance(data, testee.django.db.models.query.QuerySet)
    # assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
    #                                    "called filter() on queryset with args"
    #                                    " {'name__icontains': 'x'}\n"
    #                                    "called order_by() on queryset with args ('name',)\n")
    # data = testee.list_albums_by_search('', 'credits', 'x', 'Jaar')
    # assert isinstance(data, testee.django.db.models.query.QuerySet)
    # assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
    #                                    "called filter() on queryset with args"
    #                                    " {'name__icontains': 'x'}\n"
    #                                    "called order_by() on queryset with args ('name',)\n")
    # data = testee.list_albums_by_search('', 'bezetting', 'x', 'Niet sorteren')
    # assert isinstance(data, testee.django.db.models.query.QuerySet)
    # assert capsys.readouterr().out == ("called exclude() on queryset with args {'label': ''}\n"
    #                                    "called filter() on queryset with args"
    #                                    " {'name__icontains': 'x'}\n"
    #                                    "called order_by() on queryset with args ('name',)\n")


@pytest.mark.django_db
def test_list_album_details():
    artist = my.Act.objects.create(last_name='bladibla')
    album = my.Album.objects.create(artist=artist, name='Number one')
    assert testee.list_album_details(album.id) == album


def test_get_tracks_lists(monkeypatch, capsys):
    def mock_list_tracks(*args):
        print(f'called dml.list_tracks with args', args)
        return [{'volgnr': 2, 'name': 'a'}, {'volgnr': 1, 'name': 'b'}]
    monkeypatch.setattr(testee, 'list_tracks', mock_list_tracks)
    assert testee.get_tracks_lists('x', 'y') == ([2, 1], ['a', 'b'])
    assert capsys.readouterr().out == "called dml.list_tracks with args ('y',)\n"


@pytest.mark.django_db
def test_list_tracks():
    artist = my.Act.objects.create(last_name='bladibla')
    album = my.Album.objects.create(artist=artist, name='Number one')
    track1 = my.Song.objects.create(volgnr=2, name='track 1')
    track2 = my.Song.objects.create(volgnr=1, name='track 2')
    album.tracks.add(track1, track2)
    assert list(testee.list_tracks(album.id)) == [track2, track1]


@pytest.mark.django_db
def test_list_recordings():
    artist = my.Act.objects.create(last_name='bladibla')
    album = my.Album.objects.create(artist=artist, name='Number one')
    opname1 = my.Opname.objects.create(type='x', oms='opname 1')
    opname2 = my.Opname.objects.create(type='y', oms='opname 2')
    album.opnames.add(opname1, opname2)
    assert list(testee.list_recordings(album.id)) == [opname1, opname2]

def _test_update_album_details():
    assert testee.update_album_details(album_id, albumdata)
    # if album_id:
    #     if albumdata['artist'] != album.artist:
    #     if albumdata['titel'] != album.name:
    # else:
    # for name, value in albumdata['details']:
    #     if name == 'Label/jaar:':
    #         if len(test) == 2:
    #             if test[1]:
    #         else:
    #             try:
    #             except ValueError:
    #     elif name == 'Produced by:':
    #     elif name == 'Credits:':
    #     elif name == 'Bezetting:':
    #     elif name == 'Tevens met:':
    return updated, ok


def _test_update_album_tracks():
    assert testee.update_album_tracks(album_id, tracks)
    # for ix, item in tracks:
    #     if ix in old_tracks:
    #         if item != old_tracks[ix]:
    #     else:
    #     if changed or new_track:
    return ok


def _test_update_album_recordings():
    assert testee.update_album_recordings(album_id, recordings)
    # for ix, item in recordings:
    #     if ix < len(old_recs):
    #         if item != old_item:
    #     else:
    #     if changed or new_rec:
    return ok


def _test_update_artists():
    assert testee.update_artists(changes)
    # for id, first_name, last_name in changes:
    # if id:
    # else:
    return results


def _test_update_albums_by_artist():
    assert testee.update_albums_by_artist(artist_id, changes)
    # for id, name, year, is_live, tracks in changes:
    #     if id:
    #         if name == item.name and year == item.release_year:
    #             for opn in item.opnames.all():
    #                 if opn.type == c_type:
    #     else:
    #         if not is_live:
    #     if changed:
    #         if year:
    #         for opn in item.opnames.all():
    #             if opn.type == c_type:
    #         if not found:
    #         for num, title in tracks:
    return results


def _test_update_album_tracknames():
    testee.update_album_tracknames(album_id, tracks)
    # for num, title in tracks:
    #     if title_u in oldtracks:
    #         if num != oldtracks[title_u].volgnr:
    #     else:


def _test_unlink_album():
    testee.unlink_album(album_id)
    # for opn in item.opnames.all():
    #     if opn.type == c_type:
