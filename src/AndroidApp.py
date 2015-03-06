__author__ = 'kocsen'

import xml.etree.ElementTree as ET


class AndroidApp():
    """
    Class representation of the app.
    Contains all sorts of infromationa bout the app including
    name and the parseable xml for the Manifest
    """

    def __init__(self, name, location_root):
        self.name = name
        self.location = location_root
        self.manifest_ET_root = ET.parse(location_root + '/app/AndroidManifest.xml').getroot()


