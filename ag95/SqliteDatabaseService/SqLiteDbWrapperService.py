from ag95 import (Singleton_without_cache,
                  SqLiteDbWrapper,
                  SqLiteDbbackup,
                  SqLiteDbMigration,
                  SqLiteColumnDef,
                  stdin_watcher)
from flask import (Flask,
                   jsonify,
                   request)
from waitress import serve
from datetime import datetime
from typing import (List,
                    AnyStr,
                    Optional,
                    Literal,
                    Dict)
import threading
import queue
import os
import requests
import time

all_shutdown_watcher_modes = Literal["ag95_stdin_watcher", "wait_for_exit_file", "none"]
def shutdown_watcher_start(mode: all_shutdown_watcher_modes = 'ag95_stdin_watcher',
                           trigger_action = (lambda: None)):
    if mode == "ag95_stdin_watcher":
        shutdown_watcher = threading.Thread(target=stdin_watcher,
                                            kwargs={'trigger_command': 'exit',
                                                    'init_action': (lambda: None),
                                                    'trigger_action': trigger_action},
                                            daemon=True)
        shutdown_watcher.start()

    elif mode == "wait_for_exit_file":
        def wait_for_exit_file():
            while True:
                if os.path.isfile('exit'):
                    trigger_action()
                else:
                    time.sleep(1)

        shutdown_watcher = threading.Thread(target=wait_for_exit_file,
                                            daemon=True)
        shutdown_watcher.start()

    else:
        return

class DbTask:
    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.error = None
        self.done = threading.Event()

class SqliteDbWorker:
    def __init__(self,
                 database_path: str,
                 timeout: int,
                 use_wal: bool = True,
                 num_threads: int = 4):
        self.database_path = database_path
        self.timeout = timeout
        self.use_wal = use_wal
        self.queue = queue.Queue()
        self._stop = False
        self.num_threads = num_threads
        self.threads = []

        # We need a barrier or counter to ensure ALL threads are ready before we proceed
        # otherwise the service might start accepting requests before connections are open.
        self._ready_barrier = threading.Barrier(num_threads + 1)  # +1 for the main thread

        # NEW: Ensure the DB is in WAL mode before threads start
        # This prevents the "database is locked" race condition.
        with SqLiteDbWrapper(database_path=self.database_path,
                             timeout=self.timeout,
                             use_wal=self.use_wal) as _:
            pass

        # Now it is safe to start multiple threads
        for _ in range(num_threads):
            t = threading.Thread(target=self._run, daemon=True)
            t.start()
            self.threads.append(t)

        # Wait for all workers to create their database connections
        try:
            self._ready_barrier.wait(timeout=10.0)
        except threading.BrokenBarrierError:
            print("Error: Database worker threads failed to initialize in time.")

    def _run(self):
        # Create a THREAD-LOCAL connection.
        # SQLite connections generally cannot be shared across threads.
        db = SqLiteDbWrapper(
            database_path=self.database_path,
            timeout=self.timeout,
            use_wal=self.use_wal
        )

        # Set auto-commit mode
        db.con.isolation_level = None

        # Signal that this specific thread is ready
        self._ready_barrier.wait()

        while not self._stop:
            task: DbTask = self.queue.get()

            # Sentinel value to stop the thread
            if task is None:
                self.queue.task_done()
                break

            try:
                # Execute the task using THIS thread's connection
                task.result = task.fn(db, *task.args, **task.kwargs)
                db.con.commit()
            except Exception as e:
                db.con.rollback()
                task.error = e
            finally:
                task.done.set()
                self.queue.task_done()

        # Clean up when thread exits
        if db:
            db.con.close()

    def execute(self, fn, *args, **kwargs):
        task = DbTask(fn, args, kwargs)
        self.queue.put(task)
        task.done.wait()

        if task.error:
            raise task.error

        return task.result

    def shutdown(self):
        self._stop = True
        # Put 'None' in the queue once for EACH thread
        for _ in range(self.num_threads):
            self.queue.put(None)

        # Wait for all threads to finish
        for t in self.threads:
            t.join(timeout=2.0)

