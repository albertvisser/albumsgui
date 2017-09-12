"""dml for reading Albums database from banshee_gui
"""
import sqlite3
from banshee_settings import databases
DB = databases['albums']


def execute_query(db, query):
    """get data from database
    """
    result = []
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for row in cur.execute(query):
            result.append({name: row[name] for name in row.keys()})
    return result


def list_artists(db):
    """produce list of artists
    """
    return execute_query(
        db, "select id, first_name, last_name from muziek_act order by last_name;")


def list_albums(db, artist_id):
    """produce list of albums for artist
    """
    return execute_query(
        db, "select id, name from muziek_album where artist_id = {}".format(artist_id))


def list_tracks(db, album_id):
    """produce list of tracks for album
    """
    return execute_query(
        db, "select volgnr, name, written_by, credits from muziek_song inner join "
        "muziek_album_tracks on muziek_song.id = muziek_album_tracks.song_id "
        "where muziek_album_tracks.album_id = {} order by volgnr".format(album_id))


def main():
    """simple test: print data
    """
    with open("test_albums_output", "w") as _out:
        print(list_artists(DB), file=_out)
        print(list_albums(DB, 1), file=_out)
        print(list_tracks(DB, 1), file=_out)


def restore_artists():
    """needed to copy artists over from an older database after I replaced them
    with references to the screen fields during testing
    """
    fromdb = '/home/albert/projects/albums/albums/pythoneer.db'
    todb = '/home/albert/projects/albums/albums/albums.db'
    with sqlite3.connect(fromdb) as conn:
        cur = conn.cursor()
        query = 'select * from muziek_act'
        result = cur.execute(query)
        data = {x[0]: (x[1], x[2]) for x in result}

        ## data = cur.fetchall()
    print(data)
    # niet weggoien en opnieuw opvoeren: waarden vervangen
    # dan data iets slimmer opzetten

    with sqlite3.connect(todb) as conn:
        cur = conn.cursor()
        ## cur.execute('delete from muziek_act')
        for key, names in data.items():
            cur.execute('update muziek_act set first_name = ?, last_name = ?'
                        ' where id = ?', (names[0], names[1], key))
        conn.commit()


if __name__ == "__main__":
    ## main()
    restore_artists()
