#!/usr/bin/env python3
from AndroidApp import AndroidApp


__author__ = 'kocsen'

import sys
import logging
from os.path import *


def main():
    setup_logging()

    arguments = sys.argv
    if len(arguments) < 2:
        logging.error("Need more arguments")
        logging.info("USAGE: ./Driver.py path/to/uncompressedAPK")
        exit()

    # Carry on with app preconditions
    path = arguments[1]
    app_name = basename(path).split(".")[0]
    logging.info("Starting Android Scraper")
    logging.info("App name: %s", app_name)
    logging.info(abspath(path))

    current_app = AndroidApp(app_name, abspath(path))


def setup_logging():
    logging.basicConfig(level=logging.DEBUG);
    # logging.basicConfig(filename='android-scraper.log', level=logging.DEBUG)
    pass


if __name__ == "__main__":
    main()