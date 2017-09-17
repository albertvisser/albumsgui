"""dml for Banshee database
"""
import sqlite3
from contextlib import closing
from banshee_settings import databases
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


def list_tracks(db, album_id):
    """produce list of tracks for album
    """
    return execute_query(
        db, "select TrackNumber, Title from coretracks where AlbumID = {} "
        "order by Disc, TrackNumber".format(album_id))


def main():
    """simple test: print data
    """
    db = DB
    with open("test_banshee_output", "w") as _out:
        print(list_artists(db), file=_out)
        print(list_albums(db, 19), file=_out)
        print(list_tracks(db, 182), file=_out)

if __name__ == "__main__":
    main()
