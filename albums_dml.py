"""dml for Albums webapp database
"""
import sqlite3
from contextlib import closing
from banshee_settings import databases
DB = databases['albums']
SEL = {'studio': "label != ''", 'live': "label = ''"}
ORDER = {'Uitvoerende': 'order by muziek_act.last_name',
         'Titel': 'order by name',
         'Jaar': 'order by release_year',
         'Niet sorteren': '',
         'Locatie': 'order by name',
         'Datum': 'order by substr(naam, len(naam)-4)'}


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
        db, "select id, first_name, last_name from muziek_act order by last_name;")


def list_albums(db, artist_id):
    """produce list of albums for artist
    """
    return execute_query(
        db, "select id, name from muziek_album where artist_id = {}".format(artist_id))


def list_albums_by_artist(db, albumtype, artist_id, order_by):
    """produce list of albums for artist (sorted)
    """
    seltxt = SEL[albumtype]
    sort = ORDER[order_by] if order_by != 'Uitvoerende' else ''
    return execute_query(
        db, "select id, name from muziek_album where artist_id = {} and {} {}".format(
            artist_id, seltxt, sort))


def list_albums_by_search(db, albumtype, search_type, search_for, order_by):
    """produce list of albums by tesxt search and sorted
    """
    seltxt = SEL[albumtype]
    sort = ORDER[order_by]
    if sort:
        sort += 'and '
    if search_type == '*':
        colsel = ''
    else:
        colsel = 'and {} like "%{}%"'.format(search_type, search_for)
    return execute_query(
        db, 'select muziek_album.id, name, first_name, last_name from muziek_album '
        'inner join muziek_act on muziek_album.artist_id = muziek_act.id '
        'where {} {} {}'.format(seltxt, colsel, sort))


def list_album_details(db, album_id):
    """get album details
    """
    return execute_query(
        db, 'select * from muziek_album '
        'inner join muziek_act on muziek_album.artist_id = muziek_act.id '
        'where muziek_album.id = {}'.format(album_id))


def list_tracks(db, album_id):
    """produce list of tracks for album
    """
    return execute_query(
        db, "select volgnr, name, written_by, credits from muziek_song inner join "
        "muziek_album_tracks on muziek_song.id = muziek_album_tracks.song_id "
        "where muziek_album_tracks.album_id = {} order by volgnr".format(album_id))


def list_recordings(db, album_id):
    """produce list of recordings for album
    """
    return execute_query(
        db, "select type, oms from muziek_opname inner join "
        "muziek_album_opnames on muziek_opname.id = muziek_album_opnames.opname_id "
        "where muziek_album_opnames.album_id = {} order by type".format(album_id))


def main():
    """simple test: print data
    """
    with open("test_albums_output", "w") as _out:
        print(list_artists(DB), file=_out)
        print(list_albums(DB, 1), file=_out)
        print(list_tracks(DB, 1), file=_out)

if __name__ == "__main__":
    main()
