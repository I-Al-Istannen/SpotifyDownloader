from abc import ABC, abstractmethod


class Downloader(ABC):
    """An object able to download a video or music"""

    @abstractmethod
    def download(self, url: str, target_file: str):
        """Downloads an audio/video from the given source.

        :param url: The youtube url
        :param target_file: The file to save it to
        """
        pass

    @abstractmethod
    def can_download(self, url: str):
        """Checks if this Downloader can download the video/audio.

        :param url: The url to check
        """
        pass
    
    @abstractmethod
    def needs_conversion(self) -> bool:
        """Checks if this downloader downloads a mp3, or if the file needs conversion
        """
        pass
