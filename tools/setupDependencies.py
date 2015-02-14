# Setup Dependencies - PYTHON 3
# Downloads dependencies and gets them ready for stuff

__author__ = "Kocsen Chung"

import os
import zipfile
import urllib.request

# # Directory Variables ##
__DIR = os.path.dirname(os.path.realpath(__file__))
lib_dir = __DIR + "/lib"

# URLS for libraries
dex2jar_url = "https://dex2jar.googlecode.com/files/dex2jar-0.0.9.15.zip"
dex2jar_dir = lib_dir + "/dex2jar.zip"


def main():
    create_lib_dir()

    urllib.request.urlretrieve(dex2jar_url, dex2jar_dir)
    extract(dex2jar_dir)


def extract(path_to_zip):
    print("Extracting " + path_to_zip)
    with zipfile.ZipFile(path_to_zip, "r") as z:
        z.extractall(lib_dir)

    zip_name = os.path.basename(dex2jar_url).split(".zip")[0]
    # Rename dex2jar.#.#.# to dex2jar
    os.rename(lib_dir + "/" + zip_name, lib_dir + "/dex2jar")
    # Remove the zip
    os.remove(dex2jar_dir)


def create_lib_dir():
    """
    Creates a /lib directory in the working directory if it doesent already exist,
    if dir exists, deletes it and makes a new one.
    """
    if os.path.exists(lib_dir):
        print("Existing lib directory is being deleted...")
        os.rmdir(lib_dir)
    print("Creating new lib directory")
    os.makedirs(lib_dir)


if __name__ == "__main__":
    main()