class ServiceBackend(metaclass=Singleton_without_cache):
    def __init__(self,
                 database_path: str,
                 timeout: int,
                 use_wal: bool = True,
                 num_threads: int = 4):
        self.worker = SqliteDbWorker(
            database_path=database_path,
            timeout=timeout,
            use_wal=use_wal,
            num_threads=num_threads
        )

    def get_tables_columns(self):
        return self.worker.execute(
            lambda db: db.get_tables_columns()
        )

    def insert_record(self,
                      table_name: AnyStr,
                      column_names: List,
                      column_values: List):
        self.worker.execute(
            lambda db: db.append_in_table(table_name=table_name,
                                          column_names=column_names,
                                          column_values=column_values)
        )

    def get_records(self,
                    table_name: AnyStr,
                    select_values: List[AnyStr] = (),
                    where_statement: Optional[str] = None,
                    order: Optional[Literal['DESC', 'ASC']] = None,
                    order_by: AnyStr = 'ID',
                    limit: Optional[int] = None):
        return self.worker.execute(
            lambda db: db.return_records(table_name=table_name,
                                         select_values=select_values,
                                         where_statement=where_statement,
                                         order=order,
                                         order_by=order_by,
                                         limit=limit)
        )

    def update_record(self,
                      table_name: AnyStr,
                      record_ID: int,
                      data: Dict,
                      skip_new_empty_entries: bool = False):
        self.worker.execute(
            lambda db: db.update_record(table_name=table_name,
                                        record_ID=record_ID,
                                        data=data,
                                        skip_new_empty_entries=skip_new_empty_entries)
        )

    def delete_record(self,
                      table_name: AnyStr,
                      record_ID: int):
        self.worker.execute(
            lambda db: db.delete_record(table_name=table_name,
                                        record_ID=record_ID)
        )

    def clear_old_records(self,
                          table_name: AnyStr,
                          since_time_in_past_s: int,
                          timestamp_column_name: AnyStr = 'TIMESTAMP'):
        self.worker.execute(
            lambda db: db.clear_old_records(table_name=table_name,
                                            since_time_in_past_s=since_time_in_past_s,
                                            timestamp_column_name=timestamp_column_name)
        )

    def backup_db(self, output_filepath: str):
        # Execute the backup using the worker's DB connection (db.con)
        self.worker.execute(
            lambda db: SqLiteDbbackup(input_filepath=db.database_path,
                                      output_filepath=output_filepath).backup_db(source_connection=db.con)
        )

    def migrate_db(self, all_tables_def: Optional[List] = None):
        # Execute the migration using the worker's DB wrapper (db)
        self.worker.execute(
            lambda db: SqLiteDbMigration(database_path=db.database_path,
                                         all_tables_def=all_tables_def).migrate(db_wrapper=db)
        )

