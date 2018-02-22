import os
from typing import List, Optional

import Config
import PathHelper
from conversion import FfmpegConverter, Converter
from downloader import Downloader
from downloader.YoutubeDlDownloader import YoutubeDlDownloader
from metadata import Metadata
from metadata.fetcher import SpotifyMetadataFetcher, MetadataFetcher
from metadata.injector import MutagenMetadataInjector, MetadataInjector
from normalization import Normalizer
from searching.Base import SongSearcher
from searching.Youtube import YoutubeSearcher
from util import ColorCodes

downloaders: List[Downloader] = [YoutubeDlDownloader()]
converters: List[Converter] = [FfmpegConverter()]
metadata_fetchers: List[MetadataFetcher] = [SpotifyMetadataFetcher()]
metadata_injectors: List[MetadataInjector] = [MutagenMetadataInjector()]
searchers: List[SongSearcher] = [YoutubeSearcher()]


def download_spotify_song(
        spotify_track_id: str, output_folder: str, redownload_if_exists: bool):
    metadata = fetch_metadata(spotify_track_id)
    if not metadata:
        print(
            "No metadata found for track with it '{}'".format(
                spotify_track_id)
        )
        return

    file_name = "{0} - {1}".format(metadata.title, metadata.artists[0])
    output_file = PathHelper.get_output_file(file_name, output_folder)

    if not redownload_if_exists and os.path.exists(output_file):
        return

    url: str = search_song(metadata)

    if not url:
        print("No url found for track with metadata '{0}'".format(metadata))
        return

    tmp_file = PathHelper.get_tmp_file(file_name)
    if not download_song(url, tmp_file):
        print("Error downloading a song from '{0}'".format(url))
        return

    if not convert_song(tmp_file, output_file):
        print("Error converting song '{0}'".format(tmp_file))
        return

    print(
        ColorCodes.BLUE + "Tagging:" + ColorCodes.RESET + " In progress",
        end=""
    )

    if not Normalizer.normalize(Config.tmp_folder, output_file):
        print(
            ColorCodes.RED
            + "Deleting generated file as a critical error occurred..."
            + ColorCodes.RESET
        )
        os.remove(output_file)
        return

    if not inject_metadata(output_file, metadata):
        print("\r", end="")
        print("Unable to inject metadata to '{0}'".format(output_file))
        return
    print(
        "\r" + ColorCodes.BLUE + "Tagging: "
        + ColorCodes.GREEN + "Done." + " " * 25 + ColorCodes.RESET
    )


def fetch_metadata(spotify_track_id: str) -> Optional[Metadata]:
    for fetcher in metadata_fetchers:
        metadata = fetcher.fetch(spotify_track_id)
        if metadata:
            return metadata
    return None


def search_song(metadata: Metadata) -> Optional[str]:
    for searcher in searchers:
        result = searcher.search(metadata)
        if result:
            return result
    return None


def download_song(url: str, target_file: str) -> bool:
    for downloader in downloaders:
        if downloader.can_download(url):
            downloader.download(url, target_file)
            return True
    return False


def convert_song(input_file: str, output_file: str):
    for converter in converters:
        if converter.can_convert(input_file):
            converter.convert(input_file, output_file)
            return True
    return False


def inject_metadata(file: str, metadata: Metadata):
    """Injects a file with the given metadata."""
    for metadata_injector in metadata_injectors:
        if metadata_injector.can_inject(file):
            metadata_injector.inject(file, metadata)
            return True
    return False
