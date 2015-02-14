# Setup Dependencies - PYTHON 3
# Downloads dependencies and gets them ready for stuff
import shutil

__author__ = "Kocsen Chung"

import os
import zipfile
import urllib.request

# # Directory Variables ##
__DIR = os.path.dirname(os.path.realpath(__file__))
lib_dir = __DIR + "/lib"

# URLS for libraries
dex2jar_url = "https://dex2jar.googlecode.com/files/dex2jar-0.0.9.15.zip"
dex2jar_zip_destination = lib_dir + "/dex2jar.zip"
apktools_url = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.0.0rc4.jar"
apktools_destination = lib_dir + "/apktool.jar"
decompiler_url = "https://bitbucket.org/mstrobel/procyon/downloads/procyon-decompiler-0.5.28.jar"
decompiler_destination = lib_dir + "/procyon-decompiler.jar"


def main():
    create_lib_dir()

    # ############
    # # Dex2Jar
    # ############
    print("Downloading dex2jar")
    urllib.request.urlretrieve(dex2jar_url, dex2jar_zip_destination)
    extract(dex2jar_zip_destination)
    zip_name = os.path.basename(dex2jar_url).split(".zip")[0]
    # Rename dex2jar.#.#.# to dex2jar
    os.rename(lib_dir + "/" + zip_name, lib_dir + "/dex2jar")
    # Remove the zip
    os.remove(dex2jar_zip_destination)


    # ############
    # # apktools
    #############
    print("Downloading apktools")
    urllib.request.urlretrieve(apktools_url, apktools_destination)

    #############
    ## apktools
    #############
    print("Downloading decompiler")
    urllib.request.urlretrieve(decompiler_url, decompiler_destination)


def extract(path_to_zip):
    """ Extract a zip """
    print("Extracting " + path_to_zip)
    with zipfile.ZipFile(path_to_zip, "r") as z:
        z.extractall(lib_dir)


def create_lib_dir():
    """
    Creates a /lib directory in the working directory if it doesent already exist,
    if dir exists, deletes it and makes a new one.
    """
    if os.path.exists(lib_dir):
        print("Existing lib directory is being deleted...")
        shutil.rmtree(lib_dir)
    print("Creating new lib directory")
    os.makedirs(lib_dir)


if __name__ == "__main__":
    main()