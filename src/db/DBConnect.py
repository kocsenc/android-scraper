__author__ = 'kocsen'

import logging
import time
import json

import mysql.connector
from mysql.connector import errorcode


"""
Used to write app feature data to a DB.

NOTE: This script is VERY specifically tied to the way data is modeled
in the existing Database AppDataDB and the naming conventions of the apk's.
"""


def write_app_data(app, config_filename):
    """

    :param app:
    :param config_filename:
    :return:
    """
    config = parse_config(config_filename)

    cnx = None
    try:
        # Establish a connection
        cnx = mysql.connector.connect(**config)
        write(app, cnx)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist")
        else:
            logging.error(err.message)
    finally:
        logging.debug("Conclude")
        # Close no matter what
        if cnx is not None:
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
    results = app.features
    table_name = 'features'

    split = app.name.split("-")
    if len(split) != 3:
        exit()

    logging.debug("getting foregin id")
    foreign_key_id = get_version_id(split[0], split[1], split[2], cnx)

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


def get_version_id(app_package, version_code, raw_date, cnx):
    """
    Gets the id of the app found inside of the `version_details` table
    in the Database. Used for adding a foreign key to the features table
    :param app_package:  The name, such as com.google.gmail (without the .apk ending)
    :param version_code: The version code used in the DB
    :param raw_date:     The date as appears on apk name in the format YYYY_MM_DD
    :return: id - as integer
    """
    cursor = cnx.cursor
    uid = None
    logging.debug("App package ", app_package)
    logging.debug("version code ", version_code)
    logging.debug("raw date ", raw_date)

    parsed_date = time.strftime("%b %d, %Y", time.strptime(raw_date, "%Y_%m_%d"))

    # Select id FROM version_details WHERE
    # docid = app package,
    # details_appDetails_versionCode = version_code
    # details_appDetails_uploadDate = parsed_date // Maybe use %LIKE%
    query = ("SELECT id FROM version_details WHERE "
             "docid = %s AND "
             "details_appDetails_versionCode = %s AND "
             "details_appDetails_uploadDate = %s")

    cursor.execute(query, (app_package, version_code, parsed_date))
    row = cursor.fetchone()
    uid = row[0]
    logging.debug("GOT ID!: ", str(uid))

    cursor.close()
    return uid


def parse_config(filename):
    try:
        # TODO: Validate configuration contents
        with open(filename) as f:
            config = json.load(f)

        return config
    except Exception as e:
        logging.error(e.message)
        exit(2)

