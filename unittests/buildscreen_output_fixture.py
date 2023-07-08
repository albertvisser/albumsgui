import pytest


@pytest.fixture
def expected_output():
    return {
        'start': """\
called GridLayout.__init__
called newline with arg of type <class 'apps.albums_gui.Start'>
called GridLayout.addLayout with arg of type <class 'type'> at (0, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (1, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (2, 0)
called ComboBox.__init__
called ComboBox.addItems with arg `['Niet zoeken, alles tonen', 'Zoek op Uitvoerende: ', 'Zoek op Tekst in Titel', 'Zoek op Tekst in Producer', 'Zoek op Tekst in Credits', 'Zoek op Tekst in Bezetting']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (2, 1)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (3, 1)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (4, 1)
called Label.__init__
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
called GridLayout.addLayout with arg of type <class 'type'> at (7, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (8, 0, 1, 3)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (9, 0)
called ComboBox.__init__
called ComboBox.addItems with arg `['Niet zoeken, alles tonen', 'Zoek op Uitvoerende: ', 'Zoek op Tekst in Locatie', 'Zoek op Tekst in Datum', 'Zoek op Tekst in Bezetting']`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called GridLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'> at (9, 1)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg `--- Maak een selectie ---`
called ComboBox.setMaximumWidth to `200`
called ComboBox.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockComboBox'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (10, 1)
called HBoxLayout.__init__
called Label.__init__
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called LineEdit.setMaximumWidth to `200`
called LineEdit.setMinimumWidth to `200`
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockLineEdit'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (11, 1)
called Label.__init__
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
called Label.__init__
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
called GridLayout.addLayout with arg of type <class 'type'> at (17, 0, 1, 3)
called PushButton.__init__ with args ('&Import Data', {me})
called connect with args ({start_imp},)
called HBoxLayout.__init__
called HBoxLayout.addStretch
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called PushButton.__init__ with args ('E&xit', {me})
called connect with args ({exit},)
called HBoxLayout.addWidget with arg of type <class 'unittests.mockqtwidgets.MockButton'>
called HBoxLayout.addStretch
called GridLayout.addLayout with arg of type <class 'unittests.mockqtwidgets.MockHBox'> at (18, 0, 1, 3)
called QWidget.setLayout with arg of type <class 'unittests.mockqtwidgets.MockGrid'>
""",
        'select': """\
""",
        'detail': """\
""",
        'artists': """\
"""}
