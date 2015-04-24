#!/usr/bin/env python3
import logging

from AndroidApp import AppEmptyException


__author__ = 'kocsen'

import os
import subprocess
import shutil
import sys

from Driver import analyze_app


def main():
    """
    Sets up basic logging config.
    Sets logging output to `out.batch.log`
    Runs the batch system with the arguments.
    ARGS:
    - Path to where all the applications are located
    - Path to the file which has the application names to run on
        Note: This file has to have only the names, not the paths.
    - Path to the decompiler script
    """
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)2s ', level=logging.DEBUG,
                        filename='out.batch.log')

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
    Sets all ABSOLUTE paths to every parameter to avoid confusion.
    Gathers the

    :param app_directory:       The directory path where all apps are located
    :param file_with_apknames:  The file path for list of apps to batch analyze
    :param decompiler_script:   The path to the decompiler script
    """
    app_directory = os.path.abspath(app_directory)
    decompiler_script = os.path.abspath(decompiler_script)
    file_with_apknames = os.path.abspath(file_with_apknames)

    logging.info("* BATCH RUN CONFIG *")
    logging.info("APPS:    " + app_directory)
    logging.info("DECOMPLR:" + decompiler_script)
    logging.info("APPNAMES:" + file_with_apknames)
    logging.info("********************")

    # Used to keep count of the app batch number.
    count = 1
    for original_apk_file in get_apk_paths_given_filename(app_directory, file_with_apknames):
        logging.info("*************** Starting #%d ***************", count)
        logging.info("Assessing: \t%s", os.path.basename(original_apk_file).rstrip())
        apk_absolute_path = os.path.abspath(original_apk_file)
        apk_name = os.path.basename(apk_absolute_path).rstrip()
        uncompressed_apk_name = apk_name + ".uncompressed"
        uncompressed_apk_absolute_path = os.path.join(os.path.dirname(decompiler_script),
                                                      uncompressed_apk_name)
        try:
            # Step 1 : decompile
            logging.info("\tDecompiling...")
            subprocess.call([decompiler_script, apk_absolute_path],
                            stdout=subprocess.DEVNULL)  # apkdecompiler.sh /apks/app.apk

            # Step 2 : call analysis on uncompressed apk
            logging.info("Uncompressed Path: " + uncompressed_apk_absolute_path)
            analyze_app(uncompressed_apk_absolute_path)
        except AppEmptyException as e:
            logging.error("It seems the app is empty, skipping.")
        finally:
            # Hopefully the uncompressed app has been analyzed, now remove it
            if os.path.isdir(uncompressed_apk_absolute_path) and os.path.exists(uncompressed_apk_absolute_path):
                logging.info("Deleting uncompressed directory")
                shutil.rmtree(uncompressed_apk_absolute_path)
            logging.info("*************** DONE ***************\n\n")
            count += 1


def get_apk_paths_given_filename(apps_path, filename):
    """
    Reads the file filename and creates a list of absolute paths
    for the actual absolute locations of the apk's.
    
    :param apps_path: The path to where all the apks are located
    :param filename:  The filename that has the list of all the app names
    :return: a list of the absolute paths for the actual locations of the apk's
    """
    with open(filename, 'r') as f:
        file_lines = f.readlines()

    return [os.path.join(apps_path, app_name) for app_name in file_lines]


if __name__ == "__main__":
    main()

