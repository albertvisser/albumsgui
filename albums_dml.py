import sqlite3
from contextlib import closing
db = '/home/albert/projects/albums/albums/albums.db'
SEL = {'studio': "label != ''", 'live': "label = ''"}
ORDER = {
    'studio': {'Uitvoerende': 'order by artist_id',
               'Titel': 'order by name',
                'Jaar': 'order by release_year',
                'Niet sorteren': ''},
    'live': {'Uitvoerende': 'order by artist_id',
            'Locatie': 'order by name',
            'Datum': 'order by substr(naam, len(naam)-4)',
            'Niet sorteren': ''}
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
    sort = ORDER[albumtype][order_by]
    return execute_query(db, "select id, name from muziek_album "
        "where artist_id = {} and {} {}".format(artist_id, seltxt, sort))

def list_albums_by_search(db, albumtype, search_type, search_for, order_by):
    seltxt = SEL[albumtype]
    sort = ORDER[albumtype][order_by]
    if search_type == '*':
        colsel = ''
    else:
        colsel = 'and {} like "%{}%"'.format(search_type, search_for)
    return execute_query(db, "select id, name from muziek_album "
        "where {} {} {}".format(seltxt, colsel, sort))


def list_tracks(db, album_id):
    return execute_query(db, "select volgnr, name from muziek_song inner join "
        "muziek_album_tracks on muziek_song.id = muziek_album_tracks.song_id "
        "where muziek_album_tracks.album_id = {} order by volgnr".format(album_id))

def main():
    with open("test_albums_output", "w") as _out:
        print(list_artists(db), file=_out)
        print(list_albums(db, 1), file=_out)
        print(list_tracks(db, 1), file=_out)

if __name__ == "__main__":
    main()
