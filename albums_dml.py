"""Data manipulation routines for albums_gui
"""
import sys
import os
import django
sys.path.append('/home/albert/projects/albums')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albums.settings")
django.setup()
from django.db.models import Q
import albums.muziek.models as my


def list_artists(sel=""):
    """produce list of artists
    """
    if not sel:
        artist_list = my.Act.objects.order_by('last_name')
    else:
        artist_list = my.Act.objects.filter(
            Q(first_name__icontains=sel) | Q(last_name__icontains=sel)).order_by(
                'last_name')
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
    else:
        sel = my.Album.objects.all()
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
    """store data from screen in database - return updated version
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
                album.label = test[0]
                if test[1]:
                    album.release_year = int(test[1])
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
        if ix in old_tracks:
            if item != old_tracks[ix]:
                trk = old_tracks[ix]
                changed = True
        else:
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
        if ix < len(old_recs):
            old_item = (old_recs[ix].type, old_recs[ix].oms)
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
    """store data from screen in database
    """
    results = []
    for id, first_name, last_name in changes:
        if id:
            item = my.Act.objects.get(pk=id)
        else:
            item = my.Act.objects.create()
        item.first_name = first_name
        item.last_name = last_name
        item.save()
        results.append(item)
    return results


def update_albums_by_artist(artist_id, changes):
    """store data from screen in database

    also add "recorded in Clementine"
    when provided, also add tracks
    """
    c_type = 'Clementine music player'
    artist = my.Act.objects.get(pk=artist_id)
    results = []
    for id, name, year, is_live, tracks in changes:
        if id:
            item = my.Album.objects.get(pk=id)
            changed = True
            if name == item.name and year == item.release_year:
                for opn in item.opnames.all():
                    if opn.type == c_type:
                        changed = False
                        break
        else:
            item = my.Album()
            item.artist = artist
            if not is_live:
                item.label = "(unknown)"
            changed = True
        if changed:
            item.name = name
            if year:
                item.release_year = int(year)
            item.save()
            found = False
            for opn in item.opnames.all():
                if opn.type == c_type:
                    found = True
                    break
            if not found:
                item.opnames.add(my.Opname.objects.create(type=c_type))
            for num, title in tracks:
                item.tracks.add(my.Song.objects.create(volgnr=num, name=title))
            item.save()
        results.append(item)
    return results


def update_album_tracknames(album_id, tracks):
    """store data from screen in database
    """
    item = my.Album.objects.get(pk=album_id)
    oldtracks = {x.name.upper(): x for x in item.tracks.all()}
    for num, title in tracks:
        title_u = title.upper()
        if title_u in oldtracks:
            if num != oldtracks[title_u].volgnr:
                oldtracks[title_u].volgnr = num
                oldtracks[title_u].save()
        else:
            item.tracks.add(my.Song.objects.create(volgnr=num, name=title))
    item.save()


def unlink_album(album_id):
    """remove Clementine indicator
    """
    c_type = 'Clementine music player'
    item = my.Album.objects.get(pk=album_id)
    for opn in item.opnames.all():
        if opn.type == c_type:
            item.opnames.remove(opn)
            item.save()
            break


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
        for x in test:
            print(x, file=_out)
