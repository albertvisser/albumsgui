"""dml for Clementine database
"""
import pprint
import sqlite3
from contextlib import closing


def execute_query(db, query):
    "get data from database"
    result = []
    with closing(sqlite3.connect(db)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print(query)
        for row in cur.execute(query):
            result.append({name: row[name] for name in row.keys()})
    return result


def list_artists(db):
    "produce list of artists"
    return execute_query(
        db, "select distinct artist from songs where unavailable = '0' order by artist;")


def list_albums(db, artist_id):
    "produce list of albums for artist"
    return execute_query(
        db, "select distinct album from songs where artist = '{}' "
        "and unavailable = '0';".format(artist_id))


def list_tracks(db, artist_id, album_id):
    "produce list of tracks for album"
    return execute_query(
        db, "select track, title from songs where artist = '{}' and album = '{}' "
        "and unavailable = '0' order by disc, track;".format(artist_id, album_id))


def main():
    """simple test: print data
    """
    db = '/home/albert/.config/Clementine.orig/clementine.db'
    with open("/tmp/test_clementine_output", "w") as _out:
        artist_list = list_artists(db)
        pprint.pprint(artist_list, stream=_out)
        artist = artist_list[18]['artist']
        album_list = list_albums(db, artist)
        pprint.pprint(album_list, stream=_out)
        album = album_list[0]['album']
        pprint.pprint(list_tracks(db, artist, album), stream=_out)

if __name__ == "__main__":
    main()
