import os
import subprocess

from downloader.DownloaderBase import Downloader


class YoutubeDlDownloader(Downloader):
    """A downloader using youtube-dl."""

    def download(self, url: str, target_file: str):
        command = [
            "youtube-dl",
            "--output", target_file.replace(".mp3", "") + ".%(ext)s",
            "--extract-audio", "--audio-format", "mp3",
            url
        ]
        subprocess.call(command)

        # Youtube-DL appends the mp3 extension for us
        os.rename(target_file + ".mp3", target_file)
        pass

    def can_download(self, url: str):
        return "youtube.com" in url
