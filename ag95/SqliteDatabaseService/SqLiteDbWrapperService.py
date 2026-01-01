from ag95 import (Singleton_without_cache,
                  SqLiteDbWrapper,
                  SqLiteColumnDef,
                  stdin_watcher)
from flask import (Flask,
                   jsonify,
                   request)
from waitress import serve
from datetime import datetime
import threading
import queue
import os
import requests

class DbTask:
    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.error = None
        self.done = threading.Event()

class SqliteDbWorker:
    def __init__(self, database_path: str, timeout: int):
        self.database_path = database_path
        self.timeout = timeout
        self.queue = queue.Queue()
        self._stop = False

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )
        self.thread.start()

        shutdown_watcher = threading.Thread(target=stdin_watcher,
                                            kwargs={'trigger_command': 'exit',
                                                    'init_action': (lambda: None),
                                                    'trigger_action': (lambda: self.shutdown())},
                                            daemon=True)
        shutdown_watcher.start()

    def _run(self):
        with SqLiteDbWrapper(
            database_path=self.database_path,
            timeout=self.timeout
        ) as db:

            while not self._stop:
                task: DbTask = self.queue.get()

                if task is None:
                    break

                try:
                    task.result = task.fn(db, *task.args, **task.kwargs)
                except Exception as e:
                    task.error = e
                finally:
                    task.done.set()

    def execute(self, fn, *args, **kwargs):
        task = DbTask(fn, args, kwargs)
        self.queue.put(task)
        task.done.wait()

        if task.error:
            raise task.error

        return task.result

    def shutdown(self):
        self._stop = True
        self.queue.put(None)
        self.thread.join()
        os._exit(0)

class ServiceBackend(metaclass=Singleton_without_cache):
    def __init__(self, database_path: str, timeout: int):
        self.worker = SqliteDbWorker(
            database_path=database_path,
            timeout=timeout
        )

    def get_tables_columns(self):
        return self.worker.execute(
            lambda db: db.get_tables_columns()
        )

    def insert_record(self, table_name, column_names, column_values):
        self.worker.execute(
            lambda db: db.append_in_table(
                table_name,
                column_names,
                column_values
            )
        )

    def get_records(self, **kwargs):
        return self.worker.execute(
            lambda db: db.return_records(**kwargs)
        )

    def update_record(self, table_name, record_id, data, skip_empty):
        self.worker.execute(
            lambda db: db.update_record(
                table_name,
                record_id,
                data,
                skip_empty
            )
        )

    def delete_record(self, table_name, record_id):
        self.worker.execute(
            lambda db: db.delete_record(table_name, record_id)
        )

def initialize_SqliteDbWrapper_service(LOCALHOST_ONLY=True,
                                       SERVICE_PORT=5834,
                                       database_path='database.db',
                                       timeout=60):

    backend = ServiceBackend(
        database_path=database_path,
        timeout=timeout
    )

    app = Flask(__name__)

    @app.get('/tables_columns')
    def tables_columns():
        return jsonify(backend.get_tables_columns())

    @app.post('/insert_record/<table>')
    def insert_record(table):
        payload = request.json
        backend.insert_record(
            table,
            payload['column_names'],
            payload['column_values']
        )
        return {'status': 'ok'}

    @app.get('/get_records/<table>')
    def get_records(table):
        return jsonify(
            backend.get_records(
                table_name=table
            )
        )

    serve(
        app,
        host='127.0.0.1' if LOCALHOST_ONLY else '0.0.0.0',
        port=SERVICE_PORT,
        threads=5
    )

if __name__ == '__main__':
    from ag95 import SqLiteDbMigration

    SqLiteDbMigration().migrate()

    SERVICE_PORT = 5834

    detached_thread = threading.Thread(target=initialize_SqliteDbWrapper_service,
                                       kwargs={'LOCALHOST_ONLY': True, 'SERVICE_PORT': SERVICE_PORT})
    detached_thread.start()

    with requests.Session() as session:

        # TEST correct column names query
        result = session.get(f'http://localhost:{SERVICE_PORT}/tables_columns').json()
        expected = {'my_db_table_name': ['ID', 'TIMESTAMP', 'my_column_name1', 'my_column_name2']}
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct new data append
        timestamp = int(datetime.now().timestamp())
        session.post(f'http://localhost:{SERVICE_PORT}/insert_record/my_db_table_name',
                     json={'column_names': ['my_column_name1', 'my_column_name2'],
                           'column_values': [7, 5]})
        result = session.get(f'http://localhost:{SERVICE_PORT}/get_records/my_db_table_name').json()
        expected = [[1, timestamp, 7, 5]]
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

    print('All tests are PASSED !')