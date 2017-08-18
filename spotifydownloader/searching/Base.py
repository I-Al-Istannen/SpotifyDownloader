from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlencode

from metadata import Metadata


class SongSearcher(ABC):
    @abstractmethod
    def search(self, metadata: Metadata) -> Optional[str]:
        """Searches a song.

        :return: the url, if found, None if not
        """
        pass

    @staticmethod
    def _urlencode(query: dict) -> str:
        return urlencode(query=query)
