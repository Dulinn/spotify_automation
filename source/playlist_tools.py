import spotipy
from source.contants import TEST_ACCOUNT_USER_ID
from source.spotify_client import get_spotify_client
from enum import Enum
from itertools import chain


class DeduplicationMethod(Enum):
    TRACK_ID = 1
    NAME_AND_ARTIST = 2
    ISRC = 3


class PlaylistTools:
    def __init__(self, user_id=TEST_ACCOUNT_USER_ID):
        self.spotify_client = get_spotify_client(user_id=user_id)
        print(self.spotify_client.me())
        self.user_id = user_id

    def create_or_clean_playlist(self, name, user_id=None):
        if user_id is None:
            user_id = self.user_id
        print(f"Creating or cleaning playlist {name} with for user {user_id}")
        user_playlists = self.spotify_client.user_playlists(user=user_id)
        playlists_with_name = [
            playlist for playlist in user_playlists["items"] if playlist["name"] == name
        ]
        if len(playlists_with_name) == 0:
            response = self._create_playlist(name)
            return response["id"]
        elif len(playlists_with_name) == 1:
            id = playlists_with_name[0]["id"]
            confirmation = input(
                f"Playlist {name}, id {id} already exists. Do you want to clean it? (y/n)"
            )
            if confirmation.lower() != "y":
                print("Aborting.")
                return None
            self._clean_playlist(id)
            return id
        else:
            raise ValueError(
                f"There is more than one playlist with the name {name}, so I don't know which one to clean. Please clean up first."
            )

    def _create_playlist(self, name, user_id=None):
        if user_id is None:
            user_id = self.user_id
        return self.spotify_client.user_playlist_create(user_id, name)

    def _clean_playlist(self, id):
        self.spotify_client.playlist_replace_items(id, list())

    def merge_and_deduplicate(
        self,
        source_playlist_ids,
        target_playlist_id,
        deduplication_method=DeduplicationMethod.TRACK_ID,
    ):
        track_list = [self.get_and_iterate_tracks(id) for id in source_playlist_ids]
        all_tracks = chain(*track_list)
        merged_tracks_dict = self.deduplicate_tracks(
            all_tracks, deduplication_method=deduplication_method
        )

        print(f"Merged and deduplicated {len(source_playlist_ids)} playlists.")
        self.add_tracks_to_playlist(
            target_playlist_id, list(merged_tracks_dict.values())
        )

    def deduplicate_tracks(self, tracks, deduplication_method, skip_none=True):
        deduplicated_tracks_dict = dict()
        number_of_tracks_with_duplicates = 0
        for track in tracks:
            if skip_none and track["id"] is None:
                print("Skipping None track")
                continue
            if deduplication_method == DeduplicationMethod.NAME_AND_ARTIST:
                deduplicated_tracks_dict[self.track_to_str(track)] = track["id"]
            elif deduplication_method == DeduplicationMethod.TRACK_ID:
                deduplicated_tracks_dict[track["id"]] = track["id"]
            elif DeduplicationMethod.ISRC:
                if (not "external_ids" in track) or (
                    not "isrc" in track["external_ids"]
                ):
                    print(
                        f"Track does not have a ISRC: {track['external_urls']['spotify']}"
                    )
                else:
                    deduplicated_tracks_dict[track["external_ids"]["isrc"]] = track[
                        "id"
                    ]
            else:
                raise NotImplementedError(
                    f"Unknown deduplication method: {deduplication_method}"
                )

            number_of_tracks_with_duplicates += 1
        print(
            f"Deduplicated {number_of_tracks_with_duplicates} tracks by {deduplication_method}, resulting in {len(deduplicated_tracks_dict)} unique tracks."
        )
        return deduplicated_tracks_dict

    def add_tracks_to_playlist(self, playlist_id, tracks, user_id=None):
        if user_id is None:
            user_id = self.user_id
        for batch in self._list_batcher(list_to_batch=tracks, batch_size=100):
            try:
                self.spotify_client.user_playlist_add_tracks(
                    user=user_id, playlist_id=playlist_id, tracks=batch
                )
            except (TypeError, spotipy.exceptions.SpotifyException):
                for track in self._list_batcher(list_to_batch=batch, batch_size=1):
                    try:
                        self.spotify_client.user_playlist_add_tracks(
                            user=user_id,
                            playlist_id=playlist_id,
                            tracks=track,
                        )
                    except TypeError as e:
                        print(f"TypeError occurred at track {track}: {e}")
                    except spotipy.exceptions.SpotifyException as e:
                        print(f"SpotiffyException at track {track}: {e}")

    def _list_batcher(self, list_to_batch, batch_size):
        for lower, upper in self._batcher(
            length=len(list_to_batch), batch_size=batch_size
        ):
            yield list_to_batch[lower:upper]

    def _batcher(self, length, batch_size):
        i = 0
        while i * batch_size < length:
            yield (i * batch_size, (i + 1) * batch_size)
            i += 1

    def get_and_iterate_tracks(self, playlist_id):
        playlist = self.spotify_client.playlist_items(playlist_id=playlist_id, limit=1)
        playlist_len = playlist["total"]
        batch_size = 100
        for lower, upper in self._batcher(playlist_len, batch_size=batch_size):
            playlist = self.spotify_client.playlist_items(
                playlist_id=playlist_id, limit=batch_size, offset=lower
            )
            for track in playlist["items"]:
                yield track["track"]

    def update_playlist_description(self, playlist_id, description):
        self.spotify_client.playlist_change_details(
            playlist_id=playlist_id, description=description
        )

    @staticmethod
    def track_to_str(track):
        return f"{track['name']} - {', '.join(artist['name'] for artist in track['artists'])}"
