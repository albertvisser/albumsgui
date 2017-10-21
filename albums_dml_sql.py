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
        db, "select muziek_song.id, volgnr, name, written_by, credits "
        "from muziek_song inner join "
        "muziek_album_tracks on muziek_song.id = muziek_album_tracks.song_id "
        "where muziek_album_tracks.album_id = {} order by volgnr".format(album_id))


def main():
    """simple test: print data
    """
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute('delete from muziek_song where id = 10644;')
        cur.execute('delete from muziek_song where id = 10645;')
        cur.execute('delete from muziek_song where id = 10646;')
        ## cur.execute('update muziek_song set name = "Anthrax" where id = 1697;')
        ## cur.execute('update muziek_song set volgnr = 6 where id = 4100;')
        conn.commit()
    with open("/tmp/tracks", "w") as _out:
        ## print(list_artists(DB), file=_out)
        ## for item in list_albums(DB, 110):
            ## print(item, file=_out)
        for item in list_tracks(DB, 458):
            print(item, file=_out)


def restore_artists():
    """needed to copy artists over from an older database after I replaced them
    with references to the screen fields during testing
    """
    fromdb = '/home/albert/projects/albums/albums/pythoneer.db'
    todb = DB
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


def read_tracks_to_correct(inlist):
    """correct entries created with albumsmatcher stage 1: get tracks
    """
    outstuff = []
    for album_id in inlist:
        data =  execute_query(
            DB, "select muziek_song.id, volgnr, name from muziek_song inner join "
            "muziek_album_tracks on muziek_song.id = muziek_album_tracks.song_id "
            "where muziek_album_tracks.album_id = {} order by muziek_song.id".format(
            album_id))
        for item in data:
            outstuff.append((album_id, item['id'], item['volgnr'], item['name']))
    with open('/tmp/tracks', 'w') as _out:
        for item in outstuff:
            print(item, file=_out)

def update_corrected_tracks():
    """correct entries created with albumsmatcher stage 2: write them back
    """
    with open('/tmp/tracks') as _in:
        data = _in.readlines()
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        for line in data:
            _, trackid, volgnr, name = line.strip()[1:-1].split(', ', 3)
            name = name[1:-1]
            ## cur.execute("update muziek_song set volgnr = ? where id = ?",
                ## (volgnr, trackid))
            cur.execute("update muziek_song set name = ? where id = ?",
                (name, trackid))
        conn.commit()



if __name__ == "__main__":
    main()
    ## restore_artists()
    ## update_corrected_tracks()
    ## read_tracks_to_correct((457,))
