import sqlite3
from contextlib import closing
db = '/home/albert/projects/albums/albums/albums.db'
SEL = {'studio': "label != ''", 'live': "label = ''"}
ORDER = {
        'Uitvoerende': 'order by muziek_act.last_name',
        'Titel': 'order by name',
        'Jaar': 'order by release_year',
        'Niet sorteren': '',
        'Locatie': 'order by name',
        'Datum': 'order by substr(naam, len(naam)-4)',
        }


def execute_query(db, query):
    result = []
    with closing(sqlite3.connect(db)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for row in cur.execute(query):
            result.append({name: row[name] for name in row.keys()})
    return result


def list_artists(db):
    return execute_query(db, "select id, first_name, last_name from muziek_act "
        "order by last_name;")


def list_albums(db, artist_id):
    return execute_query(db, "select id, name from muziek_album "
        "where artist_id = {}".format(artist_id))


def list_albums_by_artist(db, albumtype, artist_id, order_by):
    seltxt = SEL[albumtype]
    sort = ORDER[order_by] if order_by != 'Uitvoerende' else ''
    print("select id, name from muziek_album "
        "where artist_id = {} and {} {}".format(artist_id, seltxt, sort))
    return execute_query(db, "select id, name from muziek_album "
        "where artist_id = {} and {} {}".format(artist_id, seltxt, sort))


def list_albums_by_search(db, albumtype, search_type, search_for, order_by):
    seltxt = SEL[albumtype]
    sort = ORDER[order_by]
    if sort: sort += 'and '
    if search_type == '*':
        colsel = ''
    else:
        colsel = 'and {} like "%{}%"'.format(search_type, search_for)
    ## print('select muziek_album.id, name, first_name, last_name '
        ## 'from muziek_album inner join muziek_act on muziek_album.artist_id = '
        ## 'muziek_act.id where {} {} {}'.format(seltxt, colsel, sort))
    return execute_query(db, 'select muziek_album.id, name, first_name, last_name '
        'from muziek_album inner join muziek_act on muziek_album.artist_id = '
        'muziek_act.id where {} {} {}'.format(seltxt, colsel, sort))


def list_album_details(db, album_id):
    return execute_query(db, 'select * from muziek_album '
        'inner join muziek_act on muziek_album.artist_id = muziek_act.id '
        'where muziek_album.id = {}'.format(album_id))


def list_tracks(db, album_id):
    return execute_query(
        db, "select volgnr, name, written_by, credits from muziek_song inner join "
        "muziek_album_tracks on muziek_song.id = muziek_album_tracks.song_id "
        "where muziek_album_tracks.album_id = {} order by volgnr".format(album_id))


def list_recordings(db, album_id):
    return execute_query(db, "select type, oms from muziek_opname inner join "
        "muziek_album_opnames on muziek_opname.id = muziek_album_opnames.opname_id "
        "where muziek_album_opnames.album_id = {} order by type".format(album_id))


def main():
    with open("test_albums_output", "w") as _out:
        print(list_artists(db), file=_out)
        print(list_albums(db, 1), file=_out)
        print(list_tracks(db, 1), file=_out)

if __name__ == "__main__":
    main()
