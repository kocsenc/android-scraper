__author__ = 'kocsen'

from Commands.Command import Command


class InternetUseCommand(Command):
    """
    Command that will check if app uses internet or not
    """

    def __init__(self, app):
        self.app = app

    def execute(self):
        pass
