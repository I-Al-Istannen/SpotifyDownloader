import shlex
from subprocess import check_output
from typing import Any
from urllib.request import urlopen

import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC

from metadata import Metadata
from metadata.injector.Base import MetadataInjector


class MutagenMetadataInjector(MetadataInjector):
    def can_inject(self, file: str):
        return "audio/mpeg" in check_output(
              shlex.split("file -i \"{0}\"".format(file))
        ).decode()

    def inject(self, file: str, metadata: Metadata):
        try:
            meta = EasyID3(file)
        except mutagen.id3.ID3NoHeaderError:
            meta = mutagen.File(file, easy=True)
            meta.add_tags()

        self.__add(meta, "artist", metadata.artists)
        self.__add(meta, "album", metadata.album)
        self.__add(meta, "title", metadata.title)
        self.__add(
              meta, "tracknumber",
              "{0}/{1}".format(metadata.track_number,
                               metadata.total_track_number)
        )
        self.__add(meta, "originaldate", metadata.release_date)
        self.__add(meta, "genre", metadata.genre)
        self.__add(meta, "date", metadata.release_date)

        meta.save()

        with urlopen(metadata.album_art_url, timeout=30) as response:
            cover_data = response.read()
            id3 = ID3(file)
            id3["APIC"] = APIC(encoding=3, desc=u"Frontcover", type=3,
                               data=cover_data)
            id3.save()

    @staticmethod
    def __add(audio_file: EasyID3, key: str, value: Any):
        if value:
            audio_file[key] = value
