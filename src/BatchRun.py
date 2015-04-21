import logging

__author__ = 'kocsen'

import os
import subprocess
import shutil

from Driver import analyze_app


def batch(app_directory, decompiler_script):
    """

    :param app_directory:
    :param decompiler_script:
    :return:
    """
    app_directory = os.path.abspath(app_directory)
    decompiler_script = os.path.abspath(decompiler_script)
    logging.info("APPS:    " + app_directory)
    logging.info("DECOMPLR:" + decompiler_script)

    for original_apk_file in os.listdir(app_directory):
        logging.info("Decompiling and assessing " + os.path.basename(original_apk_file))
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



