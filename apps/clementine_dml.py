"""dml for Clementine database
"""
## import os
import pprint
import sqlite3
from .banshee_settings import databases
DB = databases['clementine']


def retrieve(db, query, parms):
    "get data from database"
    result = []
    with sqlite3.connect(db) as conn:
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
