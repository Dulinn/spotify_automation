from spotipy import Spotify

from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client(scope=["playlist-modify-private", "playlist-modify-public", "user-library-read"]):
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))
