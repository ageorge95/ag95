from ag95 import ColumnDef,\
    DbWrapper
from typing import AnyStr,\
    List

class DbMigration:

    def __init__(self,
                 database_path: AnyStr = 'database.db',
                 all_tables_def: List = None):

        self.database_path = database_path
        if not all_tables_def:
            self.all_tables_def = [{'table_name': 'my_db_table_name',
                                     'columns_def': [ColumnDef(column_name='my_column_name1',
                                                               column_type='INTEGER'),
                                                     ColumnDef(column_name='my_column_name2',
                                                               column_type='INTEGER')]}]
        else:
            self.all_tables_def = all_tables_def

    def migrate(self):
        with DbWrapper(database_path=self.database_path) as DB:
            current_table_columns = DB.get_tables_columns()
            for table_def in self.all_tables_def:
                if table_def['table_name'] not in current_table_columns.keys():
                    DB.create_table(table_name=table_def['table_name'],
                                    columns_definition=table_def['columns_def'])
                else:
                    for column_def in table_def['columns_def']:
                        if column_def.column_name not in current_table_columns[table_def['table_name']]:
                            # a table with this name exists, but the columns configuration has changed,
                            # so the table will be updated
                            # !!! ONLY NEW COLUMNS WILL BE ADDED !!!
                            # !!! IF A COLUMN WAS DELETED FROM THE db_def IT WILL STILL BE PRESENT IN THE DB !!!
                            DB.add_column(table_name=table_def['table_name'],
                                          column_def=column_def)

if __name__ == '__main__':
    DbMigration().migrate()

    print('No automatic tests implemented so far; Please check the expected behavior manually.')