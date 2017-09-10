"""Data manipulation routines for albums_gui
"""
import sys
import os
import django
sys.path.append('/home/albert/projects/albums')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albums.settings")
django.setup()

import albums.muziek.models as my


def list_artists():
    """produce list of artists
    """
    artist_list = my.Act.objects.order_by('last_name')
    ## return [{'id': x.id, 'name': x.get_name()} for x in artist_list]
    return artist_list


def list_albums(artist_id):
    """produce list of albums for artist
    """
    album_list = my.Album.objects.filter(artist=artist_id)
    return [{'id': x.id, 'name': x.name} for x in album_list]


def list_albums_by_artist(albumtype, artist_id, order_by):
    """produce list of albums for artist (sorted)
    """
    if albumtype == 'studio':
        sel = my.Album.objects.exclude(label="")
    elif albumtype == 'live':
        sel = my.Album.objects.filter(label="")
    sel = sel.filter(artist=artist_id)
    if order_by == 'Uitvoerende':
        sel = sel.order_by('artist')
    elif order_by == 'Titel':
        sel = sel.order_by('name')
    elif order_by == 'Jaar':
        sel = sel.order_by('release_year')
    elif order_by == 'Niet sorteren':
        pass
    elif order_by == 'Locatie':
        sel = sel.order_by('name')
    ## elif order_by == 'Datum':
        ## sel = sel.order_by('name'[:-4])
    return sel


def list_albums_by_search(albumtype, search_type, search_for, order_by):
    """produce list of albums by text search and sorted
    """
    print(albumtype, search_type, search_for, order_by)
    if albumtype == 'studio':
        sel = my.Album.objects.exclude(label="")
    elif albumtype == 'live':
        sel = my.Album.objects.filter(label="")
    if search_type == 'name':
        sel = sel.filter(name__icontains=search_for)
    elif search_type == 'produced_by':
        sel = sel.filter(produced_by__icontains=search_for)
    elif search_type == 'credits':
        sel = sel.filter(credits__icontains=search_for)
    elif search_type == 'bezetting':
        sel = sel.filter(bezetting__icontains=search_for)
    if order_by == 'Uitvoerende':
        sel = sel.order_by('artist')
    elif order_by == 'Titel':
        sel = sel.order_by('name')
    elif order_by == 'Jaar':
        sel = sel.order_by('release_year')
    elif order_by == 'Niet sorteren':
        pass
    elif order_by == 'Locatie':
        sel = sel.order_by('name')
    ## elif order_by == 'Datum':
        ## sel = sel.order_by('name'[:-4])
    return sel


def list_album_details(album_id):
    """get album details
    """
    album = my.Album.objects.get(pk=album_id)
    return album


def list_tracks(album_id):
    """produce list of tracks for album
    """
    album = my.Album.objects.get(pk=album_id)
    return album.tracks.all().order_by('volgnr')


def list_recordings(album_id):
    """produce list of recordings for album
    """
    album = my.Album.objects.get(pk=album_id)
    return album.opnames.all()


def update_album_details(album_id, albumdata):
    """store album as prepared - return updated version
    """
    """prepare data from screen for storing in database
    """
    if album_id:
        album = my.Album.objects.get(pk=album_id)
        if albumdata['artist'] != album.artist:
            album.artist = albumdata['artist']
        if albumdata['titel'] != album.name:
            album.name = albumdata['titel']
    else:
        album = my.Album.objects.create(artist=albumdata['artist'],
                                        name=albumdata['titel'])
    for name, value in albumdata['details']:
        if name == 'Label/jaar:':
            test = value.split(', ')
            if len(test) == 2:
                album.label, album.release_year = test
            else:
                try:
                    album.release_year = int(test[0])
                except ValueError:
                    album.label = test[0]
        elif name == 'Produced by:':
            album.produced_by = value
        elif name == 'Credits:':
            album.credits = value
        elif name == 'Bezetting:':
            album.bezetting = value
        elif name == 'Tevens met:':
            album.additional = value
    ok = True   # hoe detecteer ik dat er iets foutgaat? Exception?
    album.save()
    updated = album
    return updated, ok


def update_album_tracks(album_id, tracks):
    """store data from screen in database
    """
    ok = True   # hoe detecteer ik dat er iets foutgaat? Exception?
    album = my.Album.objects.get(pk=album_id)
    old_tracks = {x.volgnr: x for x in album.tracks.all()}
    new_track = changed = False
    for ix, item in tracks:
        print(ix, type(ix), item)
        if ix in old_tracks:
            if item != old_tracks[ix]:
                print('updating track')
                trk = old_tracks[ix]
                changed = True
        else:
            print('adding track')
            trk = my.Song.objects.create(volgnr=ix)
            album.tracks.add(trk)
            new_track = True
        if changed or new_track:
            trk.name = item[0]
            trk.written_by = item[1]
            trk.credits = item[2]
            trk.save()
    return ok


def update_album_recordings(album_id, recordings):
    """store data from screen in database
    """
    ok = True   # hoe detecteer ik dat er iets foutgaat? Exception?
    album = my.Album.objects.get(pk=album_id)
    old_recs = [x for x in album.opnames.all()]
    new_rec = changed = False
    for ix, item in recordings:
        old_item = (old_recs[ix].type, old_recs[ix].oms)
        if ix < len(old_recs):
            if item != old_item:
                rec = old_recs[ix]
                changed = True
        else:
            rec = my.Opname.objects.create()
            album.opnames.add(rec)
            new_rec = True
        if changed or new_rec:
            rec.type = item[0]
            rec.oms = item[1]
            rec.save()
    return ok


def update_artists(changes):
    ok = True
    for id, first_name, last_name in changes:
        if id:
            it = my.Act.objects.get(pk=id)
        else:
            it = my.Act.objects.create()
        it.first_name = first_name
        it.last_name = last_name
        it.save()
    return ok

if __name__ == '__main__':
    test = list_artists()
    ## test = list_albums(15)
    ## test = list_albums_by_artist('studio', 15, 'Jaar')
    ## test = list_albums_by_artist('studio', 15, 'Titel')
    ## test = list_albums_by_artist('studio', 15, 'Niet sorteren')
    ## test = list_albums_by_artist('live', 16, 'Locatie')
    ## test = list_albums_by_artist('live', 16, 'Datum')
    ## test = list_albums_by_artist('live', 16, 'Niet sorteren')
    ## test = list_albums_by_search('live', 2, 'Rotterdam', 'Niet sorteren')
    with open('results', 'w') as _out:
        print(len(test), file=_out)
        for item in test:
            print(item, file=_out)
