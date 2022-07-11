#!/usr/bin/env python3
"""Spotify Extender (spotex)

Usage:
    spotex.py config
    spotex.py playlist create
    spotex.py test

Options:
    -h --help  Show this screen.
    --version  Show version.
"""
import os

from docopt import docopt
from InquirerPy import inquirer
import dotenv

SPOTEX_DIR_PATH = os.getcwd()
DOTENV_PATH = f"{SPOTEX_DIR_PATH}/.env"

dotenv.load_dotenv(DOTENV_PATH)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", None)


def _abort(message):
    print(message)
    exit()


def config():
    try:
        spotify_client_id = inquirer.text( # type: ignore
            message=f"Your Spotify client ID{' (blank to use current ID)' if SPOTIFY_CLIENT_ID is not None else ''}: ",
            filter=lambda text: text.replace('\n', ''),
            validate=lambda text: text or SPOTIFY_CLIENT_ID
        ).execute()
    except KeyboardInterrupt:
        _abort("Operation cancelled.")

    dotenv.set_key(dotenv_path=DOTENV_PATH, key_to_set="SPOTIFY_CLIENT_ID", value_to_set=spotify_client_id)

    try:
        spotify_client_secret = inquirer.secret( # type: ignore
            message=f"Your Spotify client secret{' (blank to use current secret)' if SPOTIFY_CLIENT_ID is not None else ''}: ",
            transformer=lambda _: "[hidden]",
            filter=lambda text: text.replace('\n', ''),
            validate=lambda text: text or SPOTIFY_CLIENT_SECRET
        ).execute()
    except KeyboardInterrupt:
        _abort("Operation cancelled.")

    dotenv.set_key(dotenv_path=DOTENV_PATH, key_to_set="SPOTIFY_CLIENT_SECRET", value_to_set=spotify_client_secret)


def main():
    arguments = docopt(__doc__, version="spotex 0.1") # type: ignore
    if not arguments:
        print(__doc__)

    if arguments.get("config"):
        config()

    if arguments.get("test"):
        print("test")


if __name__ == "__main__":
    main()
