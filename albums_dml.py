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
    return [{'id': x.id, 'name': x.get_name()} for x in artist_list]
    ## return [{'id': x.id, 'first_name': x.first_name, 'last_name': x.last_name}
            ## for x in artist_list]


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
    return sel  # [{'id': x.id, 'name': x.name} for x in sel]


def list_albums_by_search(albumtype, search_type, search_for, order_by):
    """produce list of albums by tesxt search and sorted
    """
    if albumtype == 'studio':
        sel = my.Album.objects.exclude(label="")
        if search_type == 2:
            sel = sel.filter(name__icontains=search_for)
        elif search_type == 3:
            sel = sel.filter(produced_by__icontains=search_for)
        elif search_type == 4:
            sel = sel.filter(credits__icontains=search_for)
        elif search_type == 5:
            sel = sel.filter(bezetting__icontains=search_for)
    elif albumtype == 'live':
        sel = my.Album.objects.filter(label="")
        if search_type == 2:
            sel = sel.filter(name__icontains=search_for)
        elif search_type == 3:
            sel = sel.filter(name__icontains=search_for)
        elif search_type == 4:
            sel.filter(bezetting__icontains=search_for)
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
    return sel, [x.artist.get_name() for x in sel]


def list_album_details(album_id):
    """get album details
    """
    print(album_id, type(album_id))
    album = my.Album.objects.get(pk=album_id)
    print(album.artist)
    artist = album.artist.get_name()
    return album, artist


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
