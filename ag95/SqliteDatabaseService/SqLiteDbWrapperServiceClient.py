import requests
from typing import (List,
                    AnyStr,
                    Optional,
                    Literal,
                    Dict)

class SqLiteDbWrapperServiceClient:
    """
    A client library for interacting with the SqLiteDbWrapperService.

    This client is designed to be used as a context manager to ensure
    that network connections are properly managed and closed.

    Recommended Usage:
    with SqLiteDbWrapperServiceClient(port=5834) as client:
        tables = client.get_tables_columns()
        client.insert_record(...)
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 5834):
        """
        Initializes the client.

        Args:
            host (str): The hostname or IP address of the service.
            port (int): The port the service is running on.
        """
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()

    def __enter__(self):
        """Enables use of the 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the session when exiting the 'with' block."""
        self.close()

    def close(self):
        """Closes the underlying requests session."""
        if self.session:
            self.session.close()
            self.session = None

    def _request(self, method: str, endpoint: str, **kwargs):
        """Helper method to handle requests and errors."""
        if not self.session:
            raise RuntimeError("Session is closed. Cannot make requests.")

        url = self.base_url + endpoint
        try:
            # Set a reasonable timeout for all requests
            kwargs.setdefault('timeout', 30)
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            if response.text:
                return response.json()
            return {'status': 'ok'}  # Return a default success status for POSTs with no body
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the service: {e}")
            raise

    def get_tables_columns(self) -> Dict:
        """Retrieves all table names and their column definitions."""
        return self._request('get', '/tables_columns')

    def insert_record(self, table_name: AnyStr, column_names: List, column_values: List) -> Dict:
        """Inserts a new record into a table."""
        payload = {
            'table_name': table_name,
            'column_names': column_names,
            'column_values': column_values
        }
        return self._request('post', '/insert_record', json=payload)

    def get_records(self,
                    table_name: AnyStr,
                    select_values: Optional[List[AnyStr]] = None,
                    where_statement: Optional[str] = None,
                    order: Optional[Literal['DESC', 'ASC']] = None,
                    order_by: AnyStr = 'ID',
                    limit: Optional[int] = None) -> List:
        """Retrieves records from a table with optional filtering and ordering."""
        payload = {
            'table_name': table_name,
            'select_values': select_values,
            'where_statement': where_statement,
            'order': order,
            'order_by': order_by,
            'limit': limit
        }
        return self._request('get', '/get_records', json=payload)

    def update_record(self,
                      table_name: AnyStr,
                      record_ID: int,
                      data: Dict,
                      skip_new_empty_entries: bool = False) -> Dict:
        """Updates an existing record in a table."""
        payload = {
            'table_name': table_name,
            'record_ID': record_ID,
            'data': data,
            'skip_new_empty_entries': skip_new_empty_entries
        }
        return self._request('post', '/update_record', json=payload)

    def delete_record(self, table_name: AnyStr, record_ID: int) -> Dict:
        """Deletes a record from a table by its ID."""
        payload = {'table_name': table_name, 'record_ID': record_ID}
        return self._request('post', '/delete_record', json=payload)

    def backup_db(self, output_filepath: str = 'database_BAK.db') -> Dict:
        """Triggers a database backup on the service."""
        payload = {'output_filepath': output_filepath}
        return self._request('post', '/backup_db', json=payload)

    def migrate_db(self, all_tables_def: Optional[List] = None) -> Dict:
        """Triggers a database migration on the service."""
        payload = {'all_tables_def': all_tables_def}
        return self._request('post', '/migrate_db', json=payload)

# --- Test Suite ---
if __name__ == '__main__':
    import threading
    import time
    import os
    from datetime import datetime
    # We need to import the service from the other file to start it for the test
    from SqLiteDbWrapperService import initialize_SqliteDbWrapper_service, all_shutdown_watcher_modes

    # --- Test Setup ---
    TEST_DB_FILE = "test_client_db.db"
    TEST_BACKUP_FILE = "client_test_BAK.db"
    TEST_SERVICE_PORT = 5835  # Use a different port to avoid conflicts

    # Clean up any leftover files from a previous failed run
    if os.path.exists(TEST_DB_FILE): os.remove(TEST_DB_FILE)
    if os.path.exists(TEST_BACKUP_FILE): os.remove(TEST_BACKUP_FILE)
    if os.path.exists("exit"): os.remove("exit")

    print("Starting background service for testing...")
    service_thread = threading.Thread(
        target=initialize_SqliteDbWrapper_service,
        kwargs={
            'LOCALHOST_ONLY': True,
            'SERVICE_PORT': TEST_SERVICE_PORT,
            'database_path': TEST_DB_FILE,
            # Use file-based shutdown for easy programmatic control
            'shutdown_watcher_mode': 'wait_for_exit_file'
        },
        daemon=True
    )
    service_thread.start()
    time.sleep(2)  # Give the service a moment to start up

    # --- Test Execution ---
    try:
        with SqLiteDbWrapperServiceClient(port=TEST_SERVICE_PORT) as client:
            print("--- Running Client Tests ---")

            # 1. Test DB Migration
            migration_payload = {
                "all_tables_def": [{
                    "table_name": "my_test_table",
                    "columns_def": [
                        {"column_name": "col_A", "column_type": "INTEGER"},
                        {"column_name": "col_B", "column_type": "TEXT"}
                    ]
                }]
            }
            client.migrate_db(all_tables_def=migration_payload['all_tables_def'])
            print("✅ Test 1: Migration successful")

            # 2. Test Get Tables & Columns
            tables = client.get_tables_columns()
            expected_tables = {'my_test_table': ['ID', 'TIMESTAMP', 'col_A', 'col_B']}
            assert tables == expected_tables, f"Expected {expected_tables}, got {tables}"
            print("✅ Test 2: Get Tables & Columns successful")

            # 3. Test Insert Record
            timestamp_before = int(datetime.now().timestamp())
            client.insert_record(
                table_name='my_test_table',
                column_names=['col_A', 'col_B'],
                column_values=[123, 'hello']
            )
            print("✅ Test 3: Insert Record successful")

            # 4. Test Get Records
            records = client.get_records(table_name='my_test_table')
            assert len(records) == 1, "Should be 1 record"
            # Verify record content (ID=1, timestamp is recent, data is correct)
            assert records[0][0] == 1
            assert records[0][1] >= timestamp_before
            assert records[0][2:] == [123, 'hello']
            print("✅ Test 4: Get Records successful")

            # 5. Test Get Specific Columns
            records_subset = client.get_records(table_name='my_test_table', select_values=['col_B', 'col_A'])
            expected_subset = [['hello', 123]]
            assert records_subset == expected_subset, f"Expected {expected_subset}, got {records_subset}"
            print("✅ Test 5: Get Specific Columns successful")

            # 6. Test Update Record
            client.update_record(table_name='my_test_table', record_ID=1, data={'col_B': 'world'})
            updated_records = client.get_records(table_name='my_test_table')
            assert updated_records[0][3] == 'world', "Update failed"
            print("✅ Test 6: Update Record successful")

            # 7. Test Delete Record
            client.delete_record(table_name='my_test_table', record_ID=1)
            final_records = client.get_records(table_name='my_test_table')
            assert final_records == [], "Delete failed, record still exists"
            print("✅ Test 7: Delete Record successful")

            # 8. Test DB Backup
            client.backup_db(output_filepath=TEST_BACKUP_FILE)
            assert os.path.exists(TEST_BACKUP_FILE), "Backup file was not created"
            print("✅ Test 8: DB Backup successful")

        print("\n🎉 All tests PASSED! 🎉")

    except Exception as e:
        print(f"\n❌ A test failed: {e}")
    finally:
        # --- Teardown ---
        print("\nShutting down service and cleaning up...")
        # Create the 'exit' file to signal the service to shut down
        with open("exit", "w") as f:
            f.write("stop")

        service_thread.join(timeout=5)  # Wait for the service thread to terminate

        # Clean up the files created during the test
        if os.path.exists(TEST_DB_FILE): os.remove(TEST_DB_FILE)
        if os.path.exists(TEST_DB_FILE+'-shm'): os.remove(TEST_DB_FILE+'-shm')
        if os.path.exists(TEST_DB_FILE+'-wal'): os.remove(TEST_DB_FILE+'-wal')
        if os.path.exists(TEST_BACKUP_FILE): os.remove(TEST_BACKUP_FILE)
        if os.path.exists("exit"): os.remove("exit")
        print("Cleanup complete.")