def initialize_SqliteDbWrapper_service(LOCALHOST_ONLY=True,
                                       SERVICE_PORT=5834,
                                       database_path='database.db',
                                       timeout=60,
                                       use_wal=True,
                                       shutdown_watcher_mode: all_shutdown_watcher_modes = 'ag95_stdin_watcher',
                                       num_threads: int = 4):
    # Create an event to signal the main service thread to exit
    stop_event = threading.Event()

    def handle_shutdown():
        backend.worker.shutdown()  # Closes all DB connections gracefully
        stop_event.set()  # Signals the loop below to stop

    backend = ServiceBackend(
        database_path=database_path,
        timeout=timeout,
        use_wal=use_wal,
        num_threads=num_threads
    )

    # Start the watcher and use the handle_shutdown() handler
    shutdown_watcher_start(mode=shutdown_watcher_mode,
                           trigger_action=handle_shutdown)

    app = Flask(__name__)

    @app.get('/tables_columns')
    def tables_columns():
        return jsonify(backend.get_tables_columns())

    @app.post('/insert_record')
    def insert_record():
        payload = request.json
        backend.insert_record(
            table_name=payload['table_name'],
            column_names=payload['column_names'],
            column_values=payload['column_values']
        )
        return {'status': 'ok'}

    @app.post('/update_record')
    def update_record():
        payload = request.json
        backend.update_record(
            table_name=payload['table_name'],
            record_ID=payload['record_ID'],
            data=payload['data'],
            skip_new_empty_entries=payload.get('skip_new_empty_entries')
        )
        return {'status': 'ok'}

    @app.post('/delete_record')
    def delete_record():
        payload = request.json
        backend.delete_record(
            table_name=payload['table_name'],
            record_ID=payload['record_ID']
        )
        return {'status': 'ok'}

    @app.post('/clear_old_records')
    def clear_old_records():
        payload = request.json
        backend.clear_old_records(
            table_name=payload['table_name'],
            since_time_in_past_s=payload['since_time_in_past_s'],
            timestamp_column_name=payload.get('timestamp_column_name', 'TIMESTAMP')
        )
        return {'status': 'ok'}

    @app.get('/get_records')
    def get_records():
        payload = request.json
        return jsonify(
            backend.get_records(
                table_name=payload['table_name'],
                select_values=payload.get('select_values'),
                where_statement=payload.get('where_statement'),
                order=payload.get('order'),
                order_by=payload.get('order_by', 'ID'),
                limit=payload.get('limit')
            )
        )

    @app.post('/backup_db')
    def backup_db():
        payload = request.get_json(silent=True) or {}
        # Default to database_BAK.db if not specified
        output_filepath = payload.get('output_filepath', 'database_BAK.db')

        try:
            backend.backup_db(output_filepath=output_filepath)
            return {'status': 'ok', 'message': f'Backup created at {output_filepath}'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    @app.post('/migrate_db')
    def migrate_db():
        payload = request.get_json(silent=True) or {}
        raw_defs = payload.get('all_tables_def')

        final_defs = None

        # If the user passed a schema in the JSON, we must reconstruct the objects
        # because SqLiteDbMigration expects SqLiteColumnDef objects, not dicts.
        if raw_defs:
            final_defs = []
            for table in raw_defs:
                cols = [SqLiteColumnDef(c['column_name'], c['column_type']) for c in table['columns_def']]
                final_defs.append({'table_name': table['table_name'], 'columns_def': cols})

        try:
            backend.migrate_db(all_tables_def=final_defs)
            return {'status': 'ok', 'message': 'Migration completed'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    # Start Waitress in a DAEMON thread so it doesn't block the exit
    server_thread = threading.Thread(
        target=serve,
        kwargs={
            'app': app,
            'host': '127.0.0.1' if LOCALHOST_ONLY else '0.0.0.0',
            'port': SERVICE_PORT,
            'threads': 5
        },
        daemon=True
    )
    server_thread.start()

    # Keep this thread alive until handle_shutdown is called
    while not stop_event.is_set():
        stop_event.wait(timeout=1.0)

if __name__ == '__main__':
    SERVICE_PORT = 5834

    detached_thread = threading.Thread(target=initialize_SqliteDbWrapper_service,
                                       kwargs={'LOCALHOST_ONLY': True, 'SERVICE_PORT': SERVICE_PORT})
    detached_thread.start()

    with requests.Session() as session:

        migration_payload = {
            "all_tables_def": [
                {
                    "table_name": "my_db_table_name",
                    "columns_def": [
                        {"column_name": "my_column_name1", "column_type": "INTEGER"},
                        {"column_name": "my_column_name2", "column_type": "INTEGER"}
                    ]
                }
            ]
        }
        session.post(f'http://localhost:{SERVICE_PORT}/migrate_db',
                     json=migration_payload)

        # TEST correct column names query
        result = session.get(f'http://localhost:{SERVICE_PORT}/tables_columns').json()
        expected = {'my_db_table_name': ['ID', 'TIMESTAMP', 'my_column_name1', 'my_column_name2']}
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct new data append
        timestamp = int(datetime.now().timestamp())
        session.post(f'http://localhost:{SERVICE_PORT}/insert_record',
                     json={'table_name': 'my_db_table_name',
                           'column_names': ['my_column_name1', 'my_column_name2'],
                           'column_values': [7, 5]})
        result = session.get(f'http://localhost:{SERVICE_PORT}/get_records',
                             json={'table_name': 'my_db_table_name'}).json()
        expected = [[1, timestamp, 7, 5]]
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct filtered data return, 1 requested column
        result = session.get(f'http://localhost:{SERVICE_PORT}/get_records',
                             json={'table_name': 'my_db_table_name',
                                   'select_values': ['my_column_name1']}).json()
        expected = [[7]]
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct filtered data return, 2 requested columns
        result = session.get(f'http://localhost:{SERVICE_PORT}/get_records',
                             json={'table_name': 'my_db_table_name',
                                   'select_values': ['my_column_name1', 'my_column_name2']}).json()
        expected = [[7, 5]]
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct record update
        session.post(f'http://localhost:{SERVICE_PORT}/update_record',
                     json={'table_name': 'my_db_table_name',
                           'record_ID': 1,
                           'data': {'my_column_name1': 10}})
        result = session.get(f'http://localhost:{SERVICE_PORT}/get_records',
                             json={'table_name': 'my_db_table_name'}).json()
        expected = [[1, timestamp, 10, 5]]
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST db backup
        session.post(f'http://localhost:{SERVICE_PORT}/backup_db')

    print('All tests are PASSED !')