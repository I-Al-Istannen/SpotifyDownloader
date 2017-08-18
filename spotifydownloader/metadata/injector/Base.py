from abc import ABC, abstractmethod

from metadata import Metadata


class MetadataInjector(ABC):
    @abstractmethod
    def can_inject(self, file: str):
        pass

    @abstractmethod
    def inject(self, file: str, metadata: Metadata):
        pass