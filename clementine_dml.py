"""dml for Clementine database
"""
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


def list_tracks(db, artist_name, album_name):
    "produce list of tracks for album"
    return retrieve(
        db, "select track, title from songs where artist = ? and album = ? "
        "and unavailable = '0' order by disc, track;", (artist_name, album_name))


def main():
    """simple test: print data
    """
    ## db = '/home/albert/.config/Clementine.orig/clementine.db'
    db = DB
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
