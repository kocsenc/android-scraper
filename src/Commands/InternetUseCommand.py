import logging

__author__ = 'kocsen'

from Commands.Command import Command


class InternetUseCommand(Command):
    """
    Command that will check if app uses internet or not
    """

    def __init__(self, app):
        self.app = app

    def execute(self):
        logging.info("Running INTERNET USE COMMAND")
        manifest = self.app.manifest_ET_root
        permissions = manifest.findall("uses-permission")

        INTERNET_PERMISSION = "android.permission.INTERNET"
        key = '{http://schemas.android.com/apk/res/android}name'

        for permission in permissions:
            if permission.attrib[key] == INTERNET_PERMISSION:
                logging.debug("Found Internet Use")
                return True

        return False

