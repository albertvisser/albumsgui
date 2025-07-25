"""fixture function for output predictions
"""
import pytest

start_all = """\
called Grid.__init__
called newline with arg Start
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (0, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Studio Albums', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Selecteer:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (2, 0)
called ComboBox.__init__
called ComboBox.addItems with arg ['Niet zoeken, alles tonen', 'Zoek op Uitvoerende: ', 'Zoek op Tekst in Titel', 'Zoek op Tekst in Producer', 'Zoek op Tekst in Credits', 'Zoek op Tekst in Bezetting']
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called Grid.addWidget with arg MockComboBox at (2, 1)
called HBox.__init__
called Label.__init__ with args ('Kies Uitvoerende:', {me})
called HBox.addWidget with arg MockLabel
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockComboBox
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (3, 1)
called HBox.__init__
called Label.__init__ with args ('Zoektekst voor 3-6:', {me})
called HBox.addWidget with arg MockLabel
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockLineEdit
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (4, 1)
called Label.__init__ with args ('Sorteer op:', {me})
called Grid.addWidget with arg MockLabel at (5, 0)
called ComboBox.__init__
called ComboBox.addItems with arg ['Niet sorteren', 'Uitvoerende', 'Titel', 'Jaar']
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called Grid.addWidget with arg MockComboBox at (5, 1)
called HBox.__init__
called PushButton.__init__ with args ('Selectie uitvoeren', {me}) {{}}
called PushButton.__init__ with args ('Nieuw album opvoeren', {me}) {{}}
called Signal.connect with args ({select_album},)
called Signal.connect with args ({new_album},)
called HBox.addWidget with arg MockPushButton
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (6, 0, 1, 3)
called newline with arg Start
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (7, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Live Concerten', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (8, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Selecteer:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (9, 0)
called ComboBox.__init__
called ComboBox.addItems with arg ['Niet zoeken, alles tonen', 'Zoek op Uitvoerende: ', 'Zoek op Tekst in Locatie', 'Zoek op Tekst in Datum', 'Zoek op Tekst in Bezetting']
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called Grid.addWidget with arg MockComboBox at (9, 1)
called HBox.__init__
called Label.__init__ with args ('Kies Uitvoerende:', {me})
called HBox.addWidget with arg MockLabel
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockComboBox
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (10, 1)
called HBox.__init__
called Label.__init__ with args ('Zoektekst voor 3-5:', {me})
called HBox.addWidget with arg MockLabel
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockLineEdit
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (11, 1)
called Label.__init__ with args ('Sorteer op:', {me})
called Grid.addWidget with arg MockLabel at (12, 0)
called ComboBox.__init__
called ComboBox.addItems with arg ['Niet sorteren', 'Uitvoerende', 'Locatie', 'Datum']
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called Grid.addWidget with arg MockComboBox at (12, 1)
called HBox.__init__
called PushButton.__init__ with args ('Selectie uitvoeren', {me}) {{}}
called PushButton.__init__ with args ('Nieuw album opvoeren', {me}) {{}}
called Signal.connect with args ({select_concert},)
called Signal.connect with args ({new_concert},)
called HBox.addWidget with arg MockPushButton
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (13, 0, 1, 3)
called HBox.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBox.addWidget with arg MockFrame
called Grid.addLayout with arg MockHBoxLayout at (14, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Uitvoerende Artiesten', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (15, 0, 1, 3)
called HBox.__init__
called PushButton.__init__ with args ('Lijst tonen/wijzigen', {me}) {{}}
called PushButton.__init__ with args ('Nieuwe opvoeren', {me}) {{}}
called HBox.addWidget with arg MockPushButton
called HBox.addWidget with arg MockPushButton
called Signal.connect with args ({view_artists},)
called Signal.connect with args ({new_artist},)
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (16, 0, 1, 3)
called newline with arg Start
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (17, 0, 1, 3)
called PushButton.__init__ with args ('&Import Data', {me}) {{}}
called Signal.connect with args ({start_imp},)
called exitbutton with args {me}, {exit}, MockPushButton
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (18, 0, 1, 3)
called Widget.setLayout with arg MockGridLayout
"""
select_top = """\
called VBox.__init__
called newline with arg Select
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Label.__init__ with args ('', {me})
called HBox.addWidget with arg MockLabel
called VBox.addLayout with arg MockHBoxLayout
"""
select_other_artist_button = """\
called HBox.__init__
called Label.__init__ with args ('Snel naar dezelfde selectie voor een andere artiest:', {me})
called HBox.addWidget with arg MockLabel
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg ['X', 'Y']
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockComboBox
called PushButton.__init__ with args ('Go', {me}) {{}}
called PushButton.setMaximumWidth with arg `40`
called Signal.connect with args ({other_artist},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
"""
select_other_type_button = """\
called HBox.__init__
called Label.__init__ with args ('of naar een soortgelijke selectie voor ', {me})
called HBox.addWidget with arg MockLabel
called PushButton.__init__ with args ('', {me}) {{}}
called Signal.connect with args ({other_albumtype},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
"""
select_other_search_button = """\
called HBox.__init__
called Label.__init__ with args ('Snel naar dezelfde selectie voor een andere waarde:', {me})
called HBox.addWidget with arg MockLabel
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockLineEdit
called PushButton.__init__ with args ('Go', {me}) {{}}
called PushButton.setMaximumWidth with arg `40`
called Signal.connect with args ({other_search},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
"""
select_start_data = """\
called newline with arg Select
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Label.__init__ with args ('Kies een item uit de lijst:', {me})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Frame.__init__
called VBox.__init__
"""
select_data_line_1 = """\
called HBox.__init__
called Label.__init__ with args ('1', {me})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called PushButton.__init__ with args ('Go', {me}) {{}}
called PushButton.setMaximumWidth with arg `40`
called Signal.connect with args ({todetail},)
called HBox.addWidget with arg MockPushButton
called HBox.addSpacing
called VBox.addLayout with arg MockHBoxLayout
"""
select_data_line_2 = """\
called HBox.__init__
called Label.__init__ with args ('2', {me})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called PushButton.__init__ with args ('Go', {me}) {{}}
called PushButton.setMaximumWidth with arg `40`
called Signal.connect with args ({todetail},)
called HBox.addWidget with arg MockPushButton
called HBox.addSpacing
called VBox.addLayout with arg MockHBoxLayout
"""
select_end_data = """\
called Frame.setLayout with arg MockVBoxLayout
called ScrollArea.__init__ with args ()
called ScrollArea.setWidget with arg `MockFrame`
called VBox.addWidget with arg MockScrollArea
called HBox.__init__
called Label.__init__ with args ('Of', {me})
called HBox.addWidget with arg MockLabel
called PushButton.__init__ with args ('voer een nieuw item op bij deze selectie', {me}) {{}}
called Signal.connect with args ({add_new_to_sel},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called newline with arg Select
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called button_strip with args ({me}, 'Start')
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called Widget.setLayout with arg MockVBoxLayout
"""
detail_all = """\
called Grid.__init__
called Label.__init__ with args ('', {me})
called HBox.__init__
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (0, 0, 1, 3)
called newline with arg Detail
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Snel naar een ander item in deze selectie:', {me})
called HBox.addWidget with arg MockLabel
called ComboBox.__init__
called ComboBox.addItem with arg `--- selecteer titel ---`
called ComboBox.addItems with arg ['xxx', 'yyy']
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockComboBox
called PushButton.__init__ with args ('Go', {me}) {{}}
called PushButton.setMaximumWidth with arg `40`
called Signal.connect with args ({other_album},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, 3)
called newline with arg Detail
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (3, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Detailgegevens:', {me})
called HBox.addWidget with arg MockLabel
called PushButton.__init__ with args ('wijzigen', {me}) {{}}
called Signal.connect with args ({edit_alg},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (4, 0, 1, 3)
called Frame.__init__
called Grid.__init__
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('x', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (0, 0, 1, 1)
called Label.__init__ with args ('y', {me})
called Grid.addWidget with arg MockLabel at (0, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('a', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 1)
called Label.__init__ with args ('b', {me})
called Grid.addWidget with arg MockLabel at (1, 1, 1, 2)
called Frame.setLayout with arg MockGridLayout
called ScrollArea.__init__ with args ()
called ScrollArea.setWidget with arg `MockFrame`
called Grid.addWidget with arg MockScrollArea at (5, 0, 1, 3)
called newline with arg Detail
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (6, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Tracks:', {me})
called HBox.addWidget with arg MockLabel
called PushButton.__init__ with args ('wijzigen', {me}) {{}}
called Signal.connect with args ({edit_trk},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (7, 0, 1, 3)
called Frame.__init__
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('       1.', {me})
called HBox.addWidget with arg MockLabel
called Label.__init__ with args ('a (b)', {me})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Label.__init__ with args ('c', {me})
called VBox.addWidget with arg MockLabel
called HBox.__init__
called Label.__init__ with args ('       2.', {me})
called HBox.addWidget with arg MockLabel
called Label.__init__ with args ('x (y)', {me})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Frame.setLayout with arg MockVBoxLayout
called ScrollArea.__init__ with args ()
called ScrollArea.setWidget with arg `MockFrame`
called Grid.addWidget with arg MockScrollArea at (8, 0, 1, 3)
called newline with arg Detail
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (9, 0, 1, 3)
called HBox.__init__
called Label.__init__ with args ('Opnames:', {me})
called HBox.addWidget with arg MockLabel
called PushButton.__init__ with args ('wijzigen', {me}) {{}}
called Signal.connect with args ({edit_rec},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (10, 0, 1, 3)
called Frame.__init__
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('       1.', {me})
called HBox.addWidget with arg MockLabel
called Label.__init__ with args ('p q', {me})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Label.__init__ with args ('       2.', {me})
called HBox.addWidget with arg MockLabel
called Label.__init__ with args ('r', {me})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Frame.setLayout with arg MockVBoxLayout
called ScrollArea.__init__ with args ()
called ScrollArea.setWidget with arg `MockFrame`
called Grid.addWidget with arg MockScrollArea at (11, 0, 1, 3)
called newline with arg Detail
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (12, 0, 1, 3)
called button_strip with args ({me}, 'Select', 'Start')
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (13, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (14, 0, 1, 3)
called Widget.setLayout with arg MockGridLayout
"""
editdetails_studio = """\
called Grid.__init__
called Label.__init__ with args ('', {me})
called HBox.__init__
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (0, 0, 1, 3)
called newline with arg EditDetails
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 3)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg ['xxx', 'bbb']
called ComboBox.setCurrentIndex with arg `1`
called Grid.addWidget with arg MockComboBox at (2, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Albumtitel:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (3, 0, 1, 1)
called LineEdit.__init__
called Grid.addWidget with arg MockLineEdit at (3, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Label/jaar:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (4, 0, 1, 1)
called HBox.__init__
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockLineEdit
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `80`
called LineEdit.setMinimumWidth with arg `80`
called HBox.addWidget with arg MockLineEdit
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (4, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Credits:', {me})
called VBox.__init__
called VBox.addWidget with arg MockLabel
called VBox.addStretch
called HBox.addLayout with arg MockVBoxLayout
called Grid.addLayout with arg MockHBoxLayout at (5, 0, 1, 1)
called Editor.__init__ with args ('q', {me})
called Grid.addWidget with arg MockEditorWidget at (5, 1, 1, 2)
called VBox.__init__
called VBox.addStretch
called Grid.addLayout with arg MockVBoxLayout at (6, 0, 1, 3)
called button_strip with args ({me}, 'Cancel', 'Go', 'GoBack', 'Select', 'Start')
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (7, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (8, 0, 1, 3)
called Widget.setLayout with arg MockGridLayout
"""
editdetails_live = """\
called Grid.__init__
called Label.__init__ with args ('', {me})
called HBox.__init__
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (0, 0, 1, 3)
called newline with arg EditDetails
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 3)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg ['xxx', 'bbb']
called ComboBox.setCurrentIndex with arg `1`
called Grid.addWidget with arg MockComboBox at (2, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Locatie/datum:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (3, 0, 1, 1)
called LineEdit.__init__
called Grid.addWidget with arg MockLineEdit at (3, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Bezetting:', {me})
called VBox.__init__
called VBox.addWidget with arg MockLabel
called VBox.addStretch
called HBox.addLayout with arg MockVBoxLayout
called Grid.addLayout with arg MockHBoxLayout at (4, 0, 1, 1)
called Editor.__init__ with args ('rr', {me})
called Grid.addWidget with arg MockEditorWidget at (4, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Tevens met:', {me})
called VBox.__init__
called VBox.addWidget with arg MockLabel
called VBox.addStretch
called HBox.addLayout with arg MockVBoxLayout
called Grid.addLayout with arg MockHBoxLayout at (5, 0, 1, 1)
called Editor.__init__ with args ('sss', {me})
called Grid.addWidget with arg MockEditorWidget at (5, 1, 1, 2)
called VBox.__init__
called VBox.addStretch
called Grid.addLayout with arg MockVBoxLayout at (6, 0, 1, 3)
called button_strip with args ({me}, 'Cancel', 'Go', 'GoBack', 'Select', 'Start')
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (7, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (8, 0, 1, 3)
called Widget.setLayout with arg MockGridLayout
"""
editdetails_studio_nw = """\
called Grid.__init__
called Label.__init__ with args ('', {me})
called HBox.__init__
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (0, 0, 1, 3)
called newline with arg EditDetails
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 3)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg ['xxx', 'bbb']
called Grid.addWidget with arg MockComboBox at (2, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Albumtitel:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (3, 0, 1, 1)
called LineEdit.__init__
called Grid.addWidget with arg MockLineEdit at (3, 1, 1, 2)
called VBox.__init__
called VBox.addStretch
called Grid.addLayout with arg MockVBoxLayout at (4, 0, 1, 3)
called button_strip with args ({me}, 'Go', 'GoBack', 'Start')
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (5, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (6, 0, 1, 3)
called Widget.setLayout with arg MockGridLayout
"""
editdetails_live_nw = """\
called Grid.__init__
called Label.__init__ with args ('', {me})
called HBox.__init__
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (0, 0, 1, 3)
called newline with arg EditDetails
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 3)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg ['xxx', 'bbb']
called Grid.addWidget with arg MockComboBox at (2, 1, 1, 2)
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('Locatie/datum:', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (3, 0, 1, 1)
called LineEdit.__init__
called Grid.addWidget with arg MockLineEdit at (3, 1, 1, 2)
called VBox.__init__
called VBox.addStretch
called Grid.addLayout with arg MockVBoxLayout at (4, 0, 1, 3)
called button_strip with args ({me}, 'Go', 'GoBack', 'Select', 'Start')
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (5, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called Grid.addLayout with arg MockHBoxLayout at (6, 0, 1, 3)
called Widget.setLayout with arg MockGridLayout
"""
edittracks_all_start = """\
called VBox.__init__
called Label.__init__ with args ('tracks', {me})
called HBox.__init__
called HBox.addWidget with arg MockLabel
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBox.addWidget with arg MockFrame
called VBox.addLayout with arg MockHBoxLayout
called Frame.__init__
called VBox.__init__
called Grid.__init__
called HBox.__init__
called Label.__init__ with args ('Title\\nCredits', {me})
called Label.setMinimumWidth with arg `304`
called Label.setMaximumWidth with arg `304`
called HBox.addWidget with arg MockLabel
called Label.__init__ with args ('Author\\n', {me})
called HBox.addWidget with arg MockLabel
called Grid.addLayout with arg MockHBoxLayout at (1, 1)
"""
edittracks_all_middle = """\
called EditTracks.add_track_fields with args (1, 'x')
called EditTracks.add_track_fields with args (2, 'a', 'c')
"""
track_fields = """\
called Label.__init__ with args ('       {num}.', {me})
called Grid.addWidget with arg MockLabel at (1, 0)
called HBox.__init__
called LineEdit.__init__ with args ('{text1}', {me})
called LineEdit.setMaximumWidth with arg `300`
called LineEdit.setMinimumWidth with arg `300`
called HBox.addWidget with arg MockLineEdit
called LineEdit.__init__ with args ('{text2}', {me})
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockLineEdit
called Grid.addLayout with arg MockHBoxLayout at (1, 1)
called Editor.__init__ with args ('{text3}', {me})
called Editor.setMaximumWidth with arg `508`
called Editor.setMinimumWidth with arg `508`
called Editor.setMaximumHeight with arg `38`
called Editor.setMinimumHeight with arg `38`
called Grid.addWidget with arg MockEditorWidget at (2, 1)
"""
edittracks_all_end_1 = """\
called VBox.addLayout with arg MockGridLayout
called VBox.addStretch
called Frame.setLayout with arg MockVBoxLayout
called ScrollArea.__init__ with args ()
called ScrollArea.setWidget with arg `MockFrame`
called ScrollArea.setWidgetResizable with arg `True`
called ScrollArea.verticalScrollBar
called VBox.addWidget with arg MockScrollArea
called HBox.__init__
called PushButton.__init__ with args ('Nieuw track', {me}) {{}}
called Signal.connect with args ({add_new_item},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBox.addWidget with arg MockFrame
called VBox.addLayout with arg MockHBoxLayout
"""
edittracks_all_buttonstrip_1 = """\
called button_strip with args ({me}, 'Go', 'GoBack', 'Start')
"""
edittracks_all_buttonstrip_2 = """\
called button_strip with args ({me}, 'Go', 'GoBack', 'Select', 'Start')
"""
edittracks_all_buttonstrip_3 = """\
called button_strip with args ({me}, 'Cancel', 'Go', 'GoBack', 'Select', 'Start')
"""
edittracks_all_end_2 = """\
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called Widget.setLayout with arg MockVBoxLayout
"""
editrecs_all_start = """\
called VBox.__init__
called Label.__init__ with args ('opnames', {me})
called HBox.__init__
called HBox.addWidget with arg MockLabel
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBox.addWidget with arg MockFrame
called VBox.addLayout with arg MockHBoxLayout
called Frame.__init__
called VBox.__init__
called VBox.addStretch
"""
editrecs_all_middle = """\
called EditRecordings.add_track_fields with args (0, (1, ('x', 'y')))
called EditRecordings.add_track_fields with args (1, (2, ('a', 'b')))
"""
rec_fields_start = """\
called HBox.__init__
called Label.__init__ with args ('       {num}.', {me})
called HBox.addWidget with arg MockLabel
called ComboBox.__init__
called ComboBox.addItem with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg ('x', 'y', 'z')
"""
rec_fields_middle = """called ComboBox.setCurrentIndex with arg `1`
"""
rec_fields_end = """\
called HBox.addWidget with arg MockComboBox
called LineEdit.__init__ with args ('{text}', {me})
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called HBox.addWidget with arg MockLineEdit
called HBox.addStretch
called VBox.count
called VBox.insertLayout with args ({insertpos}, MockHBoxLayout)
"""
editrecs_all_end_1 = """\
called Frame.setLayout with arg MockVBoxLayout
called ScrollArea.__init__ with args ()
called ScrollArea.setWidget with arg `MockFrame`
called ScrollArea.setWidgetResizable with arg `True`
called VBox.addWidget with arg MockScrollArea
called HBox.__init__
called PushButton.__init__ with args ('Nieuwe opname', {me}) {{}}
called Signal.connect with args ({add_new_item},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBox.addWidget with arg MockFrame
called VBox.addLayout with arg MockHBoxLayout
"""
editrecs_all_buttonstrip_1 = """\
called button_strip with args ({me}, 'Go', 'GoBack', 'Start')
"""
editrecs_all_buttonstrip_2 = """\
called button_strip with args ({me}, 'Go', 'GoBack', 'Select', 'Start')
"""
editrecs_all_buttonstrip_3 = """\
called button_strip with args ({me}, 'Cancel', 'Go', 'GoBack', 'Select', 'Start')
"""
editrecs_all_end_2 = """\
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called exitbutton with args ({me}, {exit}) {{}}
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called Widget.setLayout with arg MockVBoxLayout
"""
artists_all_start = """\
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Artiestenlijst - gefilterd op', {testobj})
called HBox.addWidget with arg MockLabel
called LineEdit.__init__
called HBox.addWidget with arg MockLineEdit
called PushButton.__init__ with args ('&Go', {testobj}) {{}}
called Signal.connect with args ({filter},)
called HBox.addWidget with arg MockPushButton
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBox.addWidget with arg MockFrame
called VBox.addLayout with arg MockHBoxLayout
called Frame.__init__
called VBox.__init__
"""
artists_all_middle = """\
called Artists.add_artist_line with args (1, 'a', 'b')
called Artists.add_artist_line with args (3, 'b', 'a')
called Artists.add_artist_line with args (2, 'x', 'y')
"""
artists_all_end = """\
called VBox.addStretch
called Frame.setLayout with arg MockVBoxLayout
called ScrollArea.__init__ with args ()
called ScrollArea.setWidget with arg `MockFrame`
called ScrollArea.setWidgetResizable with arg `True`
called ScrollArea.verticalScrollBar
called VBox.addWidget with arg MockScrollArea
called button_strip with args ({testobj}, 'Edit', 'New', 'Start')
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called exitbutton with args ({testobj}, {exit}) {{}}
called HBox.__init__
called VBox.addLayout with arg MockHBoxLayout
called Widget.setLayout with arg MockVBoxLayout
"""
artists_line = """\
called HBox.__init__
called Label.__init__ with args ('  {num}.', {testobj})
called HBox.addWidget with arg MockLabel
called LineEdit.__init__ with args ('{text1}', {testobj})
called HBox.addWidget with arg MockLineEdit
called LineEdit.__init__ with args ('{text2}', {testobj})
called LineEdit.setMaximumWidth with arg `300`
called LineEdit.setMinimumWidth with arg `300`
called HBox.addWidget with arg MockLineEdit
called VBox.addLayout with arg MockHBoxLayout
"""
artist_dialog = """\
called Widget.__init__
called Widget.__init__
called Grid.__init__
called Label.__init__ with args ('First name:', {testobj})
called Grid.addWidget with arg MockLabel at (0, 0)
called LineEdit.__init__
called Grid.addWidget with arg MockLineEdit at (0, 1)
called Label.__init__ with args ('Last name:', {testobj})
called Grid.addWidget with arg MockLabel at (1, 0)
called LineEdit.__init__
called Grid.addWidget with arg MockLineEdit at (1, 1)
called Label.__init__ with args ('Names wil be shown sorted on last name',)
called Grid.addWidget with arg MockLabel at (2, 0, 1, 2)
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('Cancel', {testobj}) {{}}
called Signal.connect with args ({reject},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('Update', {testobj}) {{}}
called Signal.connect with args ({update},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (3, 0, 1, 2)
called Widget.setLayout with arg MockGridLayout
"""
matcher_noapp = "called Application._init__\n"
matcher = """\
called Icon.__init__ with arg `/home/albert/projects/albumsgui/icons/go-bottom.png`
called Icon.__init__ with arg `/home/albert/projects/albumsgui/icons/go-top.png`
called Icon.__init__ with arg `/home/albert/projects/albumsgui/icons/go-down.png`
called Icon.__init__ with arg `/home/albert/projects/albumsgui/icons/go-up.png`
called MainWindow._init__ with args ()
called MainWindow.setWindowTitle with arg `AlbumsMatcher`
called MainWindow.move with args (300, 50)
called MainWindow.resize with args (600, 650)
called TabWidget.__init__
called Signal.connect with args ({page_changed},)
called Frame.__init__
called VBox.__init__
called HBox.__init__
called HBox.addWidget with arg MockTabWidget
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('E&xit', {parent}) {{}}
called Signal.connect with args ({exit},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Frame.setLayout with arg MockVBoxLayout
called MainWidget.setCentralWindow with arg `MockFrame`
called Action.__init__ with args ('Exit', {me})
called Signal.connect with args ({exit},)
called Action.setShortcut with arg `Ctrl+Q`
called MainWindow.addAction
called MainFrame.check_for_data
called MainFrame.settabs
called TabWidget.setCurrentIndex with arg `0`
called MainWindow.show
called MainFrame.go with arg `{app}`
"""
cmpart = """\
called HBox.__init__
called VBox.__init__
called create_treewidget with args ({testobj}, ['Artist', 'Match'], [-1, 50])
called Tree.__init__
called Signal.connect with args ({testobj.select_and_go},)
called VBox.addWidget with arg MockTreeWidget
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Help', {testobj}) {{}}
called Signal.connect with args ({testobj.help},)
called HBox.addWidget with arg MockPushButton
called create_updownbuttons with args ({testobj},) {{'seltext': 'Go to {{}} unmatched artist', 'icons': ('next_icon', 'prev_icon'), 'callbacks': ({testobj.focus_next}, {testobj.focus_prev})}}
called HBox.addLayout with arg SimpleNamespace
called PushButton.__init__ with args ('&Check Artist', {testobj}) {{}}
called Signal.connect with args ({testobj.find_artist},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.addLayout with arg MockVBoxLayout
called VBox.__init__
called create_treewidget with args ({testobj}, ['First Name', 'Last Name', 'Id'], (80, -1, 50))
called Tree.__init__
called Signal.connect with args ({testobj.check_deletable},)
called VBox.addWidget with arg MockTreeWidget
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Delete', {testobj}) {{}}
called Signal.connect with args ({testobj.delete_artist},)
called PushButton.setEnabled with arg `False`
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Save All', {testobj}) {{}}
called Signal.connect with args ({testobj.save_all},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.addLayout with arg MockVBoxLayout
called Widget.setLayout with arg MockHBoxLayout
"""
cmpart_act = """\
called Tree.__init__
called Action.__init__ with args ('Help', {me})
called Signal.connect with args ({help},)
called Action.setShortcuts with arg `['F1', 'Ctrl+H']`
called CompareArtists.addAction
called Action.__init__ with args ('Focus', {me})
called Signal.connect with args ({setfocus},)
called Action.setShortcuts with arg `['Ctrl+L']`
called CompareArtists.addAction
called Action.__init__ with args ('Find', {me})
called Signal.connect with args ({find_artist},)
called Action.setShortcuts with arg `['Ctrl+Return', 'Ctrl+F']`
called CompareArtists.addAction
called Action.__init__ with args ('Go', {me})
called Signal.connect with args ({select_and_go},)
called Action.setShortcuts with arg `['Ctrl+Shift+Return']`
called CompareArtists.addAction
called Action.__init__ with args ('Next', {me})
called Signal.connect with args ({focus_next},)
called Action.setShortcuts with arg `['Ctrl+N']`
called CompareArtists.addAction
called Action.__init__ with args ('Prev', {me})
called Signal.connect with args ({focus_prev},)
called Action.setShortcuts with arg `['Ctrl+P']`
called CompareArtists.addAction
called Action.__init__ with args ('Delete', {me})
called Signal.connect with args ({delete_artist},)
called Action.setShortcuts with arg `['Ctrl+D', 'Del']`
called CompareArtists.addAction
called Action.__init__ with args ('Save', {me})
called Signal.connect with args ({save_all},)
called Action.setShortcuts with arg `['Ctrl+S']`
called CompareArtists.addAction
"""
cmpart_refresh = """\
called set_modified with arg `False`
called read_artists
called Tree.clear
called Tree.addTopLevelItem
called Tree.addTopLevelItem
called Tree.clear
called Tree.addTopLevelItem
called Tree.addTopLevelItem
"""
cmpart_ref_1 = 'called focus_artist with arg `None`\n'
cmpart_ref_2 = 'called focus_artist with arg `artist`\n'
newart = """\
called Widget.__init__
called Dialog.setWindowTitle with arg `appname - add artist`
called Grid.__init__
called Label.__init__ with args ('First name:', {me})
called Grid.addWidget with arg MockLabel at (0, 0)
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `200`
called LineEdit.setMaximumWidth with arg `200`
called Grid.addWidget with arg MockLineEdit at (0, 1)
called Label.__init__ with args ('Last name:', {me})
called Grid.addWidget with arg MockLabel at (1, 0)
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `200`
called LineEdit.setMaximumWidth with arg `200`
called Grid.addWidget with arg MockLineEdit at (1, 1)
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Cancel', {me}) {{}}
called Signal.connect with args ({reject},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Update', {me}) {{}}
called Signal.connect with args ({update},)
called PushButton.setDefault with arg `True`
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, 2)
called Widget.setLayout with arg MockGridLayout
called LineEdit.setFocus
"""
cmpalb = """\
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Selecteer een uitvoerende:', {testobj})
called HBox.addWidget with arg MockLabel
called ComboBox.__init__
called Signal.connect with args ({testobj.get_albums},)
called HBox.addWidget with arg MockComboBox
called create_updownbuttons with args ({testobj},) {{'seltext': 'Select {{}} artist in list', 'icons': ('down_icon', 'up_icon'), 'callbacks': ({testobj.next_artist}, {testobj.prev_artist})}}
called HBox.addLayout with arg SimpleNamespace
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called VBox.__init__
called create_treewidget with args ({testobj}, ['Album Name in Clementine', 'Match'], (-1, 60))
called Tree.__init__
called VBox.addWidget with arg MockTreeWidget
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Help', {testobj}) {{}}
called Signal.connect with args ({testobj.help},)
called PushButton.__init__ with args ('&Check Album', {testobj}) {{}}
called Signal.connect with args ({testobj.find_album},)
called HBox.addWidget with arg MockPushButton
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.addLayout with arg MockVBoxLayout
called VBox.__init__
called create_treewidget with args ({testobj}, ['Album Name in Albums', 'Year', 'Id'], (-1, 60, 60))
called Tree.__init__
called VBox.addWidget with arg MockTreeWidget
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Save All', {testobj}) {{}}
called Signal.connect with args ({testobj.save_all},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.addLayout with arg MockVBoxLayout
called VBox.addLayout with arg MockHBoxLayout
called CompareAlbums.setLayout with arg MockVBoxLayout
"""
cmpalb_act = """\
called Tree.__init__
called Action.__init__ with args ('Help', {me})
called Signal.connect with args ({help},)
called Action.setShortcuts with arg `['F1', 'Ctrl+H']`
called CompareArtists.addAction
called Action.__init__ with args ('Select', {me})
called Signal.connect with args ({select},)
called Action.setShortcuts with arg `['Ctrl+Home']`
called CompareArtists.addAction
called Action.__init__ with args ('Focus', {me})
called Signal.connect with args ({focus},)
called Action.setShortcuts with arg `['Ctrl+L']`
called CompareArtists.addAction
called Action.__init__ with args ('Next', {me})
called Signal.connect with args ({next},)
called Action.setShortcuts with arg `['Ctrl+N']`
called CompareArtists.addAction
called Action.__init__ with args ('Prev', {me})
called Signal.connect with args ({prev},)
called Action.setShortcuts with arg `['Ctrl+P']`
called CompareArtists.addAction
called Action.__init__ with args ('Find', {me})
called Signal.connect with args ({find},)
called Action.setShortcuts with arg `['Ctrl+Return', 'Ctrl+F']`
called CompareArtists.addAction
called Action.__init__ with args ('Save', {me})
called Signal.connect with args ({save},)
called Action.setShortcuts with arg `['Ctrl+S']`
called CompareArtists.addAction
"""
newalb = """\
called Widget.__init__
called Dialog.setWindowTitle with arg `appname - add album`
called Grid.__init__
called Label.__init__ with args ('Album title:', {me})
called Grid.addWidget with arg MockLabel at (0, 0)
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `200`
called LineEdit.setMaximumWidth with arg `200`
called Grid.addWidget with arg MockLineEdit at (0, 1)
called Label.__init__ with args ('Release year:', {me})
called Grid.addWidget with arg MockLabel at (1, 0)
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `100`
called LineEdit.setMaximumWidth with arg `100`
called Grid.addWidget with arg MockLineEdit at (1, 1)
called HBox.__init__
called Widget.__init__
called HBox.addStretch
called HBox.addWidget with arg QCheckBox
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, 2)
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Cancel', {me}) {{}}
called Signal.connect with args ({reject},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Update', {me}) {{}}
called Signal.connect with args ({update},)
called PushButton.setDefault with arg `True`
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (3, 0, 1, 2)
called Widget.setLayout with arg MockGridLayout
called LineEdit.setFocus
"""
cmptrk = """\
called VBox.__init__
called HBox.__init__
called Grid.__init__
called Label.__init__ with args ('Selecteer een uitvoerende:', {testobj})
called Grid.addWidget with arg MockLabel at (0, 0)
called ComboBox.__init__
called Signal.connect with args ({testobj.get_albums},)
called HBox.addWidget with arg MockComboBox
called create_updownbuttons with args ({testobj},) {{'seltext': 'Select {{}} artist in list', 'icons': ('down_icon', 'up_icon'), 'callbacks': ({testobj.next_artist}, {testobj.prev_artist})}}
called HBox.addLayout with arg SimpleNamespace
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (0, 1)
called HBox.__init__
called Label.__init__ with args ('Selecteer een album:', {testobj})
called Grid.addWidget with arg MockLabel at (1, 0)
called ComboBox.__init__
called ComboBox.setMinimumWidth with arg `300`
called Signal.connect with args ({testobj.get_tracks},)
called HBox.addWidget with arg MockComboBox
called create_updownbuttons with args ({testobj},) {{'seltext': 'Select {{}} album in list', 'icons': ('down_icon', 'up_icon'), 'callbacks': ({testobj.next_album}, {testobj.prev_album})}}
called HBox.addLayout with arg SimpleNamespace
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (1, 1)
called VBox.addLayout with arg MockGridLayout
called HBox.__init__
called VBox.__init__
called create_treewidget with args ({testobj}, ['Track Name in Clementine'], ())
called Tree.__init__
called VBox.addWidget with arg MockTreeWidget
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Help', {testobj}) {{}}
called Signal.connect with args ({testobj.help},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Copy Tracks', {testobj}) {{}}
called Signal.connect with args ({testobj.copy_tracks},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.addLayout with arg MockVBoxLayout
called VBox.__init__
called create_treewidget with args ({testobj}, ['Track Name in Albums'], ())
called Tree.__init__
called VBox.addWidget with arg MockTreeWidget
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Unlink Album', {testobj}) {{}}
called Signal.connect with args ({testobj.unlink},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Save Unlinked', {testobj}) {{}}
called Signal.connect with args ({testobj.save_all},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.addLayout with arg MockVBoxLayout
called VBox.addLayout with arg MockHBoxLayout
called CompareAlbums.setLayout with arg MockVBoxLayout
"""
cmptrk_act = """\
called Action.__init__ with args ('Help', {me})
called Signal.connect with args ({help},)
called Action.setShortcuts with arg `['F1', 'Ctrl+H']`
called CompareArtists.addAction
called Action.__init__ with args ('Select_Artist', {me})
called Signal.connect with args ({selart},)
called Action.setShortcuts with arg `['Ctrl+Home']`
called CompareArtists.addAction
called Action.__init__ with args ('Select_Album', {me})
called Signal.connect with args ({selalb},)
called Action.setShortcuts with arg `['Ctrl+A']`
called CompareArtists.addAction
called Action.__init__ with args ('Next_Artist', {me})
called Signal.connect with args ({nextart},)
called Action.setShortcuts with arg `['Ctrl+N']`
called CompareArtists.addAction
called Action.__init__ with args ('Prev_Artist', {me})
called Signal.connect with args ({prevart},)
called Action.setShortcuts with arg `['Ctrl+P']`
called CompareArtists.addAction
called Action.__init__ with args ('Next_Album', {me})
called Signal.connect with args ({nextalb},)
called Action.setShortcuts with arg `['Ctrl+Shift+N']`
called CompareArtists.addAction
called Action.__init__ with args ('Prev_Album', {me})
called Signal.connect with args ({prevalb},)
called Action.setShortcuts with arg `['Ctrl+Shift+P']`
called CompareArtists.addAction
called Action.__init__ with args ('Copy', {me})
called Signal.connect with args ({copy},)
called Action.setShortcuts with arg `['Ctrl+C']`
called CompareArtists.addAction
called Action.__init__ with args ('Unlink', {me})
called Signal.connect with args ({unlink},)
called Action.setShortcuts with arg `['Ctrl+U']`
called CompareArtists.addAction
called Action.__init__ with args ('Save', {me})
called Signal.connect with args ({save},)
called Action.setShortcuts with arg `['Ctrl+S']`
called CompareArtists.addAction
"""
bgui_createstart = """\
called VBox.__init__
called Grid.__init__
called Label.__init__ with args ('Database: ', {testobj})
called Grid.addWidget with arg MockLabel at (0, 0)
called HBox.__init__
called ComboBox.__init__
called ComboBox.addItems with arg ['xxx', 'yyy']
called Signal.connect with args ({testobj.change_db},)
called HBox.addWidget with arg MockComboBox
called HBox.addStretch
called Grid.addLayout with arg MockHBoxLayout at (0, 1)
called Label.__init__ with args ('Artist: ', {testobj})
called Grid.addWidget with arg MockLabel at (1, 0)
called ComboBox.__init__
called ComboBox.setMinimumWidth with arg `260`
called Signal.connect with args ({testobj.get_artist},)
called Grid.addWidget with arg MockComboBox at (1, 1)
called Label.__init__ with args ('Album: ', {testobj})
called Grid.addWidget with arg MockLabel at (2, 0)
called ComboBox.__init__
called ComboBox.setMinimumWidth with arg `260`
called Signal.connect with args ({testobj.get_album},)
called Grid.addWidget with arg MockComboBox at (2, 1)
called VBox.addLayout with arg MockGridLayout
called HBox.__init__
called HBox.addStretch
called List.__init__
called List.setMinimumWidth with arg `400`
called List.setMinimumHeight with arg `300`
called HBox.addWidget with arg MockListBox
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addStretch
called Label.__init__ with args ({testobj},)
called Label.setMinimumWidth with arg `500`
called Label.setMinimumHeight with arg `500`
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('E&xit', {testobj}) {{}}
called Signal.connect with args ({testobj.exit},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Widget.setLayout
called ComboBox.count
"""
bgui_createmiddle = """\
called ComboBox.itemText with value `0`
called ComboBox.itemText with value `1`
called ComboBox.itemText with value `2`
called ComboBox.setCurrentIndex with arg `2`
"""
bgui_createend = """\
called ComboBox.setFocus
"""

