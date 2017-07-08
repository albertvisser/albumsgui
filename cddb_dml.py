import struct
import collections
import logging
logging.basicConfig(filename='/tmp/cddb.log',level=logging.DEBUG)
Album = collections.namedtuple('Album', ['cddbid', 'title', 'jaar', 'genre'])


def log(msg):
    logging.info(msg)


def readstr(data, pos):
    result = []
    while data[pos] != 0x00:
        ## result.append(str(data[pos], encoding='latin-1'))
        result.append(chr(data[pos]))
        pos += 1
    return ''.join(result), pos + 1


def disc(data, pos, albumid, extra=False):
    "get albumdata"
    title, pos = readstr(data, pos)
    artist, pos = readstr(data, pos)
    genre = jaar = ''
    if extra:
        genre, pos = readstr(data, pos)
        jaar, pos = readstr(data, pos)
    id_, pos = readstr(data, pos)
    album = Album(id_, title, jaar, genre)
    ntracks = struct.unpack('=L', data[pos:pos+4])[0]
    pos += 4
    tracks = []
    while ntracks > 0:
        name, pos = readstr(data, pos)
        tracks.append(name)
        ntracks -= 1
    return artist, album, tracks


def cdinfo (data, pos):
    """get album info from "quick index"

    steeds 12 bytes waarvan de eerste het aantal tracks aangeeft,
    dan 4 bytes met een CD-ID, dan twee nulbytes,
    dan 4 bytes met het adres van de bijbehorende "albumdata",
    dit moet vermeerderd worden met ofset 000C
    """
    cd_id, data_start = struct.unpack('=QL', data[pos:pos+12])
    data_start += 12
    return cd_id, data_start


class CDDBData:

    def __init__(self, fnaam):
        self.artists = collections.defaultdict(list)
        self.albums = {} # collections.defaultdict(Album)
        self.tracks = {} # collections.defaultdict(list)
        self.error = self.read(fnaam)

    def read(self, fnaam):
        ok = False
        with open(fnaam, 'rb') as cddb:
            try:
                cddbdata = cddb.read()
            except IOError:
                return "Error reading file"
        # TODO: check if all data is read

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

        albumcount = len(all_albums)
        for albumid, datastart in all_albums:
            ## log('{} {}'.format(albumid, datastart))
            artist, album, tracks = disc(cddbdata, datastart, albumid, self.extra)
            ## log('{} {}'.format(artist, album))
            ## albumid = album.id
            self.artists[artist].append(albumid)
            self.albums[albumid] = album.title
            self.tracks[albumid] = tracks

    # new API functions
    def list_artists(self):
        return [x for x in self.artists]

    def list_albums(self, artist):
        return [(x, self.albums[x]) for x in self.artists[artist]]

    def list_tracks(self, album):
        return self.tracks[album]

def test_readstr():
    data = b'\x41\x48\x41\x00\x41\x41\x48\x00'
    print(readstr(data, 0))
    print(readstr(data, 1))
    print(readstr(data, 2))
    print(readstr(data, 3))
    print(readstr(data, 4))


def main():
    ## test_readstr()
    db = '/home/albert/projects/albumsgui/oude data/IN_CDDA_wa5.cdb'
    test = CDDBData(db)
    if test.error:
        print(test.error)
        return
    with open('cddb_all_artists', 'w') as _o:
        for item in test.artists.items():
            print(item, file=_o)
    with open('cddb_all_albums', 'w') as _o:
        for item in test.albums.items():
            print(item, file=_o)
    with open('cddb_all_tracks', 'w') as _o:
        for item in test.tracks.items():
            print(item, file=_o)
    artistlist = test.list_artists()
    with open('cddb_artistlist', 'w') as _o:
        print(artistlist, file=_o)
    albumlist = test.list_albums(artistlist[10])
    print(albumlist)
    print(test.list_tracks(albumlist[0][0]))

if __name__ == '__main__':
    main()