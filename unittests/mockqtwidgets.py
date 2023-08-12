import types

class MockApplication:  # (qtw.QApplication):
    def __init__(self, *args):
        print('called QApplication.__init__')
    def exec_(self):
        print('called QApplication.exec_')
    def changeOverrideCursor(self, arg):
        print(f'called changeOverrideCursor with arg of type {type(arg)}')
    def restoreOverrideCursor(self):
        print('called app.restoreOverrideCursor')

class MockCursor:
    def __init__(self, arg):
        print(f'called QCursor with arg {arg}')

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


class MockScrollBar:
    def __init__(self, *args):
        print('called scrollbar.__init__')
    def maximum(self):
        print('called scrollbar.maximum')
        return 99
    def setMaximum(self, value):
        print(f'called scrollbar.setMaximum with value `{value}`')
    def setValue(self, value):
        print(f'called scrollbar.setValue with value `{value}`')


class MockScrolledWidget:
    def __init__(self, *args):
        print('called scrolledwidget.__init__')
    def verticalScrollBar(self):
        print('called scrolledwidget.verticalScrollBar')
        return MockScrollBar()


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
        self._count = 0
    def addWidget(self, *args):
        print(f'called VBoxLayout.addWidget with arg of type {type(args[0])}')
        self._count += 1
    def addLayout(self, *args):
        print(f'called VBoxLayout.addLayout with arg of type {type(args[0])}')
        self._count += 1
    def insertLayout(self, *args):
        print(f'called VBoxLayout.insertLayout with arg1 {args[0]} and arg2 of type {type(args[1])}')
        self._count += 1
    def addStretch(self, *args):
        print('called VBoxLayout.addStretch')
    def count(self):
        return self._count


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
    def count(self):
        pass
    def itemAt(self, num):
        pass


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
        self._index = 1
    def setMaximumWidth(self, number):
        print(f'called ComboBox.setMaximumWidth to `{number}`')
    def setMinimumWidth(self, number):
        print(f'called ComboBox.setMinimumWidth to `{number}`')
    def setCurrentIndex(self, number):
        print(f'called ComboBox.setCurrentIndex to `{number}`')
        self._index = number
    def setCurrentText(self, text):
        print(f'called ComboBox.setCurrentText to `{text}`')
    def currentIndex(self):
        print('called ComboBox.currentIndex')
        return self._index
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
        self._text = args[0] if args else '..'
    def setMaximumWidth(self, number):
        print(f'called LineEdit.setMaximumWidth to `{number}`')
    def setMinimumWidth(self, number):
        print(f'called LineEdit.setMinimumWidth to `{number}`')
    def setText(self, text):
        print(f'called LineEdit.setText with arg `{text}`')
        self._text = text
    def clear(self):
        print('called LineEdit.clear')
    def text(self):
        print('called LineEdit.text')
        return self._text


class MockTextEdit:
    def __init__(self, *args):
        print('called TextEdit.__init__')
        self._text = args[0] if args else '..'
    def setMaximumWidth(self, number):
        print(f'called TextEdit.setMaximumWidth to `{number}`')
    def setMaximumHeight(self, number):
        print(f'called TextEdit.setMaximumHeight to `{number}`')
    def setMinimumWidth(self, number):
        print(f'called TextEdit.setMinimumWidth to `{number}`')
    def setMinimumHeight(self, number):
        print(f'called TextEdit.setMinimumHeight to `{number}`')
    def setText(self, text):
        print(f'called TextEdit.setText with arg `{text}`')
    def clear(self):
        print('called TextEdit.clear')
    def toPlainText(self):
        print('called TextEdit.toPlainText')
        return self._text


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
        print('called Label.__init__ with args', args)
        if args:
            self._text = args[0]
    def setVisible(self, value):
        print(f'called Label.setVisible to `{value}`')
    def setMinimumWidth(self, number):
        print(f'called Label.setMinimumWidth to `{number}`')
    def setMinimumHeight(self, number):
        print(f'called Label.setMinimumHeight to `{number}`')
    def setMaximumWidth(self, number):
        print(f'called Label.setMaximumWidth to `{number}`')
    def setText(self, text):
        print(f'called Label.setText with arg `{text}`')
        self._text = text
    def text(self):
        return self._text
    def setPixmap(self, data):
        print(f'called Label.setPixmap')


class MockButton:
    def mock_connect(*args):
        print('called connect with args', args)
    clicked = types.SimpleNamespace(connect=mock_connect)
    def __init__(self, *args):
        print('called PushButton.__init__ with args', args)
        self._text = args[0]
    def setMaximumWidth(self, number):
        print(f'called PushButton.setMaximumWidth to `{number}`')
    def text(self):
        return self._text
    def setText(self, value):
        self._text = value
        print(f'called PushButton.setText with arg `{value}`')

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
    Ok = 'okbutton'
    AcceptRole = 1
    Information = 2
    def __init__(self, *args, **kwargs):
        print('called QMessageBox with args', args, kwargs)
    def information(parent, caption, message):
        print(f'called QMessageBox.information with args `{caption}` `{message}`')
    def setDefaultButton(self, arg):
        print(f'called QMessageBox.setDefaultButton with arg `{arg}`')
    def setEscapeButton(self, arg):
        print(f'called QMessageBox.setEscapeButton with arg `{arg}`')
    def addButton(self, *args):
        print(f'called QMessageBox.addButton with arg `{args}`')
    def exec_(self, *args):
        print(f'called QMessageBox.exec_')
    def clickedButton(self):
        print(f'called QMessageBox.clickedButton')
        return 'button'


class MockScrollArea:
    def setWidget(self, arg):
        print(f'called ScrollArea.setWidget with arg of type `{type(arg)}`')
    def setWidgetResizable(self, arg):
        print(f'called ScrollArea.setWidgetResizable with arg `{arg}`')

class MockDialog:
    def __init__(self, *args, **kwargs):
        print('called QDialog.__init__')
    # def setLayout(self, arg):
    #     print(f'called QDialog.setLayout with arg of type `{type(arg)}`')
    def accept(self):
        print('called QDialog.accept')
