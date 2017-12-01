"""
We use the objectstore to get the latest and greatest of database dump
assert os.getenv('HANDELSREGISTER_OBJECTSTORE_PASSWORD')

EXAXMPLE:
---------

    ENV = os.getenv('ENVIRONMENT', 'ACCEPTANCE')
    OBJECTSTORE_LOCAL = os.getenv('OBJECTSTORE_LOCAL', '')

    OBJECTSTORE = dict(
        VERSION='2.0',
        AUTHURL='https://identity.stack.cloudvps.com/v2.0',
        TENANT_NAME='BGE000081_Handelsregister',
        TENANT_ID='0efc828b88584759893253f563b35f9b',
        USER=os.getenv('OBJECTSTORE_USER', 'handelsregister'),
        PASSWORD=os.getenv('HANDELSREGISTER_OBJECTSTORE_PASSWORD'),
        REGION_NAME='NL',
    )


    connection = objectstore.get_connection(OBJECTSTORE)

    use this connection in below methods
"""

import os
import datetime
import argparse
import logging

# import datetime
# import connection
import objectstore
from dateutil import parser as dateparser


log = logging.getLogger(__name__)

DUMPFOLDER = '/tmp/backups/'
ENV = os.getenv('ENVIRONMENT', 'ACCEPTANCE')


def upload_database(connection, container: str, location: str):

    if location:
        dump = open(location, 'rb')
    else:
        dump = open(f'{DUMPFOLDER}/database.dump', 'rb')

    objectstore.put_object(
        connection,
        f'{container}/database',
        f'database.{ENV}.dump',
        # contents=dump.read(),
        contents=dump,
        content_type='application/octet-stream')


def download_database(connection, container: str, ):
    """
    Download database dump
    """

    meta_data = objectstore.get_full_container_list(
        connection, container, prefix='database')

    for o_info in meta_data:
        expected_file = f'database.{ENV}.dump'
        if o_info['name'].endswith(expected_file):
            dt = dateparser.parse(o_info['last_modified'])
            now = datetime.datetime.now()

            delta = now - dt

            log.debug('AGE: %d %s', delta.days, expected_file)

            log.debug('Downloading: %s', (expected_file))

            new_data = objectstore.get_object(
                connection, o_info, container)

        # save output to file!
        with open('data/{}'.format(expected_file), 'wb') as outputzip:
            outputzip.write(new_data)


def run(connection):

    parser = argparse.ArgumentParser(description='Process database dumps.')

    parser.add_argument(
        'location',
        nargs='*',
        default=f'{DUMPFOLDER}/database.{ENV}.dump',
        help="Dump file location")

    parser.add_argument(
        '--download-db',
        action='store_true',
        dest='download',
        default=False,
        help='Download db')

    parser.add_argument(
        '--upload-db',
        action='store_true',
        dest='upload',
        default=False,
        help='Upload db')

    parser.add_argument(
        '--container',
        action='store_true',
        dest='container',
        default=False,
        help='Upload db')

    parser.config()

    if parser.download:
        download_database(connection, parser.container, parser.location)
    if parser.upload:
        upload_database(connection, parser.container, parser.location)


if __name__ == '__main__':
    run()
