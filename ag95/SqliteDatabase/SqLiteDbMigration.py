from ag95 import (SqLiteColumnDef,
                  SqLiteDbWrapper)
from typing import (AnyStr,
                    List,
                    Optional)
import os

class SqLiteDbMigration:

    def __init__(self,
                 database_path: AnyStr = 'database.db',
                 all_tables_def: Optional[List] = None):

        self.database_path = database_path
        if not all_tables_def:
            self.all_tables_def = [{'table_name': 'my_db_table_name',
                                     'columns_def': [SqLiteColumnDef(column_name='my_column_name1',
                                                                     column_type='INTEGER'),
                                                     SqLiteColumnDef(column_name='my_column_name2',
                                                                     column_type='INTEGER')]}]
        else:
            self.all_tables_def = all_tables_def

    def migrate(self, db_wrapper: Optional[SqLiteDbWrapper] = None): #
        # create the db folder if missing
        if not os.path.isdir(os.path.dirname(self.database_path)):
            try:
                os.makedirs(os.path.dirname(self.database_path))
            except:
                pass

        if db_wrapper:
            # Run directly on the provided wrapper (Worker Thread)
            self._perform_migration(db_wrapper)
        else:
            # Run in its own new context (Standalone usage)
            with SqLiteDbWrapper(database_path=self.database_path) as DB:
                self._perform_migration(DB)

    def _perform_migration(self, DB: SqLiteDbWrapper):
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
    SqLiteDbMigration().migrate()

    print('No automatic tests implemented so far; Please check the expected behavior manually.')