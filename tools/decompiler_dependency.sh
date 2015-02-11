#!/usr/bin/env bash
# Author: Kocsen Chung
# Gets libraries needed for the apk conversion script

# Setting Error Codes for Script
set -o errexit
set -o pipefail
set -o nounset

# Setting Directory Variables
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root="$(cd "$(dirname "${__dir}")" && pwd)/" 
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"
__lib="${__dir}/lib"

# URLS for libraries
# dex2jar
dexjar_url="https://dex2jar.googlecode.com/files/dex2jar-0.0.9.15.zip"
dexjar_sha="cc9366836d576ce22a18de8f214368636db9fcba"
__dexjar_zip="${__lib}/$(basename ${dexjar_url})"
# apk tools
apktools_url="https://"
# procyon decompiler
decompiler_url=""

function get_dex2jar
{ # Gets and checks integrity of dex2jar
	echo "Getting dex2jar library version: $(basename ${__dexjar_zip})"
	wget ${dexjar_url} -P ${__lib}

	# Checksum check
	downloaded_raw_sha="$(openssl sha1 ${__dexjar_zip})"
	downloaded_sha=${downloaded_raw_sha##*= }
	# If the shas don't match, exit with error code.
 	if [ "${dexjar_sha}" != "${downloaded_sha}" ]; then
		echo "SHA doesen't match. try again"
		exit 1
	fi

	# Unzip and rename to dex2jar, get rid of zip.
	echo "unzipping"
	unzip -qq -o ${__dexjar_zip} -d ${__lib}
	rm ${__dexjar_zip}
	
	
}

function get_apktools
{ # gets apk tools and checks integrity of download
	echo "Getting apktools library version: $(basename ${apktools_url})"


}



get_dex2jar
