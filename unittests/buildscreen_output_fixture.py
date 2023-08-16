import pytest

start_all = """\
called GridLayout.__init__
called newline with arg of type <class 'apps.albums_gui.Start'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (0, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Studio Albums', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Selecteer:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (2, 0)
called ComboBox.__init__
called ComboBox.addItems with arg `['Niet zoeken, alles tonen', 'Zoek op Uitvoerende: ', 'Zoek op Tekst in Titel', 'Zoek op Tekst in Producer', 'Zoek op Tekst in Credits', 'Zoek op Tekst in Bezetting']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (2, 1)
called HBoxLayout.__init__
called Label.__init__ with args ('Kies Uitvoerende:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 1)
called HBoxLayout.__init__
called Label.__init__ with args ('Zoektekst voor 3-6:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (4, 1)
called Label.__init__ with args ('Sorteer op:', {me})
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (5, 0)
called ComboBox.__init__
called ComboBox.addItems with arg `['Niet sorteren', 'Uitvoerende', 'Titel', 'Jaar']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (5, 1)
called HBoxLayout.__init__
called PushButton.__init__ with args ('Selectie uitvoeren', {me})
called PushButton.__init__ with args ('Nieuw album opvoeren', {me})
called connect with args ({select_album},)
called connect with args ({new_album},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (6, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.Start'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (7, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Live Concerten', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (8, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Selecteer:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (9, 0)
called ComboBox.__init__
called ComboBox.addItems with arg `['Niet zoeken, alles tonen', 'Zoek op Uitvoerende: ', 'Zoek op Tekst in Locatie', 'Zoek op Tekst in Datum', 'Zoek op Tekst in Bezetting']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (9, 1)
called HBoxLayout.__init__
called Label.__init__ with args ('Kies Uitvoerende:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (10, 1)
called HBoxLayout.__init__
called Label.__init__ with args ('Zoektekst voor 3-5:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (11, 1)
called Label.__init__ with args ('Sorteer op:', {me})
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (12, 0)
called ComboBox.__init__
called ComboBox.addItems with arg `['Niet sorteren', 'Uitvoerende', 'Locatie', 'Datum']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (12, 1)
called HBoxLayout.__init__
called PushButton.__init__ with args ('Selectie uitvoeren', {me})
called PushButton.__init__ with args ('Nieuw album opvoeren', {me})
called connect with args ({select_concert},)
called connect with args ({new_concert},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (13, 0, 1, 3)
called HBoxLayout.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockFrame'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (14, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Uitvoerende Artiesten', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (15, 0, 1, 3)
called HBoxLayout.__init__
called PushButton.__init__ with args ('Lijst tonen/wijzigen', {me})
called PushButton.__init__ with args ('Nieuwe opvoeren', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called connect with args ({view_artists},)
called connect with args ({new_artist},)
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (16, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.Start'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (17, 0, 1, 3)
called PushButton.__init__ with args ('&Import Data', {me})
called connect with args ({start_imp},)
called exitbutton with args {me}, {exit}, <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (18, 0, 1, 3)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
"""
select_top = """\
called VBoxLayout.__init__
called newline with arg of type <class 'apps.albums_gui.Select'>
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Label.__init__ with args ('', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
select_other_artist_button = """\
called HBoxLayout.__init__
called Label.__init__ with args ('Snel naar dezelfde selectie voor een andere artiest:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg `['X', 'Y']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'>
called PushButton.__init__ with args ('Go', {me})
called PushButton.setMaximumWidth to `40`
called connect with args ({other_artist},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
select_other_type_button = """\
called HBoxLayout.__init__
called Label.__init__ with args ('of naar een soortgelijke selectie voor ', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called PushButton.__init__ with args ('', {me})
called connect with args ({other_albumtype},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
select_other_search_button = """\
called HBoxLayout.__init__
called Label.__init__ with args ('Snel naar dezelfde selectie voor een andere waarde:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called PushButton.__init__ with args ('Go', {me})
called PushButton.setMaximumWidth to `40`
called connect with args ({other_search},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
select_start_data = """\
called newline with arg of type <class 'apps.albums_gui.Select'>
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Label.__init__ with args ('Kies een item uit de lijst:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Frame.__init__
called VBoxLayout.__init__
"""
select_data_line_1 = """\
called HBoxLayout.__init__
called Label.__init__ with args ('1', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.addStretch
called PushButton.__init__ with args ('Go', {me})
called PushButton.setMaximumWidth to `40`
called connect with args ({todetail},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addSpacing
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
select_data_line_2 = """\
called HBoxLayout.__init__
called Label.__init__ with args ('2', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.addStretch
called PushButton.__init__ with args ('Go', {me})
called PushButton.setMaximumWidth to `40`
called connect with args ({todetail},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addSpacing
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
select_end_data = """\
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockVBox'>`
called ScrollArea.setWidget with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockScrollArea'>
called HBoxLayout.__init__
called Label.__init__ with args ('Of', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called PushButton.__init__ with args ('voer een nieuw item op bij deze selectie', {me})
called connect with args ({add_new_to_sel},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called newline with arg of type <class 'apps.albums_gui.Select'>
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called button_strip with args ({me}, 'Start')
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
"""
detail_all = """\
called GridLayout.__init__
called Label.__init__ with args ('', {me})
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (0, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.Detail'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Snel naar een ander item in deze selectie:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg `--- selecteer titel ---`
called ComboBox.addItems with arg `['xxx', 'yyy']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'>
called PushButton.__init__ with args ('Go', {me})
called PushButton.setMaximumWidth to `40`
called connect with args ({other_album},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (2, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.Detail'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Detailgegevens:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called PushButton.__init__ with args ('wijzigen', {me})
called connect with args ({edit_alg},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (4, 0, 1, 3)
called Frame.__init__
called GridLayout.__init__
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('x', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (0, 0, 1, 1)
called Label.__init__ with args ('y', {me})
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (0, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('a', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 1)
called Label.__init__ with args ('b', {me})
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (1, 1, 1, 2)
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockGrid'>`
called ScrollArea.setWidget with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockScrollArea'> at (5, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.Detail'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (6, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Tracks:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called PushButton.__init__ with args ('wijzigen', {me})
called connect with args ({edit_trk},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (7, 0, 1, 3)
called Frame.__init__
called VBoxLayout.__init__
called HBoxLayout.__init__
called Label.__init__ with args ('       1.', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called Label.__init__ with args ('a (b)', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Label.__init__ with args ('c', {me})
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.__init__
called Label.__init__ with args ('       2.', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called Label.__init__ with args ('x (y)', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockVBox'>`
called ScrollArea.setWidget with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockScrollArea'> at (8, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.Detail'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (9, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__ with args ('Opnames:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called PushButton.__init__ with args ('wijzigen', {me})
called connect with args ({edit_rec},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (10, 0, 1, 3)
called Frame.__init__
called VBoxLayout.__init__
called HBoxLayout.__init__
called Label.__init__ with args ('       1.', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called Label.__init__ with args ('p q', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Label.__init__ with args ('       2.', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called Label.__init__ with args ('r', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockVBox'>`
called ScrollArea.setWidget with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockScrollArea'> at (11, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.Detail'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (12, 0, 1, 3)
called button_strip with args ({me}, 'Select', 'Start')
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (13, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (14, 0, 1, 3)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
"""
editdetails_studio = """\
called GridLayout.__init__
called Label.__init__ with args ('', {me})
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (0, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.EditDetails'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 3)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg `['xxx', 'bbb']`
called ComboBox.setCurrentIndex to `1`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (2, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Albumtitel:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 0, 1, 1)
called LineEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'> at (3, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Label/jaar:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (4, 0, 1, 1)
called HBoxLayout.__init__
called LineEdit.__init__
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called LineEdit.__init__
called LineEdit.setMaximumWidth to `80`
called LineEdit.setMinimumWidth to `80`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (4, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Credits:', {me})
called VBoxLayout.__init__
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called VBoxLayout.addStretch
called HBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (5, 0, 1, 1)
called TextEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockTextEdit'> at (5, 1, 1, 2)
called VBoxLayout.__init__
called VBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'> at (6, 0, 1, 3)
called button_strip with args ({me}, 'Cancel', 'Go', 'GoBack', 'Select', 'Start')
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (7, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (8, 0, 1, 3)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
"""
editdetails_live = """\
called GridLayout.__init__
called Label.__init__ with args ('', {me})
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (0, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.EditDetails'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 3)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg `['xxx', 'bbb']`
called ComboBox.setCurrentIndex to `1`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (2, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Locatie/datum:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 0, 1, 1)
called LineEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'> at (3, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Bezetting:', {me})
called VBoxLayout.__init__
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called VBoxLayout.addStretch
called HBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (4, 0, 1, 1)
called TextEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockTextEdit'> at (4, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Tevens met:', {me})
called VBoxLayout.__init__
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called VBoxLayout.addStretch
called HBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (5, 0, 1, 1)
called TextEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockTextEdit'> at (5, 1, 1, 2)
called VBoxLayout.__init__
called VBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'> at (6, 0, 1, 3)
called button_strip with args ({me}, 'Cancel', 'Go', 'GoBack', 'Select', 'Start')
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (7, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (8, 0, 1, 3)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
"""
editdetails_studio_nw = """\
called GridLayout.__init__
called Label.__init__ with args ('', {me})
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (0, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.EditDetails'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 3)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg `['xxx', 'bbb']`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (2, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Albumtitel:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 0, 1, 1)
called LineEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'> at (3, 1, 1, 2)
called VBoxLayout.__init__
called VBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'> at (4, 0, 1, 3)
called button_strip with args ({me}, 'Go', 'GoBack', 'Start')
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (5, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (6, 0, 1, 3)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
"""
editdetails_live_nw = """\
called GridLayout.__init__
called Label.__init__ with args ('', {me})
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (0, 0, 1, 3)
called newline with arg of type <class 'apps.albums_gui.EditDetails'>
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 3)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Uitvoerende:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (2, 0, 1, 1)
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg `['xxx', 'bbb']`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (2, 1, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addSpacing
called Label.__init__ with args ('Locatie/datum:', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 0, 1, 1)
called LineEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'> at (3, 1, 1, 2)
called VBoxLayout.__init__
called VBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'> at (4, 0, 1, 3)
called button_strip with args ({me}, 'Go', 'GoBack', 'Select', 'Start')
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (5, 0, 1, 3)
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (6, 0, 1, 3)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
"""
edittracks_all_start = """\
called VBoxLayout.__init__
called Label.__init__ with args ('tracks', {me})
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockFrame'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Frame.__init__
called VBoxLayout.__init__
called GridLayout.__init__
called HBoxLayout.__init__
called Label.__init__ with args ('Title\\nCredits', {me})
called Label.setMinimumWidth to `304`
called Label.setMaximumWidth to `304`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called Label.__init__ with args ('Author\\n', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 1)
"""
edittracks_all_middle = """\
called EditTracks.add_track_fields with args (1, 'x')
called EditTracks.add_track_fields with args (2, 'a', 'c')
"""
track_fields = """\
called Label.__init__ with args ('       {num}.', {me})
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (1, 0)
called HBoxLayout.__init__
called LineEdit.__init__ with args ('{text1}', {me})
called LineEdit.setMaximumWidth to `300`
called LineEdit.setMinimumWidth to `300`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called LineEdit.__init__ with args ('{text2}', {me})
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 1)
called TextEdit.__init__ with args ('{text3}', {me})
called TextEdit.setMaximumWidth to `508`
called TextEdit.setMinimumWidth to `508`
called TextEdit.setMaximumHeight to `38`
called TextEdit.setMinimumHeight to `38`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockTextEdit'> at (2, 1)
"""
edittracks_all_end_1 = """\
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
called VBoxLayout.addStretch
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockVBox'>`
called ScrollArea.setWidget with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called ScrollArea.setWidgetResizable with arg `True`
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockScrollArea'>
called HBoxLayout.__init__
called PushButton.__init__ with args ('Nieuw track', {me})
called connect with args ({add_new_item},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockFrame'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
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
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
"""
editrecs_all_start = """\
called VBoxLayout.__init__
called Label.__init__ with args ('opnames', {me})
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockFrame'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Frame.__init__
called VBoxLayout.__init__
called VBoxLayout.addStretch
"""
editrecs_all_middle = """\
called EditRecordings.add_track_fields with args (0, (1, ('x', 'y')))
called EditRecordings.add_track_fields with args (1, (2, ('a', 'b')))
"""
rec_fields_start = """\
called HBoxLayout.__init__
called Label.__init__ with args ('       {num}.', {me})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.addItems with arg `('x', 'y', 'z')`
"""
rec_fields_middle = """called ComboBox.setCurrentIndex to `1`
"""
rec_fields_end = """\
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'>
called LineEdit.__init__ with args ('{text}', {me})
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called HBoxLayout.addStretch
called VBoxLayout.insertLayout with arg1 {insertpos} and arg2 of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
editrecs_all_end_1 = """\
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockVBox'>`
called ScrollArea.setWidget with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called ScrollArea.setWidgetResizable with arg `True`
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockScrollArea'>
called HBoxLayout.__init__
called PushButton.__init__ with args ('Nieuwe opname', {me})
called connect with args ({add_new_item},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockFrame'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
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
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called exitbutton with args ({me}, {exit}) {{}}
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
"""
artists_all_start = """\
called VBoxLayout.__init__
called HBoxLayout.__init__
called Label.__init__ with args ('Artiestenlijst - gefilterd op', {testobj})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called PushButton.__init__ with args ('&Go', {testobj})
called connect with args ({filter},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called Frame.__init__
called Frame.setFrameShape with arg `---`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockFrame'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Frame.__init__
called VBoxLayout.__init__
"""
artists_all_middle = """\
called Artists.add_artist_line with args (1, 'a', 'b')
called Artists.add_artist_line with args (3, 'b', 'a')
called Artists.add_artist_line with args (2, 'x', 'y')
"""
artists_all_end = """\
called VBoxLayout.addStretch
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockVBox'>`
called ScrollArea.setWidget with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called ScrollArea.setWidgetResizable with arg `True`
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockScrollArea'>
called button_strip with args ({testobj}, 'Edit', 'New', 'Start')
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called exitbutton with args ({testobj}, {exit}) {{}}
called HBoxLayout.__init__
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
"""
artists_line = """\
called HBoxLayout.__init__
called Label.__init__ with args ('  {num}.', {testobj})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called LineEdit.__init__ with args ('{text1}', {testobj})
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called LineEdit.__init__ with args ('{text2}', {testobj})
called LineEdit.setMaximumWidth to `300`
called LineEdit.setMinimumWidth to `300`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
artist_dialog = """\
called QWidget.__init__
called QWidget.__init__
called GridLayout.__init__
called Label.__init__ with args ('First name:', {testobj})
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (0, 0)
called LineEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'> at (0, 1)
called Label.__init__ with args ('Last name:', {testobj})
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (1, 0)
called LineEdit.__init__
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'> at (1, 1)
called Label.__init__ with args ('Names wil be shown sorted on last name',)
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'> at (2, 0, 1, 2)
called HBoxLayout.__init__
called HBoxLayout.addStretch
called PushButton.__init__ with args ('Cancel', {testobj})
called connect with args ({reject},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called PushButton.__init__ with args ('Update', {testobj})
called connect with args ({update},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 0, 1, 2)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
"""
matcher_noapp = "called QApplication._init__\n"
matcher = """\
called Icon.__init__
called Icon.__init__
called Icon.__init__
called Icon.__init__
called QMainWindow._init__ with args ()
called QMainWindow.setWindowTitle to `AlbumsMatcher`
called QMainWindow.move with args (300, 50)
called QMainWindow.resize with args (600, 650)
called QTabWidget.__init__
called connect with args ({page_changed},)
called Frame.__init__
called VBoxLayout.__init__
called HBoxLayout.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockTabWidget'>
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.__init__
called HBoxLayout.addStretch
called PushButton.__init__ with args ('E&xit', {parent})
called connect with args ({exit},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called Frame.setLayout with arg of type `<class 'unittests.mockqtwidgets.MockVBox'>`
called QMainWidget.setCentralWindow with arg of type `<class 'unittests.mockqtwidgets.MockFrame'>`
called QAction.__init__ with args ('Exit', {me})
called connect with args ({exit},)
called QAction.setShortcut with arg `Ctrl+Q`
called QMainWindow.addAction
called MainFrame.check_for_data
called MainFrame.settabs
called QTabWidget.setCurrentIndex with arg `0`
called QMainWindow.show
called MainFrame.go with arg `{app}`
"""
cmpart = """\
called QTreeWidget.__init__
called QTreeWidget.setColumnCount with arg `2`
called QTreeWidget.header
called QHeaderView.__init__
called QHeaderView.setStretchLastSection with arg False
called QHeaderView.setSectionResixeMode for col 0 mode stretch
called QTreeWidget.setColumnWidth with args 1, 50
called QTreeWidget.setHeaderLabels with arg `['Artist', 'Match']`
called QTreeWidget.setMouseTracking with arg `True`
called connect with args ({popuptext},)
called connect with args ({select_and_go},)
called QTreeWidget.__init__
called QTreeWidget.setColumnCount with arg `3`
called QTreeWidget.header
called QHeaderView.__init__
called QHeaderView.setStretchLastSection with arg False
called QTreeWidget.setColumnWidth with args 0, 80
called QTreeWidget.setColumnWidth with args 2, 50
called QHeaderView.setSectionResixeMode for col 1 mode stretch
called QTreeWidget.setHeaderLabels with arg `['First Name', 'Last Name', 'Id']`
called QTreeWidget.setMouseTracking with arg `True`
called connect with args ({popuptext},)
called connect with args ({check_deletable},)
called PushButton.__init__ with args ('&Help', {me})
called connect with args ({help},)
called PushButton.__init__ with args ({me},)
called PushButton.setIcon with arg `next_icon`
called Size.__init__ with args (12, 12)
called PushButton.setIconSize with arg of type <class 'unittests.mockqtwidgets.MockSize'>
called PushButton.setToolTip with arg `Go to next unmatched artist`
called connect with args ({focus_next},)
called PushButton.__init__ with args ({me},)
called PushButton.setIcon with arg `prev_icon`
called Size.__init__ with args (12, 12)
called PushButton.setIconSize with arg of type <class 'unittests.mockqtwidgets.MockSize'>
called PushButton.setToolTip with arg `Go to previous unmatched artist`
called connect with args ({focus_prev},)
called PushButton.__init__ with args ('&Check Artist', {me})
called connect with args ({find_artist},)
called PushButton.__init__ with args ('&Delete', {me})
called connect with args ({delete_artist},)
called PushButton.setEnabled with arg `False`
called PushButton.__init__ with args ('&Save All', {me})
called connect with args ({save_all},)
called HBoxLayout.__init__
called VBoxLayout.__init__
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockTree'>
called HBoxLayout.__init__
called HBoxLayout.addStretch
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
called VBoxLayout.__init__
called VBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockTree'>
called HBoxLayout.__init__
called HBoxLayout.addStretch
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called VBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
called HBoxLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockVBox'>
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'>
"""
cmpalb = """\
"""
cmptrk = """\
"""

@pytest.fixture
def expected_output():
    return {
        'start': start_all,
        'select_1': (select_top + select_other_artist_button + select_other_type_button +
                     select_start_data + select_data_line_1 + select_data_line_2 + select_end_data),
        'select_2': (select_top + select_other_search_button + select_other_type_button +
                     select_start_data + select_data_line_1 + select_end_data),
        'select_3': select_top + select_other_search_button + select_start_data + select_end_data,
        'detail': detail_all,
        'editdetails_studio': editdetails_studio,
        'editdetails_live': editdetails_live,
        'editdetails_studio_nw': editdetails_studio_nw,
        'editdetails_live_nw': editdetails_live_nw,
        'edittracks': (edittracks_all_start + edittracks_all_end_1 + edittracks_all_buttonstrip_1 +
                       edittracks_all_end_2),
        'edittracks_2': (edittracks_all_start + edittracks_all_end_1 + edittracks_all_buttonstrip_2 +
                         edittracks_all_end_2),
        'edittracks_3': (edittracks_all_start + edittracks_all_middle + edittracks_all_end_1 +
                         edittracks_all_buttonstrip_3 + edittracks_all_end_2),
        'edittracks_line': track_fields,
        'editrecs': (editrecs_all_start + editrecs_all_end_1 + editrecs_all_buttonstrip_1 +
                       editrecs_all_end_2),
        'editrecs_2': (editrecs_all_start + editrecs_all_end_1 + editrecs_all_buttonstrip_2 +
                         editrecs_all_end_2),
        'editrecs_3': (editrecs_all_start + editrecs_all_middle + editrecs_all_end_1 +
                         editrecs_all_buttonstrip_3 + editrecs_all_end_2),
        'editrecs_line': rec_fields_start + rec_fields_end,
        'editrecs_line_2': rec_fields_start + rec_fields_middle + rec_fields_end,
        'artists': artists_all_start + artists_all_middle + artists_all_end,
        'artists_2': artists_all_start + artists_all_end,
        'artist_line': artists_line,
        'artist_dialog': artist_dialog,
        'matcher_main': matcher_noapp + matcher,
        'matcher_main_w_app': matcher,
        'compare_artists': cmpart,
        'compare_albums': cmpalb,
        'compare_tracks': cmptrk,
        }
