from abc import ABC, abstractmethod


class Converter(ABC):
    """A converter to convert audio / video files."""

    @abstractmethod
    def can_convert(self, file: str) -> bool:
        """Checks if this converter can convert the given file."""
        pass

    @abstractmethod
    def convert(self, input_file: str, output_file: str):
        """Converts the given input file and stores the result in the output one.


        :param input_file: The path to the file to read from
        :param output_file: The path to the file to write to
        """
        pass

    @abstractmethod
    def name(self):
        pass
