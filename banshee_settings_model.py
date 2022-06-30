"""database mappings for banshee GUI
"""
import sys
import pathlib

PROJ = pathlib.Path.home() / 'projects'
CONF = pathlib.Path.home() / '.config'
LOCAL = pathlib.Path.home() / '.local' / 'share'
databases = {
    'banshee': str(CONF / 'banshee-1/banshee.db'),
    'clementine': str(CONF / 'Clementine/clementine.db'),
    'strawberry': str(LOCAL / 'strawberry' / 'strawberry' / 'strawberry.db'),
    'CDDB': '<path-to-cddb-database-if-any>'}
# voor albums moeten we via de Django settings
sys.path.append(str(PROJ / 'albums' / 'albums'))
from settings import DATABASES
databases['albums'] = DATABASES['default']['NAME']
