"""dml voor CDDB database (winamp 5)
"""
import struct
import collections
import logging
from .banshee_settings import databases
DB = databases['CDDB']
logging.basicConfig(filename='/tmp/cddb.log', level=logging.DEBUG)
Album = collections.namedtuple('Album', ['cddbid', 'title', 'jaar', 'genre'])


def log(msg):
    "log a message"
    logging.info(msg)


def readstr(data, pos):
    "read some bytes as a null-delimited ascii string"
    result = []
    while data[pos] != 0x00:
        ## result.append(str(data[pos], encoding='latin-1'))
        result.append(chr(data[pos]))
        pos += 1
    return ''.join(result), pos + 1


def disc(data, pos, extra=False):
    """get albumdata
    """
    title, pos = readstr(data, pos)
    artist, pos = readstr(data, pos)
    genre = jaar = ''
    if extra:
        genre, pos = readstr(data, pos)
        jaar, pos = readstr(data, pos)
    id_, pos = readstr(data, pos)
    album = Album(id_, title, jaar, genre)
    ntracks = struct.unpack('=L', data[pos:pos + 4])[0]
    pos += 4
    tracks = []
    while ntracks > 0:
        name, pos = readstr(data, pos)
        tracks.append(name)
        ntracks -= 1
    return artist, album, tracks


def cdinfo(data, pos):
    """get album info from "quick index"

    steeds 12 bytes waarvan de eerste het aantal tracks aangeeft,
    dan 4 bytes met een CD-ID, dan twee nulbytes,
    dan 4 bytes met het adres van de bijbehorende "albumdata",
    dit moet vermeerderd worden met ofset 000C
    """
    cd_id, data_start = struct.unpack('=QL', data[pos:pos + 12])
    data_start += 12
    return cd_id, data_start


def get_artist_lists():
    "provide artist data for banshee_gui"
    data = sorted(CDDBData(DB).list_artists())
    return data, data

def get_albums_lists(artist):
    "provide album data for banshee_gui"
    data = CDDBData(DB).list_albums(artist)
    return [x[0] for x in data], [x[1] for x in data]

def get_track_lists(album):
    "provide track data for banshee_gui"
    data = CDDBData(DB).list_tracks(album)
    trackids, tracknames = [], []
    for x, y in enumerate(data):
        trackids.append(x)
        tracknames.append(y)
    return trackids, tracknames


class CDDBData:
    """Internal represeantation of a CDDB database file
    """
    def __init__(self, fnaam):
        self.artists = collections.defaultdict(list)
        self.albums = {}
        self.tracks = {}
        self.error = self.read(fnaam)

    def read(self, fnaam):
        "read the file into memory"
        ok = False
        with open(fnaam, 'rb') as cddb:
            try:
                cddbdata = cddb.read()
            except IOError:
                return "Error reading file"

        test = struct.unpack('4B', cddbdata[:4])
        if test[1] == 0xF0 and test[2] == 0xEF and test[3] == 0xBE:
            if test[0] == 0x0D:
                self.extra = False
                ok = True
            elif test[0] == 0x0E:
                self.extra = True
                ok = True
        if not ok:
            return "Beginning of file does not look ok"

        pos = struct.unpack('=L', cddbdata[4:8])[0]
        all_albums = []
        while pos < len(cddbdata):
            all_albums.append(cdinfo(cddbdata, pos))
            pos += 12

        ## albumcount = len(all_albums)
        for albumid, datastart in all_albums:
            ## log('{} {}'.format(albumid, datastart))
            artist, album, tracks = disc(cddbdata, datastart, self.extra)
            ## log('{} {}'.format(artist, album))
            ## albumid = album.id
            self.artists[artist].append(albumid)
            self.albums[albumid] = album.title
            self.tracks[albumid] = tracks

    # new API functions
    def list_artists(self):
        """produce a list of artists
        """
        return [x for x in self.artists]

    def list_albums(self, artist):
        """produce a list of albums for an artist
        """
        return [(x, self.albums[x]) for x in self.artists[artist]]

    def list_tracks(self, album):
        """produce a list of tracks for an album
        """
        return self.tracks[album]


def test_readstr():
    """test routine
    """
    data = b'\x41\x48\x41\x00\x41\x41\x48\x00'
    print(readstr(data, 0))
    print(readstr(data, 1))
    print(readstr(data, 2))
    print(readstr(data, 3))
    print(readstr(data, 4))
