import pytest
import app.albumsmatcher as testee


def build_artist_name(first, last):
    return name


def build_album_name(album):
    try:
        name, year = album.name, album.release_year
    except AttributeError:
    if year:
    return name


def save_appdata(appdata):
    """save application data to json file
    """
    try:
    except FileNotFoundError:


def load_appdata():
    """load application data from json file
    """
    try:
    except FileNotFoundError:
    return appdata


def read_artists():
    return list_a, list_c


def update_artists(artists_list):
    for item in new_artists:
        if a_name in keys:
    return new_keys


def read_artist_albums(id, name):
    return list_a, list_c


def read_albums_tracks(id, artist_name, album_name):
    return list_a, list_c


def popuptext(item, colno):
    if item.text(2):
        if colno == 1:
    elif colno == 0:


@contextlib.contextmanager
def wait_cursor(win):


class CompareArtists(qtw.QWidget):
    def create_widgets(self):

    def create_actions(self):
        for text, callback, keys in actions:

    def refresh_screen(self, artist=None):
        for item in self.artist_list_c:
            if item:
        for item in self.artist_list_a:

    def set_modified(self, value):

    def focus_artist(self, artist=None):
        """select given artist or first unhandled one in left-hand side list
        """
        if artist:
        else:
        if test:
        else:

    def focus_next(self):

    def focus_prev(self):

    def focus_item(self, forward=True):
        if test:
            if not forward:
            for item in test:
                if forward and index.row() > current.row():
                elif not forward and index.row() < current.row():
        else:
        if item:
        else:

    def check_deletable(self):
        if item in self.new_artists:

    def select_and_go(self):
        if not item:
        if not self.artist_map[search]:

    def find_artist(self):
        if not item:
            return
        if self.artist_map[item.text(0)]:
            if ok == qtw.QMessageBox.No:
                return
        try:
            found = self.lookup[search]
        except KeyError:
            if len(test) == 1:
            else:
                try:
                    found = self.lookup[search]
                except KeyError:
        if found:
            for a_item in find:  # only keep unmatched artists
                if a_item.text(2) in self.artist_map.values():
                    continue
            if ok:
                return

    def update_item(self, new_item, from_item):
        if nxt:

    def copy_artist(self):

    def add_artist(self):
        if dlg != qtw.QDialog.Accepted:
            return
        if not item:
            if result:
        if not item:
            return

        if results:
            if ok:
        if not a_item:

    def delete_artist(self):
        if item is None:
        if ok != qtw.QMessageBox.Ok:
        try:
            name = self.new_matches.pop(a_itemkey)
        except KeyError:
        if name and self.artist_map[name] == a_itemkey:

    def save_all(self):
        for i in range(self.albums_artists.topLevelItemCount()):
        for key, value in new_keys.items():

    def help(self):


class NewArtistDialog(qtw.QDialog):
    """show dialog for adding a new artist
    """
    def __init__(self, parent, name=''):

    def update(self):
        if not fname and not lname:


