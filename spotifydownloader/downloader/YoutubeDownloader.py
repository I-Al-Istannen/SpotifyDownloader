from pafy import pafy
from pafy.backend_shared import BasePafy, BaseStream

from downloader.DownloaderBase import Downloader


class YoutubeDownloader(Downloader):
    def can_download(self, url: str):
        return "youtube.com" in url

    def download(self, url: str, target_file: str):
        video_information: BasePafy = pafy.new(url)

        print("Fetching audio for '{0}'".format(video_information.title))

        best_audio: BaseStream = video_information.getbestaudio()

        best_audio.download(filepath=target_file)

        print()

    def needs_conversion(self):
        return True