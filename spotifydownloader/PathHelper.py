import os
from re import sub


def sanitize_path(name: str):
    """Sanitizes a path to remove all invalid chars"""

    return sub(pattern=r"[^a-zA-Z\d_\- ]", repl="", string=name)


def get_tmp_file(name: str):
    """A temporary file with the given name.

    The name will be sanitized first.
    """
    return os.path.join(__get_and_create_tmp_dir(), sanitize_path(name))


def __get_and_create_tmp_dir():
    path = "/tmp/SpotifyDownloader"

    if not os.path.exists(path):
        os.mkdir(path)

    return path


def get_output_file(name: str, folder: str):
    """Returns the path to a file with the given name in the folder.

    Will create the folder if needed.
    """
    if not os.path.exists(folder):
        os.mkdir(folder)

    return os.path.join(folder, sanitize_path(name) + ".mp3")
