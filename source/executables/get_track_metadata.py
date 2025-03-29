from source.spotify_client import get_spotify_client
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description="Get track metadata from Spotify")
parser.add_argument(
    "track",
    type=str,
    help="Spotify track URL or ID",
)
args = parser.parse_args()
client = get_spotify_client()
track_data = client.track(track_id=args.track)
pprint(track_data)
