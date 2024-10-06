from ag95 import configure_logger
from os import (path,
                remove,
                mkdir)
from threading import Thread
from time import sleep
from duckdb import connect
from typing import AnyStr
from logging import getLogger
from datetime import datetime
from traceback import format_exc

class DuckDbbackup():
    def __init__(self,
                 input_filepath: AnyStr = 'database.duckdb',
                 output_filepath: AnyStr = 'database_BAK.duckdb'):
        self._log = getLogger()

        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

    def backup_db(self):
        start = datetime.now()
        # if the destination db exists remove it first, this significantly decreases the backup time
        if path.isfile(self.output_filepath):
            remove(self.output_filepath)

        # create the root folder if missing
        if not path.isdir(path.dirname(self.output_filepath)):
            try:
                mkdir(path.dirname(self.output_filepath))
            except:
                pass
        try:
            # Connect to the existing DuckDB database
            connection = connect(self.input_filepath)

            # Create a backup
            connection.execute(f"ATTACH '{self.output_filepath}' AS backup_db;")

            # Get a list of tables in the current database
            tables = connection.execute("SELECT table_name FROM information_schema.tables;").fetchall()

            # Loop through the tables and copy them to the backup database
            for (table_name,) in tables:
                connection.execute(f"CREATE TABLE backup_db.{table_name} AS SELECT * FROM {table_name};")

            # Get a list of sequences
            sequences = connection.execute("SELECT sequencename, start_value, increment_by FROM database.pg_catalog.pg_sequences;").fetchall()

            # Loop through the sequences and create them in the backup database
            for (sequence_name, start_value, increment_by) in sequences:
                connection.execute(f"CREATE SEQUENCE backup_db.{sequence_name} START WITH {start_value} INCREMENT BY {increment_by};")

            # Optionally, detach the backup database
            connection.execute("DETACH backup_db;")

            # Close the connection
            connection.close()

            self._log.info(f'DB backup completed in {(datetime.now() - start).total_seconds()}s')
        except:
            # try to release the connections if any exception occurred above
            try:
                connection.close()
            except:
                # if closing the connections fails, simply do nothing
                pass

            # finally route the exception to the main thread
            raise Exception(format_exc(chain=False))

    def vacuum_db(self):
        start = datetime.now()
        # context managers do not work well with threads for some reason ...
        # for now connect will be used outside of context
        try:
            con = connect(self.input_filepath)
            con.execute("VACUUM")
            con.close()

            self._log.info(f'DB vacuum completed in {(datetime.now() - start).total_seconds()}s')
        except:
            # try to release the connection if any exception occurred above
            try:
                con.close()
            except:
                # if closing the connections fails, simply do nothing
                pass

            # finally route the exception to the main thread
            raise Exception(format_exc(chain=False))

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
                    self.vacuum_db()
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
    DuckDbbackup().backup_db()

    # threading daemon backup request
    # exit files are used
    DuckDbbackup(output_filepath='database_BAKdaemon.duckdb').thread_master(time_between_backups_s=5).start()
    with open('exit', 'w') as dummy:
        pass

    print('No automatic tests implemented so far; Please check the expected behavior manually.')