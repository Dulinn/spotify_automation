from spotipy import Spotify
import spotipy.util as util


def get_spotify_client(user_id, scope=["playlist-modify-private", "playlist-modify-public", "user-library-read"]):
    token = util.prompt_for_user_token(user_id, scope, show_dialog=True)
    if token:
        print("Token: ", token)
        return Spotify(auth=token,)
    else:
        print("Can't get token for", user_id)

    #return Spotify(client_credentials_manager=SpotifyClientCredentials(), scope=scope)