"""dml for Clementine database
"""
## import os
import pprint
import sqlite3
from .banshee_settings import databases
DB = databases['clementine']


def retrieve(query, parms):
    "get data from database"
    result = []
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for row in cur.execute(query, parms):
            result.append({name: row[name] for name in row.keys()})
    return result


def get_artists_lists():
    "produce list of artists"
    data = [x["artist"] for x in retrieve("select distinct artist from songs "
                                          "where unavailable = '0' order by artist;", ())]
    return data, data


def get_albums_lists(artist_name):
    "produce list of albums for artist"
    data = [x["album"] for x in retrieve("select distinct album, year from songs where artist = ? "
                                         "and unavailable = '0';", (artist_name,))]
    return data, data


def get_album_cover(artist_name='', album_name='', all_tracks=False):
    """produce list of album covers
    all_tracks biedt de mogelijkheid om de per track vastgelegde covers te bekijken,
    voor nu gebruiken we alleen die van het eerste track
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
    data = retrieve(query, parms)
    return data[0]['art_manual'] or data[0]['art_automatic']


def list_tracks_for_artist(artist_name):
    "produce list of tracks for artist"
    data = retrieve("select rowid, album, disc, track, title, filename from songs where "
                    "artist = ? order by album, disc, track;", (artist_name,))
    return [x["album"] for x in data], [x["title"] for x in data]


def get_tracks_lists(artist_name, album_name):
    "produce list of tracks for album"
    data = [x["title"] for x in retrieve("select rowid, track, title from songs"
                                         " where artist = ? and album = ? and unavailable = '0'"
                                         " order by disc, track;", (artist_name, album_name))]
    return data, data
