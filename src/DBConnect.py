__author__ = 'kocsen'

import logging
import time

import mysql.connector
from mysql.connector import errorcode


"""
Used to write app feature data to a DB.

NOTE: This script is VERY specifically tied to the way data is modeled
in the existing Database AppDataDB and the naming conventions of the apk's.
"""


def write_app_data(app):
    config = {
        'user': '',
        'password': '',
        'host': '127.0.0.1',
        'database': 'AppFeatures',
    }

    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
        write(app, cnx)
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


def write(app, cnx):
    """
    Given an app and a SQL connection, write the app features
    into the feature table.
    :param app: The Android Application object with the data
    :param cnx: SQL Connection
    :return:
    """
    cursor = cnx.cursor()
    try:
        results = app.features
        table_name = 'features'

        split = app.name.split("-")
        if len(split) != 3:
            exit()

        foreign_key_id = get_version_id(split[0], split[1], split[2])

        add_feature_query = ("INSERT INTO version_features "
                             "(app_version_id, internet, account_manager, uses_ssl, sharing_sending, translation) "
                             "VALUES (%s, %s, %s, %s, %s, %s)")

        feature_data = (
            foreign_key_id,
            results['Internet'],
            results['Account Manager'],
            results['Use SSL'],
            results['Sharing-Sending'],
            results['Internationalization']
        )

        cursor.execute(add_feature_query, feature_data)

        # commit & actually save
        cnx.commit()
    finally:
        cursor.close()


def get_version_id(app_package, version_code, raw_date):
    """
    Gets the id of the app found inside of the `version_details` table
    in the Database. Used for adding a foreign key to the features table
    :param app_package:  The name, such as com.google.Gmail (without the apk)
    :param version_code: The version code used in the DB
    :param raw_date:     The date as appears on apk name in the format YYYY_MM_DD
    :return: id - as integer
    """
    parsed_date = time.strftime("%b %d, %Y", time.strptime(raw_date, "%Y_%m_%d"))
    id = 0
    # Select id from version_details
    # WHERE
    # docid = app package,
    # details_appDetails_versionCode = version_code
    # details_appDetails_uploadDate = parsed_date // Maybe use %LIKE%
    return id