@pytest.fixture
def expected_output():
    """fixture returning output predictions per function
    """
    return {'start': start_all,
            'select_1': (select_top + select_other_artist_button + select_other_type_button
                         + select_start_data + select_data_line_1 + select_data_line_2
                         + select_end_data),
            'select_2': (select_top + select_other_search_button + select_other_type_button
                         + select_start_data + select_data_line_1 + select_end_data),
            'select_3': (select_top + select_other_search_button + select_start_data
                         + select_end_data),
            'detail': detail_all,
            'editdetails_studio': editdetails_studio,
            'editdetails_live': editdetails_live,
            'editdetails_studio_nw': editdetails_studio_nw,
            'editdetails_live_nw': editdetails_live_nw,
            'edittracks': (edittracks_all_start + edittracks_all_end_1
                           + edittracks_all_buttonstrip_1 + edittracks_all_end_2),
            'edittracks_2': (edittracks_all_start + edittracks_all_end_1
                             + edittracks_all_buttonstrip_2 + edittracks_all_end_2),
            'edittracks_3': (edittracks_all_start + edittracks_all_middle + edittracks_all_end_1
                             + edittracks_all_buttonstrip_3 + edittracks_all_end_2),
            'edittracks_line': track_fields,
            'editrecs': (editrecs_all_start + editrecs_all_end_1 + editrecs_all_buttonstrip_1
                         + editrecs_all_end_2),
            'editrecs_2': (editrecs_all_start + editrecs_all_end_1 + editrecs_all_buttonstrip_2
                           + editrecs_all_end_2),
            'editrecs_3': (editrecs_all_start + editrecs_all_middle + editrecs_all_end_1
                           + editrecs_all_buttonstrip_3 + editrecs_all_end_2),
            'editrecs_line': rec_fields_start + rec_fields_end,
            'editrecs_line_2': rec_fields_start + rec_fields_middle + rec_fields_end,
            'artists': artists_all_start + artists_all_middle + artists_all_end,
            'artists_2': artists_all_start + artists_all_end,
            'artist_line': artists_line,
            'artist_dialog': artist_dialog,
            'matcher_main': matcher_noapp + matcher,
            'matcher_main_w_app': matcher,
            'compare_artists': cmpart,
            'compare_artists_actions': cmpart_act,
            'compare_artists_refresh_1': cmpart_refresh + cmpart_ref_1,
            'compare_artists_refresh_2': cmpart_refresh + cmpart_ref_2,
            'new_artist': newart,
            'compare_albums': cmpalb,
            'compare_albums_actions': cmpalb_act,
            'new_album': newalb,
            'compare_tracks': cmptrk,
            'compare_tracks_actions': cmptrk_act,
            'bgui_create_widgets': bgui_createstart + bgui_createmiddle + bgui_createend,
            'bgui_create_widgets2': bgui_createstart + bgui_createend}
