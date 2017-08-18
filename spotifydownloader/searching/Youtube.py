import re
from typing import Optional, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from metadata import Metadata
from searching.Base import SongSearcher
from util import ColorCodes


class YoutubeSearcher(SongSearcher):
    base_url = "https://www.youtube.com/results?{query}"
    search_format = "{title} - {artist}"

    def search(self, metadata: Metadata) -> Optional[str]:
        search_term = self.search_format.format(
              title=metadata.title, artist=metadata.artists[0]
        )
        query = self._urlencode({"search_query": search_term})

        url = self.base_url.format(query=query)

        print(ColorCodes.BLUE + url + ColorCodes.RESET)

        html_data = requests.get(url, {"User-Agent": "Mozilla/5.0"}).text

        document: BeautifulSoup = BeautifulSoup(html_data, "html.parser")

        found_videos: List[VideoMetadata] = []

        for tile in self.find_all_search_results(document):
            if self.is_live_stream(tile) or self.is_playlist(tile):
                continue
            video_metadata = VideoMetadata.from_video_tile(tile, url)
            if not video_metadata:
                print("Error parsing: '{0}'".format(tile))
                continue
            found_videos.append(video_metadata)

        # Find video with closest matching duration
        # found_videos.sort(key=lambda x: abs(metadata.duration_ms - x.duration))

        if not found_videos:
            return None

        for video in self.__get_by_title(found_videos, metadata.title.strip()):
            if metadata.artists[0].strip().lower() in video.title.lower():
                return video.url

        if self.__get_by_title(found_videos, metadata.artists[0]):
            return self.__get_by_title(found_videos, metadata.artists[0])[0].url

        return None

    @staticmethod
    def __get_by_title(all_videos: List, search: str) -> List:
        return [x for x in all_videos if search.lower() in x.title.lower()]

    @staticmethod
    def find_all_search_results(document):
        return document.find_all("div", {
            "class": "yt-lockup-dismissable yt-uix-tile"
        })

    @staticmethod
    def is_live_stream(element: Tag):
        return element.find("span", {"class": "yt-badge yt-badge-live"})

    @staticmethod
    def is_playlist(element: Tag):
        return element.find("span", {"class": "yt-pl-watch-queue-overlay"})


class VideoMetadata:
    def __init__(self, duration: int, title: str, channel_name: str, url: str):
        self.duration = duration
        self.title = title
        self.channel_name = channel_name
        self.url = url

    def __str__(self):
        return "<VideoMetadata title='{}', duration='{}', channel_name" \
               "='{}', url='{}'>" \
            .format(self.title, self.duration, self.channel_name, self.url)

    @classmethod
    def from_video_tile(cls, tile: Tag, base_url: str):
        title = cls.__get_title(tile)
        channel_name = cls.__get_channel_name(tile)
        duration = cls.__get_duration(tile)
        url = cls.__get_url(tile, base_url)

        if title and channel_name and duration and url:
            return VideoMetadata(duration, title, channel_name, url)
        print(title, channel_name, duration, url)

        return None

    @classmethod
    def __get_url(cls, tile, base_url: str) -> Optional[str]:
        title_tag = cls.__get_title_tag(tile)
        if not title_tag:
            return None
        url = title_tag["href"]

        return urljoin(base_url, url)

    @classmethod
    def __get_duration(cls, tile) -> Optional[int]:
        duration_tag = tile.find("span", {"class": re.compile(r"video-time.*")})
        if not duration_tag:
            return None
        duration_string = duration_tag.get_text()
        return cls.__duration_to_millis(duration_string)

    @classmethod
    def __get_channel_name(cls, tile) -> Optional[str]:
        channel_a_tag = tile.find(
              "a",
              {"href": re.compile(r"(/user/.*)|(/channel/.*)")}
        )
        if not channel_a_tag:
            return None
        return channel_a_tag.get_text()

    @classmethod
    def __get_title(cls, tile) -> Optional[str]:
        title_tag = cls.__get_title_tag(tile)
        if title_tag:
            return title_tag.get_text()

        return None

    @classmethod
    def __get_title_tag(cls, tile) -> Optional[Tag]:
        title: Tag = tile.find("h3", {"class": "yt-lockup-title"})
        if not title:
            return None
        title = title.findChild("a")
        if not title:
            return None
        return title

    @staticmethod
    def __duration_to_millis(duration: str) -> Optional[int]:
        """Converts a string of the form "3:4:23" to the milliseconds value."""
        try:
            parts = [int(x) for x in duration.split(":")]
            result = 0
            multipliers = [1000, 1000 * 60, 1000 * 60 * 60, 1000 * 60 * 60 * 24]

            for index, value in enumerate(reversed(parts)):
                result += multipliers[index] * value

            return result
        except ValueError:
            return None
