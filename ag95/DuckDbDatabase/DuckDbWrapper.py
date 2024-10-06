from duckdb import connect
from typing import List,\
    AnyStr,\
    Dict,\
    Literal
from datetime import datetime,\
    timedelta
from time import sleep

class DuckColumnDef:
    def __init__(self,
                column_name: AnyStr,
                column_type: AnyStr):
        self.column_name = column_name
        self.column_type = column_type

class DuckDbWrapper():
    def __init__(self,
                 database_path: AnyStr = 'database.duckdb',
                 timeout: int = 60):
        self.database_path = database_path
        self.con = connect(database_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.con.commit()
        self.con.close()

    def get_tables_columns(self) -> Dict:
        tables_columns = {}
        cursorObj = self.con.cursor()

        # get a list of all the table names
        cursorObj.execute("""SELECT table_name 
                             FROM information_schema.tables 
                             WHERE table_schema = 'main';  -- 'main' is the default schema in DuckDB""")
        all_table_names = [_[0] for _ in cursorObj.fetchall()]

        for table_name in all_table_names:

            tables_columns.update({table_name : [_[0] for _ in cursorObj.execute(f"""SELECT column_name 
                                                                                 FROM information_schema.columns 
                                                                                 WHERE table_name = '{table_name}';""").fetchall()]})

        return tables_columns

    def create_table(self,
                     table_name: AnyStr,
                     columns_definition: List[DuckColumnDef]):

        sql_sequence = f'CREATE SEQUENCE seq_{table_name} START 1;'
        self.con.execute(sql_sequence)

        columns_definition = [DuckColumnDef(column_name = 'ID',
                                            column_type = f'INTEGER primary key default nextval(\'seq_{table_name}\')'),
                              DuckColumnDef(column_name='TIMESTAMP',
                                            column_type='INTEGER')] + columns_definition
        sqlite_columns_statement = ','.join([f"{_.column_name} {_.column_type}" for _ in columns_definition])
        sqlite_statement = f"CREATE TABLE {table_name} ({sqlite_columns_statement})"

        self.con.execute(sqlite_statement)

    def drop_table(self,
                   table_name: AnyStr):

        cursorObj = self.con.cursor()
        cursorObj.execute(f"DROP TABLE {table_name}")

    def delete_record(self,
                    table_name: AnyStr,
                    record_ID: int):

        cursorObj = self.con.cursor()
        set_statement = f"DELETE FROM {table_name} WHERE ID = (?)"
        cursorObj.execute(set_statement, [record_ID, ])

    def add_column(self,
                   table_name: AnyStr,
                   column_def: DuckColumnDef):

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
                       select_values: List[AnyStr] = None,
                       where_statement: AnyStr = None,
                       order: Literal['DESC', 'ASC'] = None,
                       order_by: AnyStr = 'ID',
                       limit: int = None) -> List[List]:

        sql_command = f'SELECT '
        if select_values:
            sql_command += ', '.join(select_values)
        else:
            sql_command += '*'
        sql_command += f' FROM {table_name}'
        if where_statement:
            sql_command += f' WHERE {where_statement}'
        if order:
            sql_command += f' ORDER BY {order_by} {order}'
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

    def update_record(self,
                      table_name: AnyStr,
                      record_ID: int,
                      data: Dict,
                      skip_new_empty_entries: bool = False):

        # extract the existing data (column names and values) as a dict
        cursorObj = self.con.cursor()
        column_names = [_[0] for _ in cursorObj.execute(f"""SELECT column_name 
                                                        FROM information_schema.columns 
                                                        WHERE table_name = '{table_name}';""").fetchall()]
        column_values = cursorObj.execute(f'SELECT * FROM {table_name} WHERE ID = (?)', [str(record_ID),]).fetchall()

        existing_data = dict([[key, value] for key, value in zip(column_names, column_values[0])])

        # only proceed if data is != existing_data
        different = False
        for key, value in data.items():
            if data[key] != existing_data[key]:
                different = True
                break
        if different:

            # update the dict with the new data passed as an argument
            existing_data.update(data)

            # remove empty entries from the dict
            if skip_new_empty_entries:
                existing_data = dict(filter(lambda _:_[1], existing_data.items()))

            # finally update the row inside the db
            # NOTE: [1:] is used because we do not want to overwrite the ID column
            # assumption that should be true: the ID is ALWAYs the first value
            set_statement_keys = ','.join([f"{key} = (?)" for key, value in list(existing_data.items())[1:]])
            set_statement_values = list(existing_data.values())[1:]
            # set_statement = ','.join([f"{key} = '{value}'" for key, value in existing_data.items()])
            sql = f"UPDATE {table_name} SET {set_statement_keys} WHERE ID = (?)"

            cursorObj.execute(sql, set_statement_values + [str(existing_data['ID'])])

if __name__ == '__main__':
    print('There is no DB available by default for this test.'
          ' Please create one before running this test. Use DbMigration for that.')
    sleep(2)

    with DuckDbWrapper() as DB:
        # TEST correct column names query
        result = str(DB.get_tables_columns())
        expected = str({'my_db_table_name': ['ID', 'TIMESTAMP', 'my_column_name1', 'my_column_name2']})
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct new data append
        timestamp = int(datetime.now().timestamp())
        DB.append_in_table(table_name='my_db_table_name',
                           column_names=['my_column_name1', 'my_column_name2'],
                           column_values=[7, 5])

        result = str(DB.return_records(table_name='my_db_table_name'))
        expected = str([(1, timestamp, 7, 5)])
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct filtered data return, 1 requested column
        result = str(DB.return_records(table_name='my_db_table_name',
                                       select_values=['my_column_name1']))
        expected = str([(7,)])
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct filtered data return, 2 requested columns
        result = str(DB.return_records(table_name='my_db_table_name',
                                       select_values=['my_column_name1', 'my_column_name2']))
        expected = str([(7,5,)])
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        # TEST correct record update
        DB.update_record(table_name='my_db_table_name',
                         record_ID=1,
                         data={'my_column_name1': 10})
        result = str(DB.return_records(table_name='my_db_table_name'))
        expected = str([(1, timestamp, 10, 5)])
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

    print('All tests are PASSED !')