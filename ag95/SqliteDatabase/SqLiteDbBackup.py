import shutil
from ag95 import configure_logger
from os import (path,
                makedirs,
                remove)
from threading import Thread
from time import sleep
from sqlite3 import connect
from typing import AnyStr
from logging import getLogger
from datetime import datetime
from traceback import format_exc

class SqLiteDbbackup():
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

    def vacuum_db(self, connection=None):
        start = datetime.now()
        threshold_mb = 50  # Limit for vacuuming

        # If an existing connection is provided, use it.
        # Otherwise, open a temporary new one (legacy behavior).
        local_con = None
        target_con = connection

        try:
            if target_con is None:
                local_con = connect(self.input_filepath)
                target_con = local_con

            # 1. Check free space before vacuuming
            cursor = target_con.cursor()
            freelist_count = cursor.execute('PRAGMA freelist_count').fetchone()[0]
            page_size = cursor.execute('PRAGMA page_size').fetchone()[0]

            free_bytes = freelist_count * page_size
            free_mb = free_bytes / (1024 * 1024)

            # 2. Decide whether to Vacuum
            if free_mb > threshold_mb:
                self._log.info(f'Free space ({free_mb:.2f} MB) > {threshold_mb} MB. Starting VACUUM...')

                # VACUUM requires no active transaction.
                target_con.execute("VACUUM")

                self._log.info(
                    f'DB vacuum completed in {(datetime.now() - start).total_seconds()}s. Reclaimed {free_mb:.2f} MB.')
            else:
                self._log.info(f'DB vacuum skipped. Free space ({free_mb:.2f} MB) is below {threshold_mb} MB limit.')

        except:
            # Only log/raise, do not close the external connection
            raise Exception(format_exc(chain=False))
        finally:
            # Only close the connection if we created it locally
            if local_con is not None:
                local_con.close()

    def backup_db(self, source_connection=None):
        # 1. VACUUM first (Conditional)
        if source_connection:
            self.vacuum_db(connection=source_connection)
        else:
            self.vacuum_db()

        # 2. Proceed with Fast Backup (Lock & Copy)
        start = datetime.now()

        # Prepare destination folder
        if not path.isdir(path.dirname(self.output_filepath)):
            try:
                makedirs(path.dirname(self.output_filepath))
            except:
                pass

        lock_con = None
        temp_backup = None
        try:
            # Connect with isolation_level=None to manage transactions manually
            lock_con = connect(self.input_filepath, isolation_level=None)

            # A. CHECK IF WAL MODE & CHECKPOINT BEFORE LOCKING
            cursor = lock_con.cursor()
            journal_mode = cursor.execute("PRAGMA journal_mode").fetchone()[0].lower()

            if journal_mode == 'wal':
                # CHECKPOINT must happen BEFORE acquiring the write lock
                # This moves data from the -wal file to the main .db file
                lock_con.execute("PRAGMA wal_checkpoint(TRUNCATE)")

            # B. ACQUIRE LOCK
            # 'BEGIN IMMEDIATE' prevents other connections from writing,
            # ensuring the file on disk doesn't change while we copy.
            lock_con.execute("BEGIN IMMEDIATE")

            # C. PERFORM FAST OS COPY TO TEMP FILE
            # Use a temporary file first to avoid deleting the old backup until we know the new one succeeds
            temp_backup = self.output_filepath + '.tmp'
            shutil.copy2(self.input_filepath, temp_backup)

            # D. RELEASE LOCK
            lock_con.execute("ROLLBACK")

            # E. REPLACE OLD BACKUP WITH NEW ONE
            # Delete old backup first for better performance (avoids slow overwrite)
            if path.exists(self.output_filepath):
                try:
                    remove(self.output_filepath)
                except Exception as del_error:
                    self._log.warning(f'Could not delete old backup: {del_error}')

            # Rename temp file to final name (fast operation)
            shutil.move(temp_backup, self.output_filepath)
            temp_backup = None  # Mark as successfully moved

            self._log.info(f'DB backup (Fast Copy) completed in {(datetime.now() - start).total_seconds()}s')

        except Exception as e:
            # Ensure lock is released even if copy fails
            if lock_con:
                try:
                    lock_con.execute("ROLLBACK")
                except:
                    pass
            # Clean up temp file if it exists
            if temp_backup and path.exists(temp_backup):
                try:
                    remove(temp_backup)
                except:
                    pass
            raise Exception(format_exc(chain=False))
        finally:
            if lock_con:
                lock_con.close()

    def thread_slave(self,
                     time_between_backups_s: int = 60*60*12):
        time_between_backup_checks_s = 60

        def check_if_backup() -> bool:
            if path.isfile(self.output_filepath):
                mtimestamp = path.getmtime(self.output_filepath)
                now_timestamp = datetime.now().timestamp()
                return True if now_timestamp - mtimestamp > time_between_backups_s\
                    else False
            else:
                return True

        while True:
            if check_if_backup():
                try:
                    self.backup_db()
                except:
                    self._log.warning(f'Failed to backup db:\n{format_exc(chain=False)}')
                    seconds_slept = 0
                    while seconds_slept < 5*60:
                        sleep(2)
                        seconds_slept += 2

                        if path.isfile('exit'):
                            print('Dbbackup terminated')
                            return
            else:
                seconds_slept = 0
                while seconds_slept < time_between_backup_checks_s:
                    sleep(2)
                    seconds_slept += 2

                    if path.isfile('exit'):
                        print('Dbbackup terminated')
                        return

    def thread_master(self,
                      time_between_backups_s: int = 60*60*12):
        return Thread(target=self.thread_slave,
                      args=(time_between_backups_s,))

if __name__ == '__main__':
    configure_logger()
    # simple backup request
    SqLiteDbbackup().backup_db()

    # # threading daemon backup request
    # # exit files are used
    # SqLiteDbbackup(output_filepath='database_BAKdaemon.db').thread_master(time_between_backups_s=5).start()
    # with open('exit', 'w') as dummy:
    #     pass

    print('No automatic tests implemented so far; Please check the expected behavior manually.')