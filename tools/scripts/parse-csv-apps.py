import codecs
import time

"""
Script that parses a SQL csv dump and creates a file with a
list of the EXPECTED app names.

"""

CODEC = 'ISO-8859-1'
SQL_CSV_FILENAME = 'kocsen_version_details_weather.csv'
OUTPUT_FILENAME = 'weather_app_names.txt'


def main():
    app_names = []
    f = codecs.open(SQL_CSV_FILENAME, 'r', CODEC)
    try:
        for line in f:
            # split on comma and get rid of the " literal
            split = [x.strip('"') for x in line.split(",")]
            if "com." in split[0]:
                parsed_date = "".join(build_date(split[2:4]))
                to_add = "-".join([split[0], split[1], parsed_date])
                to_add += ".apk"
                app_names.append(to_add)

        write(app_names)
    finally:
        f.close()


def build_date(raw_date):
    """
    Converts date to expected app name convention
    :param raw_date: Raw date string. Format: MMM DD YYYY
    i.e.  Nov 18 2015
    :return: Date string in format:           YYYY_MM_DD
    i.e.  2015_11_18
    """
    parsed_date = time.strptime(raw_date, "%b %d %Y")
    return time.strftime("%Y_%m_%d", parsed_date)


def write(app_names):
    """
    Given an array of the app names, write them to a file
    :param app_names:
    :return:
    """
    with open(OUTPUT_FILENAME, 'w') as f:
        f.writelines([x + "\n" for x in app_names])


if __name__ == "__main__":
    main()