class CompareAlbums(qtw.QWidget):
    """albums uit Clementine naast albums uit Albums zetten
    """
    def create_widgets(self):

    def create_actions(self):
        for text, callback, keys in actions:

    def refresh_screen(self, artist=None):
        if self._parent.artist_map:
        else:
            return "Please match some artists first"
        for ix in range(self.clementine_albums.topLevelItemCount()):
            if item.text(1) == 'X':
        if artist:
            try:
                self.artist_list.setCurrentIndex(artist)
            except TypeError:
                try:
                    indx = self.c_artists.index(artist)
                except ValueError:
                    qtw.QMessageBox.information(self, self._parent.title, "This "
                                                "artist has not been matched yet")
                    return

    def set_modified(self, value):

    def update_navigation_buttons(self):
        if test == 0:
        if test == len(self.c_artists) - 1:

    def get_albums(self):
        if self.artist_list.count() == 0:   # this happens when the panel is reshown
        for name, year, id, *rest in self.albums_to_save[self.c_artist]:
        for item, year in c_albums:
            try:
                new.setText(1, str(self.albums_map[self.c_artist][item][1]))
            except KeyError:
        for item in a_albums:

    def focus_albums(self):
        for ix in range(self.clementine_albums.topLevelItemCount()):
            if not item.text(1):
        else:

    def next_artist(self):
        if test < self.artist_list.count():

    def prev_artist(self):
        if test >= 0:

    def find_album(self):
        if not item:
        if item.text(0) in self.albums_map[self.c_artist]:
            if ok == qtw.QMessageBox.No:
        for album in albums:
            for a_item in self.albums_map[self.c_artist].values():
                if a_item[1] == test:
            if not found:
        if album_list:
            if ok:
                if c_year:
                    if c_year != a_year:
                        if ok == qtw.QMessageBox.Yes:

    def update_item(self, new_item, from_item):
        if nxt:

    def add_album(self):
        if dlg != qtw.QDialog.Accepted:
        if not item:
            if result:
        if not item:

        if results:
            if ok:
        if not a_item:

    def save_all(self):
        """save changes (additions) to Albums database
        """
        for key, albums in self.albums_to_update.items():
        with wait_cursor(self._parent):
            for artist, albumdata in self.albums_to_save.items():
                if not albumdata:
                for name, year, key, is_live, tracks in albumdata:
                    if key == 'X':
                for c_name, value in self.albums_map[artist].items():
                    try:
                        test = albums_map_lookup[a_name]
                    except KeyError:
                    if id != test:

    def help(self):


class NewAlbumDialog(qtw.QDialog):
    def __init__(self, parent, name='', year=''):

    def update(self):
        if not name:


class CompareTracks(qtw.QWidget):
    """tracks uit Clementine naast tracks uit Albums zetten
    """
    def create_widgets(self):

    def create_actions(self):
        for text, callback, keys in actions:

    def refresh_screen(self, artist=None, album=None, modifyoff=True):
        if modifyoff:
        if self._parent.artist_map:
        else:
        if artist:
            try:
                self.artists_list.setCurrentIndex(artist)
            except TypeError:
                try:
                    indx = self.c_artists.index(artist)
                except ValueError:
                    qtw.QMessageBox.information(self, self._parent.title, "This "
                                                "artist has not been matched yet")
                    return
        if album:
        return ''

    def get_albums(self):

    def update_navigation_buttons(self):
        if test == 0:
        if test == len(self.c_artists) - 1:
        if test == 0:
        if test == len(self.c_albums) - 1:

    def get_tracks(self):
        if self.artists_list.count() == 0:  # this happens when the panel is reshown
        if self.albums_list.count() == 0:   # this happens during screen buildup
        if not self.albums_map[self.artist]:
        try:
            self.a_album = self.albums_map[self.artist][self.c_album][1]
        except KeyError:
        for item in c_tracks:
        for item in a_tracks:
        if len(c_tracks) != len(a_tracks):
        else:
            for ix, item in enumerate(a_tracks):
                try:
                    if not (item.startswith(c_tracks[ix][0]) or c_tracks[ix][0].startswith(item)):
                except IndexError:

    def next_artist(self):
        if test < self.artists_list.count():

    def prev_artist(self):
        if test >= 0:

    def next_album(self):
        if test < self.albums_list.count():

    def prev_album(self):
        if test >= 0:

    def copy_tracks(self):
        for ix in range(self.clementine_tracks.topLevelItemCount()):
        with wait_cursor(self._parent):

    def unlink(self):
        for item in self.albums_map[self.artist].values():
            if item[1] == album_id:
        if not still_present:

    def save_all(self):

    def help(self):


class MainFrame(qtw.QMainWindow):
    def __init__(self, parent=None, app=None):
        if app:
        else:
        if appdata:
        for ix, item in enumerate([('artists', CompareArtists(self)),
                                   ('albums', CompareAlbums(self)),
                                   ('tracks', CompareTracks(self))]):
        if not app:

    def page_changed(self):
        if self.current >= 0:
            if self.not_again:
            else:
                if not ok:
        if go.first_time:
        if msg:


    def check_oldpage(self, pageno):
        if self.pages[pageno][1].modified:
        return True

    def exit(self):
        if self.check_oldpage(self.current):
