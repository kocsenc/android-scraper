__author__ = 'kocsen'

import logging
from os.path import basename

from Commands.Command import Command


class AccountManagerUseCommand(Command):
    """
    Command that will check if app uses account manager
    """

    def __init__(self, app):
        self.app = app

    def execute(self):
        logging.info("Running ACCOUNT MANAGER USE command")

        confidence_points = 0
        files_with_account_manager = []
        for file_name in self.app.source_paths:
            logging.debug("Reading file %s", basename(file_name))
            with open(file_name, 'r') as f:
                try:
                    for line in f.readlines():
                        if "AccountManager" in line:
                            files_with_account_manager.append(file_name)
                            confidence_points += 1
                            logging.info("found %d instance of Account Manager in %s", confidence_points,
                                         basename(file_name))

                except UnicodeDecodeError:
                    logging.warning("Unicode error: skipping %s", basename(file_name))

        if confidence_points > 2:
            return True
        else:
            return False