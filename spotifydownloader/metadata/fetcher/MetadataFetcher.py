from abc import ABC, abstractmethod

from metadata import Metadata


class MetadataFetcher(ABC):
    @classmethod
    @abstractmethod
    def fetch(cls, track_id: str) -> Metadata:
        pass
