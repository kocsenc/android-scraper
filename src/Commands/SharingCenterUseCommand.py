__author__ = 'kocsen'

import logging
from os.path import basename

from Commands.Command import Command


class SharingCenterUseCommand(Command):
    """
    Command that will check if app is using sharing!
    """

    def __init__(self, app):
        self.app = app

    def execute(self):
        logging.info("Running Sharing Use command")

        confidence_points = 0
        sharing_files = []

        for file_name in self.app.source_paths:
            # logging.debug("Reading file %s", basename(file_name))
            with open(file_name, 'r') as f:
                try:
                    for line in f.readlines():
                        if "Intent.ACTION_SEND" in line:
                            sharing_files.append(file_name)
                            confidence_points += 1
                            logging.info("found %d instance of Sharing in %s", confidence_points,
                                         basename(file_name))

                except UnicodeDecodeError:
                    logging.warning("Unicode error: skipping %s", basename(file_name))

        if confidence_points > 2:
            return True
        else:
            logging.info("Found no sharing feature.")
            return False