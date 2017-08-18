import os
from typing import Callable

import PathHelper
from spotifyapi import SpotifyApi


def write_playlist_by_url(playlist_url: str, output_folder: str) -> str:
    """Writes the playlist with the given url to a file.

    :return: The path to the written file
    """
    parts = split_playlist_url_in_parts(playlist_url)
    return write_playlist(parts[0], parts[1], output_folder)


def split_playlist_url_in_parts(playlist_url: str) -> tuple:
    """Splits the url in the relevant parts.

    :return: A tuple. [0] is the user id, [1] the playlist id
    """
    # Format: https://open.spotify.com/user/<user>/playlist/<playlist id>
    parts = playlist_url.split("/")
    playlist_id = parts[-1]
    user_id = parts[-3]

    return user_id, playlist_id


def write_playlist(user_id: str, playlist_id: str, output_folder: str) -> str:
    """Writes a playlist to a file."""
    name, tracks = SpotifyApi.fetch_playlist_tracks_and_name(user_id,
                                                             playlist_id)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder,
                               PathHelper.sanitize_path(name) + ".txt")

    with open(output_file, "w") as file:
        for track_id in tracks:
            file.write(track_id)
            file.write("\n")

    return output_file


def do_for_each_playlist_entry(
      file_path: str, id_consumer: Callable[[int, str], None]):
    """
    Applies the given function to each index and id in the given input file.
    """

    line_number = 0
    with open(file_path, "r") as file:
        line = file.readline()
        while line:
            line_number = line_number + 1
            id_consumer(line_number, line.rstrip())
            line = file.readline()
