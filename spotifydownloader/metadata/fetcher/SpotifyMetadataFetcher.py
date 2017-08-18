from typing import Optional

from metadata import Metadata
from metadata.fetcher.MetadataFetcher import MetadataFetcher
from spotifyapi import SpotifyApi


class SpotifyMetadataFetcher(MetadataFetcher):
    @classmethod
    def fetch(cls, track_id: str):
        track_information = SpotifyApi.fetch_track_information(track_id)
        if track_information:
            return cls.__parse_track_to_metadata(track_information)

    @classmethod
    def __parse_track_to_metadata(cls, track: dict) -> Metadata:
        title = track["name"]
        album = track["album"]["name"]
        album_art_url = track["album"]["images"][0]["url"]
        artists = [artist["name"] for artist in track["artists"]]
        track_number = track["track_number"]
        duration_ms = int(track["duration_ms"])

        album_metadata = cls.__parse_metadata_for_album(track["album"]["id"])

        total_track_number = album_metadata["track_count"]
        genre = album_metadata["genres"]
        release_date = album_metadata["release_date"]

        # noinspection PyTypeChecker
        return Metadata(
              title=title, album=album, album_art_url=album_art_url,
              artists=artists, track_number=track_number, genre=genre,
              release_date=release_date, duration_ms=duration_ms,
              total_track_number=total_track_number
        )

    @staticmethod
    def __parse_metadata_for_album(album_id: str) -> Optional[dict]:
        album = SpotifyApi.fetch_album_information(album_id)
        if not album:
            return {}
        return {
            "genres": album["genres"],
            "track_count": int(album["tracks"]["total"]),
            "release_date": album["release_date"]
        }
