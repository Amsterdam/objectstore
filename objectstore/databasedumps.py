"""
We use the objectstore to get the latest and greatest of
database dump

EXAXMPLE:
---------

    assert os.getenv('HANDELSREGISTER_OBJECTSTORE_PASSWORD')

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

import datetime
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

    date = f"{datetime.datetime.now():%Y%m%d}"

    objectstore.put_object(
        connection,
        f'{container}',
        f'database.{ENV}.{date}.dump',
        # contents=dump.read(),
        contents=dump,
        content_type='application/octet-stream')


def download_database(connection, container: str, target: str=""):
    """
    Download database dump
    """

    meta_data = objectstore.get_full_container_list(
        connection, container, prefix='database')

    options = []

    for o_info in meta_data:
        expected_file = f'database.{ENV}'
        if o_info['name'].startswith(expected_file):
            dt = dateparser.parse(o_info['last_modified'])
            now = datetime.datetime.now()

            delta = now - dt

            log.debug('AGE: %d %s', delta.days, expected_file)

            if delta.days > 20:
                objectstore.delete_object(connection, container, o_info)

            options.append((dt, o_info))

        options.sort()
        newest = options[-1][1]

        log.debug('Downloading: %s', (expected_file))

        new_data = objectstore.get_object(connection, newest, container)

        # save output to file!
        target_file = os.path.join(target, expected_file)
        with open(target_file, 'wb') as outputzip:
            outputzip.write(new_data)


def run(connection):
    """
    Parse arguments and start upload/download
    """

    parser = argparse.ArgumentParser(description="""
    Process database dumps.

    Either download of upload a dump file to the objectstore.

    downloads the latest dump and uploads with envronment and date
    into given container destination
    """)

    parser.add_argument(
        'location',
        nargs=1,
        default=f'{DUMPFOLDER}/database.{ENV}.dump',
        help="Dump file location")

    parser.add_argument(
        'objectstore',
        nargs=1,
        default=f'{DUMPFOLDER}/database.{ENV}.dump',
        help="Dump file objectstore location")

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

    args = parser.parse_args()

    if args.download:
        download_database(connection, args.objectstore[0], args.location[0])
    elif args.upload:
        upload_database(connection, args.objectstore[0], args.location[0])
    else:
        parser.print_help()


if __name__ == '__main__':
    connection = objectstore.get_connection()
    run(connection)
