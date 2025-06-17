from sqlite3 import connect
from typing import (List,
                    AnyStr,
                    Dict,
                    Literal,
                    Optional)
from datetime import (datetime,
                      timedelta)
from time import sleep

class SqLiteColumnDef:
    def __init__(self,
                column_name: AnyStr,
                column_type: AnyStr):
        self.column_name = column_name
        self.column_type = column_type

class SqLiteDbWrapper():
    def __init__(self,
                 database_path: AnyStr = 'database.db',
                 timeout: int = 60):
        self.database_path = database_path
        self.con = connect(database_path, timeout=timeout)
        self.con.execute('pragma journal_mode=wal')

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
                     columns_definition: List[SqLiteColumnDef]):
        columns_definition = [SqLiteColumnDef(column_name = 'ID',
                                              column_type = 'INTEGER PRIMARY KEY AUTOINCREMENT'),
                              SqLiteColumnDef(column_name='TIMESTAMP',
                                              column_type='INTEGER')] + columns_definition
        sql_columns_statement = ','.join([f"{_.column_name} {_.column_type}" for _ in columns_definition])
        sql_statement = f"CREATE TABLE {table_name} ({sql_columns_statement})"

        cursorObj = self.con.cursor()
        cursorObj.execute(sql_statement)

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
                   column_def: SqLiteColumnDef):

        cursorObj = self.con.cursor()
        cursorObj.execute(f"ALTER TABLE {table_name} ADD {column_def.column_name} {column_def.column_type}")

    def rename_column(self,
                      table_name: AnyStr,
                      old_column_name: AnyStr,
                      new_column_name: AnyStr):

        cursorObj = self.con.cursor()

        # 1. Get the current schema of the table
        cursorObj.execute(f"PRAGMA table_info('{table_name}')")
        columns_info = cursorObj.fetchall()

        if not any(col[1] == old_column_name for col in columns_info):
            print(f"Error: Column '{old_column_name}' not found in table '{table_name}'.")
            return

        column_definitions = []
        for col_info in columns_info:
            cid, name, data_type, notnull, default_value, primary_key = col_info
            if name == old_column_name:
                column_definitions.append(
                    f"{new_column_name} "
                    f"{data_type}"
                    f"{' NOT NULL' if notnull else ''}"
                    f"{' PRIMARY KEY' if primary_key else ''}"
                    f"{f' DEFAULT {default_value}' if default_value is not None else ''}")
            else:
                column_definitions.append(
                    f"{name} "
                    f"{data_type}"
                    f"{' NOT NULL' if notnull else ''}"
                    f"{' PRIMARY KEY' if primary_key else ''}"
                    f"{f' DEFAULT {default_value}' if default_value is not None else ''}")

        new_table_name = f"_temp_{table_name}"

        # 2. Create a new temporary table with the new column name
        create_table_sql = f"CREATE TABLE {new_table_name} ({', '.join(column_definitions)})"
        cursorObj.execute(create_table_sql)

        # 3. Construct the column list for the INSERT statement
        old_columns = [col[1] for col in columns_info]
        new_columns = [new_column_name if col == old_column_name else col for col in old_columns]
        columns_to_insert = ', '.join([str(col) for col in new_columns])
        old_columns_to_select = ', '.join(old_columns)

        # 4. Copy data from the old table to the new table
        insert_data_sql = (f"INSERT INTO "
                           f"{new_table_name} "
                           f"({columns_to_insert}) SELECT {old_columns_to_select} FROM {table_name}")
        cursorObj.execute(insert_data_sql)

        # 5. Drop the old table
        drop_table_sql = f"DROP TABLE {table_name}"
        cursorObj.execute(drop_table_sql)

        # 6. Rename the new table to the original table name
        rename_table_sql = f"ALTER TABLE {new_table_name} RENAME TO {table_name}"
        cursorObj.execute(rename_table_sql)

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
                       select_values: List[AnyStr] = [],
                       where_statement: Optional[str] = None,
                       order: Optional[Literal['DESC', 'ASC']] = None,
                       order_by: AnyStr = 'ID',
                       limit: Optional[int] = None) -> List[List]:

        sql_command = f'SELECT '
        if select_values:
            sql_command += ', '.join([str(val) for val in select_values])
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

        # extract the existing data (column names and values) as a dic
        cursorObj = self.con.cursor()
        column_names = cursorObj.execute(f"SELECT GROUP_CONCAT(NAME,',') FROM PRAGMA_TABLE_INFO('{table_name}')").fetchall()[0][0].split(',')
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
            set_statement_keys = ','.join([f"{key} = (?)" for key, value in existing_data.items()])
            set_statement_values = list(existing_data.values())
            # set_statement = ','.join([f"{key} = '{value}'" for key, value in existing_data.items()])
            sql = f"UPDATE {table_name} SET {set_statement_keys} WHERE ID = (?)"
            cursorObj.execute(sql, set_statement_values + [str(existing_data['ID'])])

if __name__ == '__main__':
    print('There is no DB available by default for this test.'
          ' Please create one before running this test. Use DbMigration for that.')
    sleep(2)

    with SqLiteDbWrapper() as DB:
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

        # TEST the column rename method
        DB.rename_column(table_name='my_db_table_name',
                         old_column_name='my_column_name1',
                         new_column_name='my_column_name11')
        result = str(DB.get_tables_columns())
        expected = str({'my_db_table_name': ['ID', 'TIMESTAMP', 'my_column_name11', 'my_column_name2']})
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

        result = str(DB.return_records(table_name='my_db_table_name'))
        expected = str([(1, timestamp, 10, 5)])
        assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

    print('All tests are PASSED !')