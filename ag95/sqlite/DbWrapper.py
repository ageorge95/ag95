from sqlite3 import connect
from typing import List,\
    AnyStr,\
    Dict,\
    Literal
from datetime import datetime,\
    timedelta
from time import sleep

class ColumnDef:
    def __init__(self,
                column_name: AnyStr,
                column_type: AnyStr):
        self.column_name = column_name
        self.column_type = column_type

class DbWrapper():
    def __init__(self,
                 database_path: AnyStr = 'database.db',
                 timeout: int = 60):
        self.database_path = database_path
        self.con = connect(database_path, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.con.commit()
        self.con.close()

    def get_tables_columns(self) -> Dict:
        tables_columns = {}
        cursorObj = self.con.cursor()
        cursorObj.execute('SELECT name from sqlite_master where type = "table"')

        all_table_names = [_[0] for _ in cursorObj.fetchall()]
        if 'sqlite_sequence' in all_table_names:
            all_table_names.remove('sqlite_sequence')

        for table_name in all_table_names:
            tables_columns.update({table_name : cursorObj.execute(f"SELECT GROUP_CONCAT(NAME,',') FROM PRAGMA_TABLE_INFO('{table_name}')").fetchall()[0][0].split(',')})

        return tables_columns

    def create_table(self,
                     table_name: AnyStr,
                     columns_definition: List):
        columns_definition = [ColumnDef(column_name = 'ID',
                                        column_type = 'INTEGER PRIMARY KEY AUTOINCREMENT'),
                              ColumnDef(column_name='TIMESTAMP',
                                        column_type='INTEGER')] + columns_definition
        sqlite_columns_statement = ','.join([f"{_.column_name} {_.column_type}" for _ in columns_definition])
        sqlite_statement = f"CREATE TABLE {table_name} ({sqlite_columns_statement})"

        cursorObj = self.con.cursor()
        cursorObj.execute(sqlite_statement)

    def drop_table(self,
                   table_name: AnyStr):

        cursorObj = self.con.cursor()
        cursorObj.execute(f"DROP TABLE {table_name}")

    def add_column(self,
                   table_name: AnyStr,
                   column_def: ColumnDef):

        cursorObj = self.con.cursor()
        cursorObj.execute(f"ALTER TABLE {table_name} ADD {column_def.column_name} {column_def.column_type}")

    def append_in_table(self,
                        table_name: AnyStr,
                        column_names: List,
                        column_values: List):

        column_names = ['TIMESTAMP'] + column_names
        column_values = [int(datetime.now().timestamp())] + column_values

        sql = f"INSERT INTO {table_name}({','.join(column_names)}) VALUES({','.join(['?']*len(column_values))})"

        cursorObj = self.con.cursor()
        cursorObj.execute(sql, column_values)

    def return_records(self,
                       table_name: AnyStr,
                       order: Literal['DESC', 'ASC'] = None,
                       limit: int = None) -> List:

        sql_command = f'SELECT * FROM {table_name}'
        if order:
            sql_command +=f' ORDER BY ID {order}'
        if limit:
            sql_command += f' LIMIT {limit}'

        cursorObj = self.con.cursor()
        return cursorObj.execute(sql_command).fetchall()

    def clear_old_records(self,
                          table_name: AnyStr,
                          since_time_in_past_s: int,
                          timestamp_column_name: AnyStr = 'TIMESTAMP'):

        minimum_timestamp = (datetime.now()-timedelta(seconds=since_time_in_past_s)).timestamp()

        sql = f"DELETE FROM {table_name} WHERE {timestamp_column_name} < {minimum_timestamp}"
        cursorObj = self.con.cursor()
        cursorObj.execute(sql)

if __name__ == '__main__':
    print('There is no DB available by default for this test.'
          ' Please create one before running this test. Use DbMigration for that.')
    sleep(2)

    with DbWrapper() as DB:
        result = str(DB.get_tables_columns())
        expected = str({'my_db_table_name': ['ID', 'TIMESTAMP', 'my_column_name']})
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        timestamp = int(datetime.now().timestamp())
        DB.append_in_table(table_name='my_db_table_name',
                           column_names=['my_column_name'],
                           column_values=[7])

        result = str(DB.return_records(table_name='my_db_table_name'))
        expected = str([(1, timestamp, 7)])
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

    print('All tests are PASSED !')