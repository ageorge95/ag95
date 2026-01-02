from ag95 import (Singleton_without_cache,
                  SqLiteDbWrapper,
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

    @app.get('/get_records')
    def get_records():
        payload = request.json
        return jsonify(
            backend.get_records(
                table_name=payload['table_name'],
                select_values=payload.get('select_values'),
                where_statement=payload.get('where_statement'),
                order=payload.get('order'),
                order_by=payload.get('order_by'),
                limit=payload.get('limit')
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

    print('All tests are PASSED !')