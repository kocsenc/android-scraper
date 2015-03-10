#!/usr/bin/env python3
from AndroidApp import AndroidApp
from Commands.InternationalizationCommand import InternationalizationCommand
from Commands.AccountManagerUseCommand import AccountManagerUseCommand
from Commands.InternetUseCommand import InternetUseCommand
from Commands.SSLUseCommand import SSLUseCommand
from Commands.SharingCenterUseCommand import SharingCenterUseCommand


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
    internet_use = InternetUseCommand(current_app).execute()

    features = {
        'Internet': False,
        'Account Manager': False,
        'Use SSL': False,

        'Sharing (Sending)': False,
        'Internationalization': False
    }

    if internet_use:
        features['Internet'] = True
        # Check for account manager
        features['Account Manager'] = AccountManagerUseCommand(current_app).execute()
        # Check for SSL
        features['Use SSL'] = SSLUseCommand(current_app).execute()

    # Check for sharing
    features['Sharing (Sending)'] = SharingCenterUseCommand(current_app).execute()

    # Check for internationalization
    features['Internationalization'] = InternationalizationCommand(current_app).execute()

    logging.info("==== FINAL RESULTS ===")
    logging.info(features)


def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)2s ', level=logging.DEBUG);
    # logging.basicConfig(filename='android-scraper.log', level=logging.DEBUG)
    pass


if __name__ == "__main__":
    main()