from base_playlists import BasePlaylistSetStyle, BasePlaylistSetEnergy, BasePlaylistSetBPM
from contants import CORYS_USER_ID, LIBRARY

#style = BasePlaylistSetStyle(user_id=CORYS_USER_ID)
energy = BasePlaylistSetEnergy(library=LIBRARY, user_id=CORYS_USER_ID)
bpm = BasePlaylistSetBPM(library=LIBRARY, user_id=CORYS_USER_ID)