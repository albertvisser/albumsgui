import pytest
import apps.albums_gui as testee


def get_artist_list():
    return [x for x in dmla.list_artists()]


def get_albums_by_artist(albumtype, search_for, sort_on):
    return [x for x in dmla.list_albums_by_artist(albumtype, search_for, sort_on)]


def get_albums_by_text(albumtype, search_type, search_for, sort_on):
    if albumtype == 'studio':
    elif albumtype == 'live':
    return [x for x in dmla.list_albums_by_search(albumtype, search_type, search_for, sort_on)]


def get_album(album_id, albumtype):
    """get the selected album's data
    """
    result = {'titel': '',
              'artist': '',
              'artistid': '',
              'details': [('Label/jaar:', ''),
                          ('Produced by:', ''),
                          ('Credits:', ''),
                          ('Bezetting:', ''),
                          ('Tevens met:', '')],
              'tracks': {},
              'opnames': []}
    if album_id:
        if album.release_year:
            if text:
        if album:
    if albumtype == 'live':
    return result


def build_heading(win, readonly=False):
    """Generate heading text for screen
    """
    if not win.parent().albumdata['artist'] or not win.parent().albumdata['titel']:
    else:
        for text in ('tracks', 'opnames'):
            if wintext == text:
            elif wintext.endswith(text):
    return text


def newline(parent):
    return hbox


def button_strip(parent, *buttons):
    if 'Cancel' in buttons:
    if 'Go' in buttons:
    if 'GoBack' in buttons:
    if 'Edit' in buttons:
    if 'New' in buttons:
    if 'Select' in buttons:
    if 'Start' in buttons:
    return hbox


def exitbutton(parent, callback, extrawidget=None):
    if extrawidget:
    return hbox


class MainFrame(qtw.QMainWindow):
    def __init__(self):

    def get_all_artists(self):

    def do_start(self):

    def do_select(self):
        if self.albumtype == 'artist':
        else:
            if self.searchtype == 1:
            else:

    def do_new(self, keep_sel=False):
        if self.albumtype == 'artist':
            if NewArtistDialog(self).exec_() == qtw.QDialog.Accepted:
        else:

    def do_detail(self):
        if self.albumtype == 'artist':
        else:

    def do_edit_alg(self, new=False, keep_sel=False):
        if new:

    def do_edit_trk(self):

    def do_edit_rec(self):

    def start_import_tool(self):


class Start(qtw.QWidget):
    """show initial screen asking what to do
    """
    def create_widgets(self):

    def refresh_screen(self):
        if self.parent().albumtype == 'studio':
        elif self.parent().albumtype == 'live':
        else:
        if self.parent().searchtype == 1:
            if self.parent().artist:  # .id:
        if self.parent().searchtype < 2:
        else:

    def select_album(self):

    def select_concert(self):

    def _select(self, albumtype, typewin, actwin, argwin, sortwin):
        if self.parent().searchtype == 1:
            if chosen:
            else:
        elif self.parent().searchtype > 0:
            if not self.parent().search_arg:
        if text:

    def new_album(self):

    def new_concert(self):

    def _new(self, albumtype):

    def view_artists(self):

    def new_artist(self):

    def exit(self):


class Select(qtw.QWidget):
    def create_widgets(self):
        if self.parent().searchtype == 1:
        else:
        if not (self.parent().albumtype == 'studio'
                and self.parent().searchtype in (3, 4)):
        for album in self.parent().albums:

    def refresh_screen(self):
        if self.parent().searchtype == 1:
        else:
            if self.parent().searchtype:
            else:
        if self.parent().albumtype == 'studio':
            if self.parent().searchtype not in (3, 4):
        else:

    def other_artist(self):
        if chosen:
            if self.parent().searchtype == 1:

    def other_search(self):
        if test:

    def other_albumtype(self):
        if self.parent().albumtype == 'studio':
            if self.parent().searchtype == 5:
            elif self.parent().searchtype == 2 and self.parent().old_seltype:
        else:
            if self.parent().searchtype == 4:
            elif self.parent().searchtype in (2, 3):
                if self.parent().searchtype == 3:

    def todetail(self):
        for ix, btn in enumerate(self.go_buttons):
            if self.sender() == btn:
        if not self.parent().album:

    def add_new_to_sel(self):

    def exit(self):


class Detail(qtw.QWidget):
    def create_widgets(self):
        for caption, text in self.parent().albumdata['details']:
        for trackindex, data in sorted(self.parent().albumdata['tracks'].items()):
            if cred:
        for opnindex, opname in enumerate(self.parent().albumdata['opnames']):

    def refresh_screen(self):

    def other_album(self):
        """Determine which other album to show and do so
        """
        if test:

    def edit_alg(self):

    def edit_trk(self):

    def edit_rec(self):

    def exit(self):


