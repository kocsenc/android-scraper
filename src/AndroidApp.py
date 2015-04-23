import fnmatch
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
        self.features = None  # This is where the result dict is stored

        # getting the source JAVA files
        self.code_source_location = os.path.join(location_root, "app/src")

        try:
            self.manifest_ET_root = ET.parse(location_root + '/app/AndroidManifest.xml').getroot()
        except FileNotFoundError:
            raise AppEmptyException("No Manifest Found")

        self.source_paths = []
        for root, subFolders, files in os.walk(self.code_source_location):
            for filename in files:
                self.source_paths.append(os.path.join(root, filename))

        # getting the source RES files and International files
        self.res_source_location = os.path.join(location_root, "app/res")
        self.res_paths = []
        self.lang_dirs = []
        for root, subFolders, files in os.walk(self.res_source_location):
            for filename in fnmatch.filter(files, '*.xml'):  # Matching XML
                self.res_paths.append(os.path.join(root, filename))

            # For matching internationalization
            if len(subFolders) > 0:
                for folder in subFolders:
                    if "values-" in folder and len(folder) == 9:
                        # Attempts to match
                        self.lang_dirs.append(folder)


class AppEmptyException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)