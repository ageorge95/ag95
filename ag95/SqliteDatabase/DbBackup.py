from ag95 import configure_logger
from os import path,\
    remove
from threading import Thread
from time import sleep
from sqlite3 import connect
from typing import AnyStr
from logging import getLogger
from datetime import datetime

class Dbbackup():
    def __init__(self,
                 input_filepath: AnyStr = 'database.db',
                 output_filepath: AnyStr = 'database_BAK.db',
                 print_progress: bool = False,
                 pages: int = 0):
        self._log = getLogger()

        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.print_progress = print_progress
        self.pages = pages

    def _backup_progress(self,
                         status,
                         remaining,
                         total):
        if self.print_progress:
            self._log.info(f'DB backup - {status}: Copied {total - remaining} of {total} pages...')

    def backup_db(self):
        start = datetime.now()
        # if the destination db exists remove it first, this significantly decreases the backup time
        if path.isfile(self.output_filepath):
            remove(self.output_filepath)

        # context managers do not work well with threads for some reason ...
        # for now connect will be used outside of context

        src = connect(self.input_filepath)
        dst = connect(self.output_filepath)

        src.backup(dst,
                   pages=self.pages,
                   progress=self._backup_progress)

        src.close()
        dst.close()

        self._log.info(f'DB backup completed in {(datetime.now() - start).total_seconds()}s')
    def vacuum_db(self):
        start = datetime.now()
        # context managers do not work well with threads for some reason ...
        # for now connect will be used outside of context
        con = connect(self.input_filepath)
        con.execute("VACUUM")
        con.close()

        self._log.info(f'DB vacuum completed in {(datetime.now() - start).total_seconds()}s')

    def thread_slave(self):
        while True:
            # 1h until the first backup
            # then 1h between subsequent backups
            to_sleep_s = 1 * 60 * 60
            seconds_slept = 0
            while seconds_slept < to_sleep_s:
                sleep(2)
                seconds_slept += 2

                if path.isfile('exit'):
                    print('Dbbackup terminated')
                    return

            self.vacuum_db()
            self.backup_db()

    def thread_master(self):
        return Thread(target=self.thread_slave)

if __name__ == '__main__':
    configure_logger()
    # simple backup request
    Dbbackup().backup_db()

    # threading daemon backup request
    # exit files are used
    Dbbackup(output_filepath='database_BAKdaemon.db').thread_master().start()
    with open('exit', 'w') as dummy:
        pass

    print('No automatic tests implemented so far; Please check the expected behavior manually.')