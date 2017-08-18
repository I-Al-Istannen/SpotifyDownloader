import os
import socket
import sys
import traceback
from time import sleep
from typing import List, Tuple

import ArgumentParsing
import Config
import SongDownloader
from spotifyapi import PlaylistIO
from util import ColorCodes


def _download_playlist_tracks(url: str):
    print(
          ColorCodes.YELLOW + "Output file:",
          ColorCodes.GREEN + PlaylistIO.write_playlist_by_url(
                url, Config.tmp_folder
          ),
          ColorCodes.RESET
    )


def _download_playlist(name: str, redownload_if_exists: bool = False):
    playlist_path = os.path.join(Config.tmp_folder, name + ".txt")

    if not os.path.exists(playlist_path):
        print(
              ColorCodes.RED + ColorCodes.BOLD
              + "Unknown playlist '{0}'!".format(
                    ColorCodes.PURPLE + name + ColorCodes.RED
              )
              + ColorCodes.RESET
        )
        return

    failed_songs: List[Tuple(int, str)] = []

    # noinspection PyBroadException,PyShadowingNames
    def downloader_function(
          line_number: int, track_id: str):
        print()
        print(ColorCodes.PURPLE + ColorCodes.BOLD + "Song: ", line_number)
        try:
            SongDownloader.download_spotify_song(track_id,
                                                 Config.output_folder,
                                                 redownload_if_exists)
        except Exception:
            print(
                  "\r" + ColorCodes.RED
                  + "Error downloading song. Retrying at the end." + " " * 50
                  + ColorCodes.RESET
            )

            cls, exception, traceback_obj = sys.exc_info()

            if not isinstance(exception, socket.timeout):
                traceback.print_exc()

            failed_songs.append((line_number, track_id))
            sleep(5)  # let it try to recover and prevent spam

    PlaylistIO.do_for_each_playlist_entry(playlist_path, downloader_function)

    while failed_songs:
        line_number, song_id = failed_songs.pop()
        downloader_function(line_number, song_id)


if __name__ == '__main__':
    socket.setdefaulttimeout(10)  # 10 Seconds timeout

    parsed = ArgumentParsing.get_argument_parser().parse_args()

    if parsed.output_folder:
        Config.output_folder = parsed.output_folder

    if parsed.download_playlist:
        _download_playlist_tracks(parsed.download_playlist)
        exit(0)
    if parsed.playlist:
        if parsed.redownload_if_exists:
            _download_playlist(parsed.playlist, parsed.redownload_if_exists)
        else:
            _download_playlist(parsed.playlist)
        exit(0)

    ArgumentParsing.get_argument_parser().print_help()
