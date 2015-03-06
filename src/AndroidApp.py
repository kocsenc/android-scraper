import os

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
        self.code_source_location = os.path.join(location_root, "app/src")
        self.manifest_ET_root = ET.parse(location_root + '/app/AndroidManifest.xml').getroot()

        self.source_paths = []
        for root, subFolders, files in os.walk(self.code_source_location):
            for filename in files:
                self.source_paths.append(os.path.join(root, filename))



