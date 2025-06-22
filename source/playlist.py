from playlist_tools import PlaylistTools


class Playlist:
    def __init__(self, name, owner_id, playlist_tools: PlaylistTools):
        self.name = name
        self.owner_id = owner_id
        self.playlist_tools = playlist_tools
        # get playlist from Spotify API, create if it doesn't exist yet
        self.spotify_playlist = playlist_tools.get_or_create_playlist(name=name)
        self.id = self.spotify_playlist['id']
        self._tracks = None
        print(f"loaded playlist {self.name}. len tracks: {len(self.tracks)}")

    @property
    def tracks(self):
        if self._tracks is None:
            self._tracks = self.playlist_tools.get_tracks_as_list(self.id)
        return self._tracks
    
    @property
    def track_ids(self):
        return [track['id'] for track in self.tracks]

    
