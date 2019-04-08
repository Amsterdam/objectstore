import argparse
import datetime
import glob
import logging
import objectstore
from databasedumps import upload_database
import os
import subprocess
import sys

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DEFAULT_TMPFOLDER = '/tmp'


class Archiver(object):
    """
    Archive specified tables.

    - Dumps postgres sql copy format - data
    - Dumps schema
    - zip the resulting archives
    - upload zip file to objectstore
    - cleanup tmp files
    - truncate tables IF ONLY everything was successfull!

    TODO:
        drop emptied partitions

    NOTE:
    avoid version conflict because we dump in copy format.
    """
    def make_stamp(self, dt=None):
        ts = dt if dt else datetime.datetime.now()
        return ts.strftime("%Y%m%d-%H%M%S")

    def __init__(self, tmp_folder=None):
        self.tmp = tmp_folder if tmp_folder else DEFAULT_TMPFOLDER
        self.stamp = self.make_stamp()

    def cmd(self, cmd, filename=None):
        log.info(f'Cmd: {cmd}, outputfile: {filename}')
        try:
            if filename:
                with open(filename, 'wb') as outfile:
                    p = subprocess.Popen(cmd, stdout=outfile)
                    p.wait()
            else:
                p = subprocess.Popen(cmd)
                p.wait()
            log.info(f'Ret. code: {p.returncode}')
            return p.returncode
        except Exception as ex:
            log.error(ex)
            # import traceback
            # print(traceback.format_exc())
            return -1

    def make_archive(self):
        archive = f'{self.tmp}/archive-{self.stamp}.zip'
        cmd = [
            'zip',
            archive,
        ]
        cmd.extend(glob.glob(f'{self.tmp}/*{self.stamp}.sql'))
        return archive if self.cmd(cmd) == 0 else None

    def cleanup_tmpfiles(self):
        cmd = [
            'rm',
            '-rf'
        ]
        cmd.extend(glob.glob(f'{self.tmp}/*{self.stamp}.sql'))
        cmd.extend(glob.glob(f'{self.tmp}/*{self.stamp}.zip'))
        return self.cmd(cmd)

    def archive_table(self, tbl):
        error_count = 0
        cmd = [
            'pg_dump',
            '--data-only',      # only data
            '--format=p',       # plain sql txt output
            '-b',               # include blobs
            '-t',               # single table
            f'{tbl}'
        ]
        outfile = f'{self.tmp}/{tbl}-data-{self.stamp}.sql'
        if self.cmd(cmd, outfile) != 0:
            error_count += 1

        cmd = [
            'pg_dump',
            '--schema-only',    # only schema
            '-t',               # single table
            f'{tbl}'
        ]
        outfile = f'{self.tmp}/{tbl}-schema-{self.stamp}.sql'
        if self.cmd(cmd, outfile) != 0:
            error_count += 1
        return error_count

    def truncate_tables(self, tbls):
        tbl_list = ','.join(tbls)
        cmd = [
            'psql',
            '-v',
            'ON_ERROR_STOP=1',
            '-c',
            f'TRUNCATE {tbl_list};',
        ]
        return self.cmd(cmd)

    def upload_to_objectstore(self, folder, archive):
        try:
            log.info('Connecting to objectstore')
            connection = objectstore.get_connection()
            log.info('Uploading to objectstore')
            upload_database(connection, folder, archive)
            return 0
        except Exception as ex:
            log.error(ex)
            return -1

    def process(self, tables, folder):
        error_count = 0
        for table in tables:
            if self.archive_table(table) != 0:
                error_count += 1
        if error_count == 0:
            archive_file = self.make_archive()
            # upload to object store
            if self.upload_to_objectstore(folder, archive_file) == 0:
                # only issue truncate if there are no errors
                self.truncate_tables(tables)

        self.cleanup_tmpfiles()


def assert_env_vars():
    # check for postgres and object store vars
    required_env = [
        'PGUSER',
        'PGDATABASE',
        'PGHOST',
        'PGPASSWORD',
        'TENANT_NAME',
        'TENANT_ID',
        'OBJECTSTORE_USER',
        'OBJECTSTORE_PASSWORD'
    ]
    error_count = 0
    for v in required_env:
        if v not in os.environ:
            log.error(f'{v} env var is not set')
            error_count += 1
    return error_count


def main():
    env_errors = assert_env_vars()
    if env_errors == 0:
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--table', nargs='+', help='List of tables',
                            required=True, type=str)
        parser.add_argument('-f', '--folder', help='folder on objectstore',
                            type=str, default='/')
        args = parser.parse_args()
        if len(sys.argv) == 1:
            parser.print_help()
            return 0
        log.info(args)
        archiver = Archiver()
        archiver.process(args.table, args.folder)
        return 0
    else:
        log.error(f'Missing env vars. Aborting.')
        return -1


if __name__ == '__main__':
    main()
