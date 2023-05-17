from ag95 import configure_logger
from os import path
from threading import Thread
from time import sleep
from sqlite3 import connect
from typing import AnyStr
from logging import getLogger

class Dbbackup():
    def __init__(self,
                 input_filepath: AnyStr = 'database.db',
                 output_filepath: AnyStr = 'database_BAK.db',
                 print_progress: bool = False):
        self._log = getLogger()

        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.print_progress = print_progress

    def _backup_progress(self,
                         status,
                         remaining,
                         total):
        if self.print_progress:
            self._log.info(f'DB backup - {status}: Copied {total - remaining} of {total} pages...')

    def backup_db(self):
        # create new connections here, as these are used from different threads
        with connect(self.input_filepath) as src,\
                connect(self.output_filepath) as dst:
            with dst:
                src.backup(dst,
                           pages=1,
                           progress=self._backup_progress)
    def vacuum_db(self):
        with connect(self.input_filepath) as con:
            con.execute("VACUUM")

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
            self._log.info(f'Vacuuming the db ...')
            self.vacuum_db()
            self._log.info(f'Vacuum completed !')
            self._log.info(f'Backing up the db to {self.output_filepath} ...')
            self.backup_db()
            self._log.info(f'DB backup completed !')

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