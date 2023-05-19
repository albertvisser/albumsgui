"""dml for Banshee database
"""
import sqlite3
import pprint
from contextlib import closing
from .banshee_settings import databases
DB = databases['banshee']


def execute_query(db, query):
    """get data from database
    """
    result = []
    with closing(sqlite3.connect(db)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for row in cur.execute(query):
            result.append({name: row[name] for name in row.keys()})
    return result


def list_artists(db):
    """produce list of artists
    """
    return execute_query(
        db, "select ArtistID, Name from coreartists order by Name;")


def list_albums(db, artist_id):
    """produce list of albums for artist
    """
    return execute_query(
        db, "select AlbumID, Title from corealbums where ArtistID = {}".format(artist_id))


def list_album_covers(db, artist_id=0, album_id=0):
    """produce list of album covers
    """
    query = 'select t1.Name, t2.Title, t2.ArtworkID from coreartists as t1 ' \
            'inner join corealbums as t2 on t1.ArtistID = t2.ArtistID'
    cond = []
    if album_id:
        cond.append('t2.AlbumID = {}'.format(album_id))
    if artist_id:
        cond.append('t1.ArtistID = {}'.format(artist_id))
    if cond:
        query += ' where ' + ' and '.join(cond)
    if not album_id and not artist_id:
        query += ' order by t1.Name, t2.Title'
    return execute_query(db, query)


def list_tracks(db, album_id):
    """produce list of tracks for album
    """
    return execute_query(
        db, "select TrackNumber, Title from coretracks where AlbumID = {} "
        "order by Disc, TrackNumber".format(album_id))
