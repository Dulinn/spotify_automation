from base_playlists import Library, BasePlaylistSetStyle, BasePlaylistSetEnergy, BasePlaylistSetBPM, BasePlaylistSetLike
from generated_playlists import GeneratedPlaylist
from contants import CORYS_USER_ID, LIBRARY

library = Library(library_name=LIBRARY)
style = BasePlaylistSetStyle()
#energy = BasePlaylistSetEnergy(library=library)
bpm = BasePlaylistSetBPM(library=library)
like = BasePlaylistSetLike(library=library)

generated_playlist_data=[
    {"name": "WCS Large",
     "description": "BASE_LIBRARY without Blues and not liked tracks",
     "filter": lambda x: x not in like.get(BasePlaylistSetLike.NAME.LOW).track_ids and \
        x not in style.get(BasePlaylistSetStyle.NAME.BLUES).track_ids
     },
]

for data in generated_playlist_data:
    GeneratedPlaylist(name=data['name'], library=library, filter_function=data['filter'], description=data['description']).sync()


