from typing import List, Tuple

import spotipy
from spotipy import oauth2

from spotifyapi.Credentials import credentials


def __generate_token():
    """Generate the token. Please respect these credentials :) (Not mine...)"""
    return credentials.get_access_token()


spotify = spotipy.Spotify(auth=__generate_token())
max_api_oauth_tries: int = 5


def with_api(f):
    """A decorator that means that a call queries the API"""

    def decorated(*args, counter: int = 0, **kwargs):
        global max_api_oauth_tries
        if counter > max_api_oauth_tries:
            return

        try:
            return f(*args, **kwargs)
        except spotipy.oauth2.SpotifyOauthError:
            decorated(counter=counter + 1, *args, **kwargs)

    return decorated


@with_api
def fetch_track_information(track_id: str) -> dict:
    return spotify.track(track_id=track_id)


@with_api
def fetch_album_information(album_id: str) -> dict:
    return spotify.album(album_id)


@with_api
def fetch_playlist_tracks_and_name(user_id: str, playlist_id: str) -> \
      Tuple[str, List[str]]:
    tracks = []
    response = spotify.user_playlist(user=user_id,
                                     playlist_id=playlist_id)

    playlist_name = response["name"]

    while response:
        for item in response["tracks"]["items"]:
            track_id = item["track"]["id"]
            tracks.append(track_id)
        response = spotify.next(response["tracks"])

    return playlist_name, tracks
