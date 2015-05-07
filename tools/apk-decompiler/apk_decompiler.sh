#!/usr/bin/env bash
# Author: Kocsen Chung
# BSD License
######
# Script that uses dex2jar, procyon and apktool to fully
# convert a apk file to readable source files.
######

# Setting Error Codes for Script
set -o errexit
set -o pipefail
set -o nounset

# Setting Directory Variables
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root="$(cd "$(dirname "${__dir}")" && pwd)/" 
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"

# APK Directory Variables
__apk_location="$1"
# Set the destination working location @ script location 
# Name: APKNAME.apk.uncompressed
__working_location="${__dir}/$(basename "${__apk_location}").uncompressed"

# Check to make sure all libraries are available
# dex2jar check
if [ ! -d ${__dir}/lib/dex2jar ]
then
   echo "dex2jar directory not found in ${__dir}. Make sure to name it dex2jar and put it in the lib dir"
   exit 1
fi
# procyon decompiler check
if [ ! -f ${__dir}/lib/procyon-decompiler.jar ]
then
    echo "procyon decompiler not found in ${__dir}. Make sure to name it procyon-decompiler.jar and put it in the lib dir"
    exit 1
fi
# apktool check
if [ ! -f ${__dir}/lib/apktool.jar ]
then
    echo "apktool jar not found in ${__dir}. Make sure to name it apktool.jar and put it in the lib dir"
    exit 1
fi


# Working directory creation
echo "All libraries found, creating working directory at ${__working_location}"
rm -r ${__working_location} || true
mkdir -p ${__working_location}
mkdir ${__working_location}/raw             # This is where the uncompressed APK goes
mkdir ${__working_location}/app             # This is where the uncompiled readable app goes

# Unzip the APK into /raw
unzip ${__apk_location} -d ${__working_location}/raw


function get_readable_assets
{ # Uses apk tool to get readable assets like the manifest file.
    java -jar ${__dir}/lib/apktool.jar d ${__apk_location} -f -o ${__working_location}/app
}

function get_java_source_from_apk
{ # Uses the apk file to get the .class files and then decompiles them
    # Run dex2jar outputting to raw/dex2jar.jar
    ${__dir}/lib/dex2jar/d2j-dex2jar.sh -o ${__working_location}/raw/dex2jar.jar --force ${__working_location}/raw/classes.dex

    # Run decompiler outputting to src/  TIMEOUT 1Hour
    mac=Darwin
    linux=Linux
    if [ $(uname) == ${mac} ]
    then
        # if on mac, cannot use timeout command. So just execute
        java -jar ${__dir}/lib/procyon-decompiler.jar -jar ${__working_location}/raw/dex2jar.jar -o ${__working_location}/app/src
    else
        timeout 1h java -jar ${__dir}/lib/procyon-decompiler.jar -jar ${__working_location}/raw/dex2jar.jar -o ${__working_location}/app/src
    fi
}

get_readable_assets
#mkdir ${__working_location}/app/src  # This is where the uncompiled .java code goes
get_java_source_from_apk

# Cleanup
# Remove raw directory
rm -r ${__working_location}/raw || true
echo "Successfully decompiled $(basename "${__apk_location}") to ${__working_location}/app"
