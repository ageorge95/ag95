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