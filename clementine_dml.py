"""dml for Clementine database
"""
## import os
import pprint
import sqlite3
from contextlib import closing
from banshee_settings import databases
DB = databases['clementine']


def retrieve(db, query, parms):
    "get data from database"
    result = []
    with closing(sqlite3.connect(db)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for row in cur.execute(query, parms):
            result.append({name: row[name] for name in row.keys()})
    return result


def list_artists(db):
    "produce list of artists"
    return retrieve(db, "select distinct artist from songs "
                    "where unavailable = '0' order by artist;", ())


def list_albums(db, artist_name):
    "produce list of albums for artist"
    return retrieve(db, "select distinct album, year from songs where artist = ? "
                    "and unavailable = '0';", (artist_name,))


def list_album_covers(db, artist_name='', album_name='', all_tracks=False):
    """produce list of album covers
    """
    query = 'select distinct artist, album, track, art_automatic, art_manual from songs'
    cond, parms = [], []
    if artist_name:
        cond.append('artist = ?')
        parms.append(artist_name)
    if album_name:
        cond.append('album = ?')
        parms.append(album_name)
    if all_tracks:
        query = query.replace('distinct ', '')
    else:
        query = query.replace('track, ', '')
    if cond:
        query += ' where ' + ' and '.join(cond)
    if not album_name and not artist_name:
        query += ' order by artist, album'
    return retrieve(db, query, parms)


def list_tracks_for_artist(db, artist_name):
    "produce list of tracks for album"
    return retrieve(
        db, "select rowid, album, disc, track, title, filename from songs where "
            "artist = ? order by album, disc, track;", (artist_name,))


def list_tracks_for_album(db, artist_name, album_name):
    "produce list of tracks for album"
    return retrieve(
        db, "select rowid, track, title from songs where artist = ? and album = ? "
        "and unavailable = '0' order by disc, track;", (artist_name, album_name))


def main():
    """simple test: print data
    """
    db = DB
    with open("/tmp/test_clementine_output", "w") as _out:
        artist_list = list_artists(db)
        pprint.pprint(artist_list, stream=_out)

        artist = artist_list[92]['artist']  # 'Blind Faith'
        album_list = list_albums(db, artist)
        pprint.pprint(album_list, stream=_out)
        pprint.pprint(list_album_covers(db, artist, ''), stream=_out)

        album = album_list[9]['album']
        pprint.pprint(list_album_covers(db, '', album, True), stream=_out)
        pprint.pprint(list_album_covers(db, artist, album), stream=_out)

        pprint.pprint(list_tracks_for_artist(db, artist))
        pprint.pprint(list_tracks_for_album(db, artist, album), stream=_out)

if __name__ == "__main__":
    main()
