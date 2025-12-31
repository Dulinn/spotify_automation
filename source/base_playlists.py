from enum import Enum
from collections import Counter
from playlist import Playlist
from playlist_tools import PlaylistTools
import config

PLAYLIST_TOOLS = PlaylistTools()
class Library:
    def __init__(self, library_name):
        self._library_playlist = Playlist(name=library_name, owner_id=config.USER_ID, playlist_tools=PLAYLIST_TOOLS)
        self._baseplaylistset_style = None
        self._baseplaylistset_energy = None
        self._baseplaylistset_bpm = None
        self._baseplaylistset_like = None
    
    @property
    def library_playlist(self):
        return self._library_playlist
    
    @property
    def tracks(self):
        return self.library_playlist.tracks
    
    @property
    def track_ids(self):
        return self.library_playlist.track_ids
    
    @property
    def style(self):
        if self._baseplaylistset_style is None:
            raise(ValueError("Style not set"))
        return self._baseplaylistset_style
    
    @style.setter
    def style(self, style):
        self._baseplaylistset_style = style

    @property
    def energy(self):
        if self._baseplaylistset_energy is None:
            raise(ValueError("Energy not set"))
        return self._baseplaylistset_energy
    
    @energy.setter
    def energy(self, energy):
        self._baseplaylistset_energy = energy

    @property
    def bpm(self):
        if self._baseplaylistset_bpm is None:
            raise(ValueError("BPM not set"))
        return self._baseplaylistset_bpm

    @bpm.setter
    def bpm(self, bpm):
        self._baseplaylistset_bpm = bpm

    @property
    def like(self): 
        if self._baseplaylistset_like is None:
            raise(ValueError("Like not set"))
        return self._baseplaylistset_like
    
    @like.setter
    def like(self, like):
        self._baseplaylistset_like = like  

    def check_missing_songs_in_playlistsets_not_in_library(self):
        missing_tracks = []
        all_playlistset_track_ids = set()
        if self._baseplaylistset_style is not None:
            all_playlistset_track_ids.update(self.style.track_ids)
        if self._baseplaylistset_energy is not None:
            all_playlistset_track_ids.update(self.energy.track_ids)
        if self._baseplaylistset_bpm is not None:
            all_playlistset_track_ids.update(self.bpm.track_ids)
        if self._baseplaylistset_like is not None:
            all_playlistset_track_ids.update(self.like.track_ids)
        
        for track_id in all_playlistset_track_ids:
            if track_id not in self.track_ids:
                missing_tracks.append(track_id)
        missing_in_base_library_playlist = PLAYLIST_TOOLS.create_or_clean_playlist("MISSING_IN_BASE_LIBRARY", quiet=True)
        PLAYLIST_TOOLS.add_tracks_to_playlist(missing_in_base_library_playlist, missing_tracks)


    def get_track_statistics(self, track_id):
        stats = {}
        if self._baseplaylistset_style is not None:
            for style_name, playlist in self.style.playlists.items():
                if track_id in playlist.track_ids:
                    stats['style'] = style_name.value
                    break
        if self._baseplaylistset_energy is not None:
            for energy_name, playlist in self.energy.playlists.items():
                if track_id in playlist.track_ids:
                    stats['energy'] = self.energy.NAME_TO_ENERGY[energy_name]
                    break
        if self._baseplaylistset_bpm is not None:
            for bpm_name, playlist in self.bpm.playlists.items():
                if track_id in playlist.track_ids:
                    stats['bpm'] = self.bpm.NAME_TO_BPM[bpm_name]
                    break
        if self._baseplaylistset_like is not None:
            for like_name, playlist in self.like.playlists.items():
                if track_id in playlist.track_ids:
                    stats['like'] = self.like.NAME_TO_LIKE[like_name]
                    break
        return stats

    

