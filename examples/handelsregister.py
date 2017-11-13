"""
We use the objectstore to get the latest and greatest of the mks dump
"""
import os
import logging

import datetime

from dateutil import parser

import objectstore

log = logging.getLogger('objectstore')

assert os.getenv('HANDELSREGISTER_OBJECTSTORE_PASSWORD')

OBJECTSTORE = dict(
    VERSION='2.0',
    AUTHURL='https://identity.stack.cloudvps.com/v2.0',
    TENANT_NAME='BGE000081_Handelsregister',
    TENANT_ID='0efc828b88584759893253f563b35f9b',
    USER=os.getenv('OBJECTSTORE_USER', 'handelsregister'),
    PASSWORD=os.getenv('HANDELSREGISTER_OBJECTSTORE_PASSWORD'),
    REGION_NAME='NL',
)

DATA_DIR = 'data/'

EXPECTED_FILES = [
    'kvkadr.sql.gz',
    'kvkbeshdn.sql.gz',
    'kvkhdn.sql.gz',
    'kvkmac.sql.gz',
    'kvkprs.sql.gz',
    'kvkprsash.sql.gz',
    'kvkves.sql.gz',
    'kvkveshis.sql.gz',
]

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)


handelsregister_conn = objectstore.get_connection(OBJECTSTORE)


def download_files(file_list):
    """Download the latest data. """
    for _, source_data_file in file_list:
        sql_gz_name = source_data_file['name'].split('/')[-1]
        msg = 'Downloading: %s' % (sql_gz_name)
        log.debug(msg)

        new_data = objectstore.get_object(
            handelsregister_conn, source_data_file, 'handelsregister')

        # save output to file!
        with open('data/{}'.format(sql_gz_name), 'wb') as outputzip:
            outputzip.write(new_data)


def get_latest_hr_files():
    """
    Download the expected files provided by mks / kpn
    """
    file_list = []

    meta_data = objectstore.get_full_container_list(
        handelsregister_conn, 'handelsregister')

    for o_info in meta_data:
        for expected_file in EXPECTED_FILES:
            if not o_info['name'].endswith(expected_file):
                continue

            dt = parser.parse(o_info['last_modified'])
            now = datetime.datetime.now()

            delta = now - dt

            log.debug('AGE: %d %s', delta.days, expected_file)

            if delta.days > 10:
                log.error('DELEVERY IMPORTED FILES ARE TOO OLD!')
                raise ValueError

            log.debug('%s %s', expected_file, dt)
            file_list.append((dt, o_info))

    download_files(file_list)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_latest_hr_files()