class EditDetails(qtw.QWidget):
    def create_widgets(self):
        if self.parent().albumtype == 'live':
        for caption, text in data:
            if caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
            else:
            if caption == 'Uitvoerende:':
                if text:
            elif caption == 'Label/jaar:':
                if len(text) == 1:
                    text.append('')
            elif caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
            else:
            if caption == 'Label/jaar:':
            else:

        if not self.parent().album:
            if not self.parent().search_arg:

    def new_data(self, keep_sel=False):
        if not keep_sel:
        for lbl, win in self.screendata[:2]:
            if self.parent().searchtype == 1 and caption == 'Uitvoerende:':
            elif self.parent().searchtype == 2:
                if self.parent().albumtype == 'studio' and caption == 'Albumtitel:':
                elif self.parent().albumtype == 'live' and caption == 'Locatie/datum:':
            elif self.parent().searchtype == 3:
                if self.parent().albumtype == 'studio' and caption == 'Produced by:':
                elif self.parent().albumtype == 'live' and caption == 'Locatie/datum:':
            elif self.parent().searchtype == 4:
                if self.parent().albumtype == 'studio' and caption == 'Credits:':
                elif self.parent().albumtype == 'live' and caption == 'Bezetting:':
            elif self.parent().searchtype == 5:
                if self.parent().albumtype == 'studio' and caption == 'Bezetting:':

    def refresh_screen(self):
        if not self.first_time:
            for i in range(self.bbox.count()):
                if btn:  # try:
                else:  # except AttributeError:
                if test == "Uitvoeren en terug":

    def submit(self, goback=False):
        def replace_details(caption, value):
            for ix, item in enumerate(self.parent().albumdata['details']):
                if item[0] == caption:
                    if value != item[1]:
            return changed
        for fields in self.screendata:
            if caption == 'Uitvoerende:':
                if test != self.parent().albumdata['artist']:
            elif caption in ('Albumtitel:', 'Locatie/datum:'):
                if test != self.parent().albumdata['titel']:
            elif caption == 'Label/jaar:':
                if test:
            elif caption in ('Credits:', 'Bezetting:', 'Tevens met:'):
                if test:
            else:
                if test:

        if is_changed:
            albumid = 0 if self.new_album else self.parent().album.id
            album, ok = dmla.update_album_details(albumid, self.parent().albumdata)
            # eigenlijk wil ik hier de nieuwe waarden teruggeven om ze op het scherm te zetten
            # zodat je kunt zien wat er daadwerkelijk in de database zit / is bijgewerkt
            if ok:
                if not goback:
                    if self.new_album:
                        self.add_another()
                    else:
                        qtw.QMessageBox.information(self, 'Albums',
                                                    'Details updated')
            else:
                qtw.QMessageBox.information(self, 'Albums',
                                            'Something went wrong, please try again')
                return
            self.parent().album = album
            if self.new_album:
                self.parent().albums.append(album)
                self.new_album = False
            # eigenlijk zou je hierna de data opnieuw moeten ophalen en het scherm opnieuw
            # opbouwen - wat nu alleen gebeurt als je naar het detailscherm gaat
        else:
            qtw.QMessageBox.information(self, 'Albums', 'Nothing changed')

        if self.first_time:
            self.first_time = False
            self.refresh_screen()

    def add_another(self):
        if message.clickedButton() == next:

    def submit_and_back(self):
        if self.first_time:
            if self.keep_sel:
            else:
        else:

    def exit(self):


class EditTracks(qtw.QWidget):
    def create_widgets(self):
        for trackindex, data in sorted(self.parent().albumdata['tracks'].items()):
        if not self.parent().album:
            if not self.parent().search_arg:

    def add_track_fields(self, trackindex, trackname='', author='', text=''):

    def refresh_screen(self):

    def add_new_item(self):

    def submit(self, skip_confirm=False):
        for ix, wins in enumerate(self.widgets):
            try:
                data = self.parent().albumdata['tracks'][ix]
            except KeyError:
            for i, item in enumerate(data):
                if screen[i] != item:
            if changed:

        if tracks:
            if not skip_confirm:
                if ok:
                else:
        else:
        if self.first_time:

    def submit_and_back(self):

    def exit(self):
        """shutdown application"""
        self.parent().close()


class EditRecordings(qtw.QWidget):
    def create_widgets(self):
        for opnindex, opname in enumerate(self.parent().albumdata['opnames']):
        if not self.parent().album:
            if not self.parent().search_arg:

    def add_rec_fields(self, opnindex, opname=None):
        if opname:
        else:
        if opname:

    def refresh_screen(self):

    def add_new_item(self):

    def submit(self, skip_confirm=False):
        for ix, wins in enumerate(self.recwins):
            try:
                data = self.parent().albumdata['opnames'][ix]
            except IndexError:
            for i, item in enumerate(data):
                if screen[i] != item:
            if changed:

        if recordings:
            if not skip_confirm:
                if ok:
                else:
        else:
            if not skip_confirm:

        if self.first_time:

    def submit_and_back(self):

    def exit(self):


class Artists(qtw.QWidget):
    def create_widgets(self):
        for artist in self.artist_list:
            if test > self.last_artistid:

    def filter(self):
        """callback for Filter button
        """
        if filter:
        else:

    def add_artist_line(self, itemid, first_name='', last_name=''):

    def refresh_screen(self):

    def submit(self):
        for ix, wins in enumerate(self.fields):
            if ix < len(self.parent().artists):
                if fname != artist.first_name or lname != artist.last_name:
            else:
        if changed or new:
        else:

    def new(self):

    def exit(self):


class NewArtistDialog(qtw.QDialog):
    def __init__(self, parent):

    def update(self):