class BasePlaylistSet:
    SET_NAME = None
    class NAME(Enum):
        pass

    def __init__(self):
        print(f"init called for type {type(self)}")
        if self.SET_NAME is None:
            raise ValueError("SET_NAME needs to be set by the child class")
        # needs to be set by the child class
        self.playlists = {}
        for playlist_metadata in self.NAME:
            playlist_name = playlist_metadata.value
            playlist = Playlist(name=playlist_name, owner_id=config.USER_ID, playlist_tools=PLAYLIST_TOOLS)
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
    def __init__(self, library):
        super().__init__()
        self.library = library
        self.create_or_refresh_playlist_with_missing_tracks()
        self.create_or_refresh_playlist_with_duplicates()

    
    def create_or_refresh_playlist_with_missing_tracks(self):
        missing_tracks = [track_id for track_id in self.library.track_ids if track_id not in self.track_ids]
        missing_playlist_id = PLAYLIST_TOOLS.create_or_clean_playlist(f"MISSING_{self.SET_NAME}", quiet=True)
        PLAYLIST_TOOLS.add_tracks_to_playlist(playlist_id=missing_playlist_id, tracks=missing_tracks)

    def create_or_refresh_playlist_with_duplicates(self):
        playlist_id = PLAYLIST_TOOLS.create_or_clean_playlist(name=f"DUPLICATE_{self.SET_NAME}", quiet=True)
        # check if there are duplicates
        len_all_playlists_with_duplicates = len(self.tracks)
        len_all_playlists_without_duplicates = len(set(self.track_ids))
        if len_all_playlists_with_duplicates != len_all_playlists_without_duplicates:
            # there are duplicates, lets find them
            track_counter = Counter(self.track_ids)
            duplicates = [track_id for track_id, count in Counter(self.track_ids).items() if count > 1]
            PLAYLIST_TOOLS.add_tracks_to_playlist(playlist_id=playlist_id, tracks=duplicates)
        
        

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
    
    NAME_TO_BPM = {
        NAME.BPM_BELOW_70: 67,
        NAME.BPM_70_74: 72,
        NAME.BPM_75_79: 77,
        NAME.BPM_80_84: 82,
        NAME.BPM_85_89: 87,
        NAME.BPM_90_94: 92,
        NAME.BPM_95_99: 97,
        NAME.BPM_100_104: 102,
        NAME.BPM_105_109: 107,
        NAME.BPM_110_114: 112,
        NAME.BPM_115_119: 117,
        NAME.BPM_120_124: 122,
        NAME.BPM_125_129: 127,
        NAME.BPM_130_134: 132,
        NAME.BPM_135_139: 137,
        NAME.BPM_ABOVE_140: 142,
    }

    def __init__(self, library):
        super().__init__(library=library)


class BasePlaylistSetEnergy(BasePlaylistSetAllTracks):
    SET_NAME = "ENERGY"
    class NAME(Enum):
        LOW = "BASE_ENERGY_LOW"
        MEDIUM = "BASE_ENERGY_MEDIUM"
        HIGH = "BASE_ENERGY_HIGH"
    
    NAME_TO_ENERGY = {
        NAME.LOW: 1,
        NAME.MEDIUM: 2,
        NAME.HIGH: 3,
    }
    
    def __init__(self, library):
        print(f"init of BasePlaylistSetEnergy called")
        super().__init__(library=library)

class BasePlaylistSetStyle(BasePlaylistSet):
    SET_NAME = "STYLE"
    class NAME(Enum):
        BLUES = "BASE_BLUES"


class BasePlaylistSetLike(BasePlaylistSetAllTracks):
    SET_NAME = "LIKE"

    class NAME(Enum):
        LOW = "BASE_LIKE_LOW"
        MEDUÌUM = "BASE_LIKE_MEDIUM"
        HIGH = "BASE_LIKE_HIGH"
    
    NAME_TO_LIKE = {
        NAME.LOW: 1,
        NAME.MEDUÌUM: 2,
        NAME.HIGH: 3,
    }



