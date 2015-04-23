#!/usr/bin/env python3
import logging

__author__ = 'kocsen'

import os
import subprocess
import shutil
import sys

from Driver import analyze_app


def main():
    logging.basicConfig(filename='out.log', level=logging.DEBUG)
    # USAGE:
    # python BatchRun.py /path/to/apps/ path/to/filename_w_appnames.txt path/to/decompiler.sh
    if len(sys.argv) == 4:
        # TODO: Add argument parsing
        batch(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        logging.info(
            "USAGE:\n  python BatchRun.py /path/to/apps/ path/to/filename_w_appnames.txt path/to/decompiler.sh")


def batch(app_directory, file_with_apknames, decompiler_script):
    """

    :param app_directory:
    :param decompiler_script:
    :return:
    """
    app_directory = os.path.abspath(app_directory)
    decompiler_script = os.path.abspath(decompiler_script)
    file_with_apknames = os.path.abspath(file_with_apknames)

    logging.info("APPS:    " + app_directory)
    logging.info("DECOMPLR:" + decompiler_script)
    logging.info("APPNAMES:" + file_with_apknames)

    # for original_apk_file in os.listdir(app_directory):
    for original_apk_file in get_apk_paths_given_filename(app_directory, file_with_apknames):
        logging.info("Decompiling and assessing " + os.path.basename(original_apk_file))
        apk_absolute_path = os.path.abspath(original_apk_file)
        abs_uncompressed_path = ""

        try:
            # Step 1 : decompile
            subprocess.call([decompiler_script, apk_absolute_path, subprocess.PIPE,
                             subprocess.DEVNULL])  # apkdecompiler.sh /apks/app.apk

            # Step 2 : get uncompressed directory created above and call analysis
            uncompressed_dir = os.path.basename(apk_absolute_path) + ".uncompressed"
            abs_uncompressed_path = os.path.join(os.path.dirname(decompiler_script),
                                                 uncompressed_dir)

            logging.info("Uncompressed Path: " + abs_uncompressed_path)
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
    with open(filename, 'r') as f:
        file_lines = f.readlines()

    return [os.path.join(apps_path, app_name) for app_name in file_lines]


if __name__ == "__main__":
    main()

