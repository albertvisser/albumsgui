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
from albums.muziek.helpers import s_keuzes, s_sorts, l_keuzes, l_sorts


def list_artists(sel=""):
    if not sel:
    else:
    return artist_list


def list_albums(artist_id):
    return [{'id': x.id, 'name': x.name} for x in my.Album.objects.filter(artist=artist_id)]


def list_albums_by_artist(albumtype, artist_id, order_by):
    if albumtype == 'studio':
    elif albumtype == 'live':
    else:
    if order_by == 'Uitvoerende':
    elif order_by == 'Titel':
    elif order_by == 'Jaar':
    elif order_by == 'Niet sorteren':
    elif order_by == 'Locatie':
    return sel


def list_albums_by_search(albumtype, search_type, search_for, order_by):
    if albumtype == 'studio':
    elif albumtype == 'live':
    if search_type == 'name':
    elif search_type == 'produced_by':
    elif search_type == 'credits':
    elif search_type == 'bezetting':
    if order_by == 'Uitvoerende':
    elif order_by == 'Titel':
    elif order_by == 'Jaar':
    elif order_by == 'Niet sorteren':
    elif order_by == 'Locatie':
    return sel


def list_album_details(album_id):
    return my.Album.objects.get(pk=album_id)


def list_tracks(album_id):
    return my.Album.objects.get(pk=album_id).tracks.all().order_by('volgnr')


def list_recordings(album_id):
    return my.Album.objects.get(pk=album_id).opnames.all()


def update_album_details(album_id, albumdata):
    if album_id:
        if albumdata['artist'] != album.artist:
        if albumdata['titel'] != album.name:
    else:
    for name, value in albumdata['details']:
        if name == 'Label/jaar:':
            if len(test) == 2:
                if test[1]:
            else:
                try:
                except ValueError:
        elif name == 'Produced by:':
        elif name == 'Credits:':
        elif name == 'Bezetting:':
        elif name == 'Tevens met:':
    return updated, ok


def update_album_tracks(album_id, tracks):
    for ix, item in tracks:
        if ix in old_tracks:
            if item != old_tracks[ix]:
        else:
        if changed or new_track:
    return ok


def update_album_recordings(album_id, recordings):
    for ix, item in recordings:
        if ix < len(old_recs):
            if item != old_item:
        else:
        if changed or new_rec:
    return ok


def update_artists(changes):
    for id, first_name, last_name in changes:
        if id:
        else:
    return results


def update_albums_by_artist(artist_id, changes):
    for id, name, year, is_live, tracks in changes:
        if id:
            if name == item.name and year == item.release_year:
                for opn in item.opnames.all():
                    if opn.type == c_type:
        else:
            if not is_live:
        if changed:
            if year:
            for opn in item.opnames.all():
                if opn.type == c_type:
            if not found:
            for num, title in tracks:
    return results


def update_album_tracknames(album_id, tracks):
    for num, title in tracks:
        if title_u in oldtracks:
            if num != oldtracks[title_u].volgnr:
        else:


def unlink_album(album_id):
    for opn in item.opnames.all():
        if opn.type == c_type:
