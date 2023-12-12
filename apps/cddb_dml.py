"""dml voor CDDB database (winamp 5)
"""
import struct
import collections
from .banshee_settings import databases
DB = databases['CDDB']
Album = collections.namedtuple('Album', ['cddbid', 'title', 'jaar', 'genre'])
valid_headers = {(0x0D, 0xF0, 0xEF, 0xBE): False, (0x0E, 0xF0, 0xEF, 0xBE): True}


def get_artists_lists():
    "provide artist data for banshee_gui"
    data = sorted(CDDBData(DB).list_artists())
    return data, data


def get_albums_lists(artist):
    "provide album data for banshee_gui"
    data = CDDBData(DB).list_albums(artist)
    return [x[0] for x in data], [x[1] for x in data]


def get_tracks_lists(artist, album):
    "provide track data for banshee_gui"
    # artist argument is alleen voor API-compatibility
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
        with open(fnaam, 'rb') as cddb:
            cddbdata = cddb.read()

        test = struct.unpack('4B', cddbdata[:4])
        if test in valid_headers:
            self.extra = valid_headers[test]
        else:
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
        return ''

    # new API functions
    def list_artists(self):
        """produce a list of artists
        """
        return list(self.artists)

    def list_albums(self, artist):
        """produce a list of albums for an artist
        """
        return [(x, self.albums[x]) for x in self.artists[artist]]

    def list_tracks(self, album):
        """produce a list of tracks for an album
        """
        return self.tracks[album]


def readstr(data, pos):
    """read some bytes as a null-delimited ascii string
    returns the string and the position after the end
    """
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
