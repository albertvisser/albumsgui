"""dml for Banshee database
"""
import sqlite3
import pprint
from .banshee_settings import databases
DB = databases['banshee']


def execute_query(query, parms):
    """get data from database
    """
    result = []
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for row in cur.execute(query, parms):
            result.append({name: row[name] for name in row.keys()})
    return result


def get_artists_lists():
    """produce list of artists
    """
    data = execute_query("select ArtistID, Name from coreartists order by Name;", ())
    return ([x["ArtistID"] for x in data], [x["Name"] for x in data])


def get_albums_lists(artist_id):
    """produce list of albums for artist
    """
    data = execute_query("select AlbumID, Title from corealbums where ArtistID = ?", (artist_id,))
    return ([x["AlbumID"] for x in data], [x["Title"] for x in data])


def get_album_cover(artist_id=0, album_id=0):
    """produce list of album covers
    """
    query = 'select t1.Name, t2.Title, t2.ArtworkID from coreartists as t1 ' \
            'inner join corealbums as t2 on t1.ArtistID = t2.ArtistID'
    cond, parms = [], []
    if album_id:
        cond.append('t2.AlbumID = ?')
        parms.append(album_id)
    if artist_id:
        cond.append('t1.ArtistID = ?')
        parms.append(artist_id)
    if cond:
        query += ' where ' + ' and '.join(cond)
    if not album_id and not artist_id:
        query += ' order by t1.Name, t2.Title'
    data = execute_query(query, tuple(parms))
    return data[0]


def get_tracks_lists(artist_id=0, album_id=0):
    """produce list of tracks for album
    """
    # artist_id is voor API-compatibiliteit
    data = execute_query("select TrackNumber, Title from coretracks where AlbumID = ? "
                         "order by Disc, TrackNumber", (album_id,))
    return [x["TrackNumber"] for x in data], [x["Title"] for x in data]
