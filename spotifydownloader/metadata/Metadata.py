from typing import List, Optional


class Metadata:
    def __init__(
          self, title: str, album: str, album_art_url: str,
          artists: List[str], genre: Optional[List[str]], track_number: int,
          release_date: Optional[str], duration_ms: int, total_track_number: int
    ):
        self.title: str = title
        self.album: str = album
        self.album_art_url: str = album_art_url
        self.artists: List[str] = artists
        self.genre: str = genre
        self.track_number: int = track_number
        self.total_track_number: int = total_track_number
        self.release_date: str = release_date
        self.duration_ms: int = duration_ms

    def __str__(self):
        return "<Metadata, title={title}, album={album}," \
               " album_art_url={album_art_url}, artists={artists}," \
               " genre={genre}, track_number={track_number}," \
               " release_data={release_date}, duration_ms={duration_ms}>" \
            .format(title=self.title, album=self.album,
                    album_art_url=self.album_art_url, artists=self.artists,
                    genre=self.genre, track_number=self.track_number,
                    release_date=self.release_date,
                    duration_ms=self.duration_ms)
