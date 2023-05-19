"""dml for Strawberry database
"""
from apps.clementine_dml import (databases, list_artists, list_albums, list_album_covers,
                                 list_tracks_for_artist, list_tracks_for_album)
# from .banshee_settings import databases
DB = databases['strawberry']
