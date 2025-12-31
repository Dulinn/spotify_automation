from base_playlists import Library, BasePlaylistSetStyle, BasePlaylistSetEnergy, BasePlaylistSetBPM, BasePlaylistSetLike
from generated_playlists import GeneratedPlaylist
from contants import CORYS_USER_ID, LIBRARY
from datetime import datetime, timedelta


def load_base_library():
    library = Library(library_name=LIBRARY)
    return library

def load_base_style(library):
    style = BasePlaylistSetStyle()
    library.style = style
    return style

def load_base_energy(library):
    energy = BasePlaylistSetEnergy(library=library)
    library.energy = energy
    return energy

def load_base_bpm(library):
    bpm = BasePlaylistSetBPM(library=library)
    library.bpm = bpm
    return bpm

def load_base_like(library):
    like = BasePlaylistSetLike(library=library)
    library.like = like
    return like


def load_base_playlists():
    library = load_base_library()
    load_base_style(library)
    load_base_energy(library)
    load_base_bpm(library)
    load_base_like(library)
    return library

def generate_playlists(library):

    generated_playlist_data=[
        {"name": "WCS Large",
        "description": "BASE_LIBRARY without Blues and not liked tracks",
        "filter": lambda x: x['id'] not in library.like.get(BasePlaylistSetLike.NAME.LOW).track_ids and \
        x not in library.style.get(BasePlaylistSetStyle.NAME.BLUES).track_ids
        },
        {"name": "WCS Favorites",
        "description": "Most liked songs",
        "filter": lambda x: x['id'] in library.like.get(BasePlaylistSetLike.NAME.HIGH).track_ids
        },
        {"name": "WCS Last 6 Months",
         "description": "Songs added to library in the last 6 months",
         "filter": lambda x: datetime.now() - timedelta(days=30*6) < x['added_at'] and \
            x['id'] not in library.like.get(BasePlaylistSetLike.NAME.LOW).track_ids
         },
         {"name": "WCS Medium and Low Energy",
          "description": "BASE_LIBRARY without High Energy songs",
          "filter": lambda x: x['id'] not in library.like.get(BasePlaylistSetLike.NAME.LOW).track_ids and \
          x['id'] not in library.style.get(BasePlaylistSetStyle.NAME.BLUES).track_ids and \
            (x['id'] in library.energy.get(BasePlaylistSetEnergy.NAME.MEDIUM).track_ids or \
            x['id'] in library.energy.get(BasePlaylistSetEnergy.NAME.LOW).track_ids)       
        },
        {
            "name": "WCS Walk 100-114 BPM",
            "description": "Songs with BPM between 100 and 114",
            "filter": lambda x: x['id'] not in library.like.get(BasePlaylistSetLike.NAME.LOW).track_ids and \
            (x['id'] in library.bpm.get(BasePlaylistSetBPM.NAME.BPM_100_104).track_ids or \
            x['id'] in library.bpm.get(BasePlaylistSetBPM.NAME.BPM_105_109).track_ids or \
            x['id'] in library.bpm.get(BasePlaylistSetBPM.NAME.BPM_110_114).track_ids)
        },
        {
            "name": "WCS Walk 115-124 BPM",
            "description": "Songs with BPM between 115 and 124",
            "filter": lambda x: x['id'] not in library.like.get(BasePlaylistSetLike.NAME.LOW).track_ids and \
            (x['id'] in library.bpm.get(BasePlaylistSetBPM.NAME.BPM_115_119).track_ids or \
            x['id'] in library.bpm.get(BasePlaylistSetBPM.NAME.BPM_120_124).track_ids)
        }
    ]


    for data in generated_playlist_data:
        try:
            GeneratedPlaylist(name=data['name'], library=library, filter_function=data['filter'], description=data['description']).sync()
        except (ValueError, KeyError) as e:
            print(f"Could not create playlist {data['name']}: {e}")


if __name__ == "__main__":
    #library = load_base_playlists()
    library = load_base_library()
    load_base_style(library)
    generate_playlists(library=library)