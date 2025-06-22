from playlist import Playlist
from base_playlists import Library
from playlist_tools import PlaylistTools

PLAYLIST_TOOLS = PlaylistTools()

class GeneratedPlaylist:
    def __init__(self, name, library: Library, filter_function, description=None):
        self.name = name
        self.library = library
        self.filter_function = filter_function
        self.description = description

    def sync(self):
        tracks = [track for track in self.library.track_ids if self.filter_function(track)]
        playlist_id = PLAYLIST_TOOLS.create_or_clean_playlist(name=self.name, quiet=True)
        PLAYLIST_TOOLS.add_tracks_to_playlist(playlist_id=playlist_id, tracks=tracks)
        if self.description is not None:
            PLAYLIST_TOOLS.update_playlist_description(playlist_id=playlist_id, description=self.description)

        


