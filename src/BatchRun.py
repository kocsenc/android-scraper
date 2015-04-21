#!/usr/bin/env python3
import logging

__author__ = 'kocsen'

import os
import subprocess
import shutil
import sys

from Driver import analyze_app


def main():
    batch(sys.argv[1], sys.argv[2], sys.argv[3])


def batch(app_directory, file_with_apknames, decompiler_script):
    """

    :param app_directory:
    :param decompiler_script:
    :return:
    """
    app_directory = os.path.abspath(app_directory)
    decompiler_script = os.path.abspath(decompiler_script)
    print("APPS:    " + app_directory)
    print("DECOMPLR:" + decompiler_script)

    # for original_apk_file in os.listdir(app_directory):
    for original_apk_file in get_apk_paths_given_filename(app_directory, file_with_apknames):
        print("Decompiling and assessing " + os.path.basename(original_apk_file))
        if False:  # TEMPORARY TODO: remove
            try:
                apk_absolute_path = os.path.abspath(original_apk_file)

                # Step 1 : decompile
                command = decompiler_script + " " + apk_absolute_path
                subprocess.call([command])  # apkdecompiler.sh /apks/app.apk

                # Step 2 : get uncompressed directory created above and call analysis
                abs_uncompressed_path = os.path.dirname(decompiler_script)
                analyze_app(abs_uncompressed_path)
            finally:
                # Hopefully the uncompressed app has been analyzed, now remove it

                if os.path.isdir(abs_uncompressed_path) and os.path.exists(abs_uncompressed_path):
                    logging.info("Deleting uncompressed directory")
                    shutil.rmtree(abs_uncompressed_path)


def get_apk_paths_given_filename(apps_path, filename):
    """
    :param apps_path: The path to where all the apks are located
    :param filename:  The filename that has the list of all the app names
    :return: a list of the absolute paths for the actual locations of the apk's
    """
    with open(filename, 'w') as f:
        file_lines = f.readlines()

    return [os.path.join(apps_path, app_name) for app_name in file_lines]


if __name__ == "__main__":
    main()

