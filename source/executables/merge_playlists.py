from source.playlist_tools import PlaylistTools, DeduplicationMethod
from source.contants import CORYS_USER_ID, TEST_ACCOUNT_USER_ID
import json

playlist_tools = PlaylistTools(user_id=CORYS_USER_ID)

load_from_file = False


playlists_to_merge = ("1zpTt0tlnZSSqOdkaoOidG", "6q6r9n9A4GV475fhOJ45lx")
if load_from_file:
    filepath = "data/corys_social_playlists.json"
    with open(filepath) as input_file:
        playlists = json.load(input_file)
    playlists_to_merge = [entry["id"] for entry in playlists]

new_playlist_id = playlist_tools.create_or_clean_playlist(name="BASE_LIBRARY")


playlist_tools.merge_and_deduplicate(
    source_playlist_ids=playlists_to_merge,
    target_playlist_id=new_playlist_id,
    deduplication_method=DeduplicationMethod.ISRC,
)
