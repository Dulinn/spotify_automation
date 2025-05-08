from enum import Enum
from playlist import Playlist
from spotify_client import get_spotify_client
from contants import CORYS_USER_ID
import typing
from playlist_tools import PlaylistTools



class BasePlaylistSet:
    SET_NAME = None
    class NAME(Enum):
        pass

    def __init__(self, user_id):
        print(f"init called for type {type(self)}")
        if self.SET_NAME is None:
            raise ValueError("SET_NAME needs to be set by the child class")
        self.playlist_tools = PlaylistTools(user_id=user_id)
        # needs to be set by the child class
        self.playlists = {}
        for playlist_metadata in self.NAME:
            playlist_name = playlist_metadata.value
            playlist = Playlist(name=playlist_name, owner_id=user_id, playlist_tools=self.playlist_tools)
            self.playlists[playlist_metadata] = playlist
        self._tracks = None
        
    def track_in_playlist(self, playlist_name, track_id):
        return track_id in self.playlists[playlist_name]
            

    def get(self, playlist):
        return self.playlists.get(playlist)
    
    def get_all_playlist_names(self):
        pass

    @property
    def tracks(self):
        if self._tracks is None:
            self._tracks = []
            for playlist in self.playlists.values():
                self._tracks += playlist.tracks
        return self._tracks

    @property
    def track_ids(self):
        return [track['id'] for track in self.tracks]
    


class BasePlaylistSetAllTracks(BasePlaylistSet):
    def __init__(self, library_name, user_id):
        super().__init__(user_id=user_id)
        self.library_name = library_name
        self.user_id = user_id
        self.library = Playlist(name=self.library_name, owner_id=self.user_id, playlist_tools=self.playlist_tools)
        self.create_or_refresh_playlist_with_missing_tracks()

    
    def create_or_refresh_playlist_with_missing_tracks(self):
        #print(f"{type(self)}: len track_ids: {len(self.track_ids)}")
        #print(f"{type(self)}: len library track_ids: {len(self.library.track_ids)}")
        missing_tracks = [track_id for track_id in self.library.track_ids if track_id not in self.track_ids]
        missing_playlist_id = self.playlist_tools.create_or_clean_playlist(f"MISSING_{self.SET_NAME}", quiet=True)
        self.playlist_tools.add_tracks_to_playlist(playlist_id=missing_playlist_id, tracks=missing_tracks)
        

class BasePlaylistSetBPM(BasePlaylistSetAllTracks):
    SET_NAME = "BPM"
    class NAME(Enum):
        BPM_BELOW_70 = "BASE_BPM_BELOW_70"
        BPM_70_74 = "BASE_BPM_70_74"
        BPM_75_79 = "BASE_BPM_75_79"
        BPM_80_84 = "BASE_BPM_80_84"
        BPM_85_89 = "BASE_BPM_85_89"
        BPM_90_94 = "BASE_BPM_90_94"
        BPM_95_99 = "BASE_BPM_95_99"
        BPM_100_104 = "BASE_BPM_100_104"
        BPM_105_109 = "BASE_BPM_105_109"
        BPM_110_114 = "BASE_BPM_110_114"
        BPM_115_119 = "BASE_BPM_115_119"
        BPM_120_124 = "BASE_BPM_120_124"
        BPM_125_129 = "BASE_BPM_125_129"
        BPM_130_134 = "BASE_BPM_130_134"
        BPM_135_139 = "BASE_BPM_135_139"
        BPM_ABOVE_140 = "BASE_BPM_ABOVE_140"
    
    def __init__(self, library, user_id):
        super().__init__(library_name=library, user_id=user_id)


class BasePlaylistSetEnergy(BasePlaylistSetAllTracks):
    SET_NAME = "ENERGY"
    class NAME(Enum):
        LOW = "BASE_ENERGY_LOW"
        MEDUIM = "BASE_ENERGY_MEDIUM"
        HIGH = "BASE_ENERGY_HIGH"
    
    def __init__(self, library, user_id):
        print(f"init of BasePlaylistSetEnergy called")
        super().__init__(library_name=library, user_id=user_id)

class BasePlaylistSetStyle(BasePlaylistSet):
    SET_NAME = "STYLE"
    class NAME(Enum):
        BLUES = "BASE_BLUES"
    



