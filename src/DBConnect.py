__author__ = 'kocsen'

import logging
import time

import mysql.connector
from mysql.connector import errorcode


def write_app_data(data):
    config = {
        'user': '',
        'password': '',
        'host': '127.0.0.1',
        'database': 'AppFeatures',
    }

    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
        write(data)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist")
        else:
            logging.error(err)
    except Exception as e:
        logging.error(e.message)
    finally:
        cnx.close()


def write(data):
    """

    :param data:
    :return:
    """
    table_name = 'features'

    add_feature = ()


def get_version_id(app_package, version_code, raw_date):
    """

    :param app_package:
    :param version_code:
    :param raw_date:
    :return:
    """
    parsed_date = time.strftime("%b %d, %Y", time.strptime(raw_date, "%Y_%m_%d"))

    # Select id from version_details
    # WHERE
    # docid = app package,
    # details_appDetails_versionCode = version_code
    # details_appDetails_uploadDate = parsed_date // Maybe use %LIKE%
