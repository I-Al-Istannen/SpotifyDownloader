from argparse import ArgumentParser


def get_argument_parser() -> ArgumentParser:
    parser = ArgumentParser("SpotifyDownloader")
    parser.add_argument("-p", "--playlist", metavar="playlist-name")
    parser.add_argument("-d", "--download-playlist", dest="download_playlist",
                        metavar="playlist-url")
    parser.add_argument("-o", "--output-folder", dest="output_folder",
                        metavar="output-folder")
    parser.add_argument("-r", "--redownload", dest="redownload_if_exists",
                        metavar="redownload-if-exists")

    return parser
