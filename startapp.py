import pathlib
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import PyQt4.QtWebKit as webkit
from viewhtml import HtmlView

base_dir = pathlib.Path('/home/albert/projects/albums-cgi')
## base_dir = pathlib.Path('/home/albert/www/django/albums/albums/templates')
## tpl_dir = base_dir / 'muziek'
## start_page = tpl_dir / 'start.html'
## select_page = tpl_dir / 'select.html'
## detail_page = tpl_dir / 'detail.html'

sys.path.append(str(base_dir / 'main_logic'))
from start_main import start

app = gui.QApplication(sys.argv)
frm = HtmlView()
meld = ''
lines = start(meld)
start_page = "".join(lines)
frm.show_html(start_page)
frm.show()
sys.exit(app.exec_())
