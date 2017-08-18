import re
import shlex

from conversion.ConverterBase import Converter
from ffmpeghelper import ProgressbarHelper
from util import ColorCodes


class FfmpegConverter(Converter):
    """A converter using FFMPEG to do the conversion."""

    def __init__(self):
        self.__command_line = "ffmpeg -y -i \"{input}\" -vn -ar 44100" \
                              " -ac 2 -b:a 192k -f mp3 \"{output}\""
        self.__time_extractor = re.compile(r"time=([\d:.]+)")

    def can_convert(self, file: str) -> bool:
        # FFMPEG can convert *anything*
        return True

    def name(self):
        return "FFMPEG"

    def convert(self, input_file: str, output_file: str):
        command_line = self.__command_line.format(
              input=input_file, output=output_file
        )

        ProgressbarHelper.execute_with_bar(shlex.split(command_line),
                                           ColorCodes.BLUE + "Conversion"
                                           + ColorCodes.RESET)
