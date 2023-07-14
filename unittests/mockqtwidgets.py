import types

class MockApplication:  # (qtw.QApplication):
    def __init__(self, *args):
        print('called QApplication.__init__')
    def exec_(self):
        print('called QApplication.exec_')


class MockControl:
    def setVisible(self, value):
        print(f'called control.setVisible with args `{type(self)}`, `{value}`')


class MockWidget: # (qtw.QWidget):
    def __init__(self, *args):
        print('called widget.__init__')
        self.tracks_list = MockControl()
        self.lbl = MockControl()
    def create_widgets(self):
        print('called widget.create_widgets, self.initializing is', self.initializing)
    def show(self):
        print('called widget.show')


class MockMainWindow:
    def __init__(self):
        print('called QMainWindow.__init__')
    def move(self, *args):
        print('called QMainWindow.move with args', args)
    def show(self):
        print('called QMainWindow.show')


class MockVBox:
    def __init__(self):
        print('called VBoxLayout.__init__')
    def addWidget(self, *args):
        print(f'called VBoxLayout.addWidget with arg of type {type(args[0])}')
    def addLayout(self, *args):
        print(f'called VBoxLayout.addLayout with arg of type {type(args[0])}')


class MockHBox:
    def __init__(self):
        print('called HBoxLayout.__init__')
    def addWidget(self, *args):
        print(f'called HBoxLayout.addWidget with arg of type {type(args[0])}')
    def addLayout(self, *args):
        print(f'called HBoxLayout.addLayout with arg of type {type(args[0])}')
    def addStretch(self, *args):
        print('called HBoxLayout.addStretch')
    def addSpacing(self, *args):
        print('called HBoxLayout.addSpacing')


class MockGrid:
    def __init__(self):
        print('called GridLayout.__init__')
    def addWidget(self, *args):
        print(f'called GridLayout.addWidget with arg of type {type(args[0])} at {args[1:]}')
    def addLayout(self, *args):
        print(f'called GridLayout.addLayout with arg of type {type(args[0])} at {args[1:]}')


class MockFrame:
    HLine = '---'
    def __init__(self, parent):
        print('called Frame.__init__')
    def setFrameShape(self, arg):
        print(f'called Frame.setFrameShape with arg `{arg}`')
    def setLayout(self, arg):
        print(f'called Frame.setLayout with arg of type `{type(arg)}`')


class MockComboBox:
    def mock_connect(*args):
        print('called connect with args', args)
    currentIndexChanged = types.SimpleNamespace(connect=mock_connect)
    def __init__(self, *args):
        print('called ComboBox.__init__')
    def setMaximumWidth(self, number):
        print(f'called ComboBox.setMaximumWidth to `{number}`')
    def setMinimumWidth(self, number):
        print(f'called ComboBox.setMinimumWidth to `{number}`')
    def setCurrentIndex(self, number):
        print(f'called ComboBox.setCurrentIndex to `{number}`')
    def setCurrentText(self, text):
        print(f'called ComboBox.setCurrentText to `{text}`')
    def currentIndex(self):
        print('called ComboBox.currentIndex')
        return 1
    def currentText(self):
        print('called ComboBox.currentText')
        return '.'
    def setFocus(self):
        print('called ComboBox.setFocus')
    def clear(self):
        print('called ComboBox.clear')
    def addItem(self, item):
        print(f'called ComboBox.addItems with arg `{item}`')
    def addItems(self, itemlist):
        print(f'called ComboBox.addItems with arg `{itemlist}`')
    def itemText(self, number):
        print(f'ComboBox.itemText for `{number}`')


class MockLineEdit:
    def __init__(self, *args):
        print('called LineEdit.__init__')
    def setMaximumWidth(self, number):
        print(f'called LineEdit.setMaximumWidth to `{number}`')
    def setMinimumWidth(self, number):
        print(f'called LineEdit.setMinimumWidth to `{number}`')
    def setText(self, text):
        print(f'called LineEdit.setText with arg `{text}`')
    def clear(self):
        print('called LineEdit.clear')
    def text(self):
        print('called LineEdit.text')
        return '..'


class MockListBox:
    def __init__(self, *args):
        print('called ListWidget.__init__')
    def setVisible(self, value):
        print(f'called ListWidget.setVisible to `{value}`')
    def setMinimumWidth(self, number):
        print(f'called ListWidget.setMinimumWidth to `{number}`')
    def setMinimumHeight(self, number):
        print(f'called ListWidget.setMinimumHeight to `{number}`')
    def clear(self):
        print('called ListWidget.clear')
    def addItems(self, itemlist):
        print(f'called ListWidget.addItems with arg `{itemlist}`')


class MockLabel:
    def __init__(self, *args):
        print('called Label.__init__')
    def setVisible(self, value):
        print(f'called Label.setVisible to `{value}`')
    def setMinimumWidth(self, number):
        print(f'called Label.setMinimumWidth to `{number}`')
    def setMinimumHeight(self, number):
        print(f'called Label.setMinimumHeight to `{number}`')
    def setText(self, text):
        print(f'called Label.setText with arg `{text}`')
    def setPixmap(self, data):
        print(f'called Label.setPixmap')


class MockButton:
    def mock_connect(*args):
        print('called connect with args', args)
    clicked = types.SimpleNamespace(connect=mock_connect)
    def __init__(self, *args):
        print('called PushButton.__init__ with args', args)
    def setMaximumWidth(self, number):
        print(f'called PushButton.setMaximumWidth to `{number}`')


class MockPixmap:
    def __init__(self, *args):
        print('called Pixmap.__init__')
    def load(self, fname):
        print(f'called Pixmap.load for `fname`')
        return 'ok'
    def scaled(self, x, y):
        print(f'called Pixmap.scaled to `{x}`, `{y}`')
        return 'ok'


class MockMessageBox:
    def information(parent, caption, message):
        print(f'called QMessageBox.information with args `{caption}` `{message}`')


class MockScrollArea:
    def setWidget(self, arg):
        print(f'called ScrollArea.setWidget with arg of type `{type(arg)}`')
