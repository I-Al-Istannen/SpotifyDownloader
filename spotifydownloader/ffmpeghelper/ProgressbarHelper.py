import re
import subprocess
from io import TextIOWrapper
from typing import List

from util import ColorCodes as Color

__time_extractor = re.compile(r"time=([\d:.]+)")


def execute_with_bar(
      command_line: List[str], prefix: str,
      end="\r{prefix}: " + Color.GREEN + "Done" + Color.RESET + "\n") \
      -> List[str]:
    """Executes the command line and displays a progress bar for it.

    :return: The output value of the process
    :except: CalledProcessError if the exit code is non-zero
    """
    process: subprocess.Popen = subprocess.Popen(
          command_line,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT,
    )
    duration = "Unknown"

    lines = []

    while True:
        line = __read_until_carriage_return(process.stdout)
        if not line:
            break

        if line.endswith("\n"):
            lines = lines + line.splitlines()

        if "Duration:" in line:
            duration = __extract_duration(line)
        if "time" in line:
            time = __extract_time(line)
            if time:
                print(
                      "\r{prefix}: {time} / {duration}".format(
                            prefix=prefix, time=time.strip(), duration=duration
                      ),
                      end=""
                )
    process.wait()

    print("\r", " " * 50, end="")
    print(end.format(prefix=prefix), end="")

    if process.returncode != 0:
        output = "\n".join(lines)
        raise subprocess.CalledProcessError("Non-zero return code",
                                            process.returncode,
                                            output)

    return lines


def __extract_time(input_string: str) -> str:
    search = __time_extractor.search(input_string)
    return None if not search else search.group(1)


def __extract_duration(input_string: str) -> str:
    search = re.search(r"Duration: ([\d:.]+)", input_string)
    return None if not search else search.group(1)


def __read_until_carriage_return(input_stream: TextIOWrapper):
    temporary_string = ""
    while True:
        read_value = input_stream.read(1)
        if read_value == b"\r" or not read_value:
            return temporary_string
        # noinspection PyUnresolvedReferences
        temporary_string += read_value.decode()
