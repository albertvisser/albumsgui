"""database mappings for banshee GUI
"""
import pathlib

CONF = pathlib.Path.home() / '.config'
databases = {
    'albums': '<path-to-albums-database>',
    'banshee': str(pathlib.Path.home() / 'banshee-1/banshee.db'),
    'clementine': str(pathlib.Path.home() / 'Clementine/clementine.db'),
    'CDDB': '<path-to-cddb-database-if-any>'}
