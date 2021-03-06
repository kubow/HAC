import argparse
import difflib
import sqlite3

from Template import SQL
# from TX74 import TextContent  # difflib import here

class DataBaseObject(object):
    """db_path can be a log_file, it creates record in sqlite in the same path"""
    def __init__(self, db_path, db_type="sqlite", active=False):
        self.active = active
        self.sql = SQL.select_tables_in_db
        if '.log' in db_path:
            self.db_file = db_path.replace('.log', '.sqlite')
        else:
            self.db_file = db_path
        if any(db_type in s for s in ['ctb', 'sqlite3', 'db']):
            self.type = 'sqlite3'
        elif any(db_type in s for s in ['xml', 'xslt', 'rss']):
            self.type = 'xml'
        else:
            self.type = 'not_defined'
        if self.active:
            self.obj_conn = sqlite3.connect(db_path)
            print('succesfully connected to database ' + db_path)
        # else:
        #     print('database ' + db_path + ' without active connection')
        self.obj_list = self.return_many(SQL.select_tables_in_db)
        self.view_list = self.return_many(SQL.select_views_in_db)

    def result_set(self, sql, just_one=True):
        if self.active:
            execution = self.obj_conn.execute(sql)
            try:
                if just_one:
                    return execution.fetchone()
                else:
                    return execution.fetchall()
            except:
                return None
        else:
            try:
                conn = sqlite3.connect(self.db_file)
                if just_one:
                    result = conn.execute(sql).fetchone()
                else:
                    result = conn.execute(sql).fetchall()
                conn.close()
                return result
            except sqlite3.OperationalError:
                pass
                #print('error on: ' + sql)

    def execute(self, sql):
        try:
            if self.active:
                self.obj_conn.execute(sql)
                self.obj_conn.commit()
            else:
                conn = sqlite3.connect(self.db_file)
                conn.cursor().execute(sql)
                conn.commit()
                conn.close()
        except Exception as ex:
            print('some exception occured: ' + str(ex.args) + ': ' + sql)


    def return_one(self, sql):
        return self.result_set(sql, just_one=True)

    def return_many(self, sql):
        return self.result_set(sql, just_one=False)

    def return_field_content(self, table, field, condition):
        return self.return_one(SQL.select_where.format(field, table, condition))

    def object_exist(self, object_name):
        if self.return_one(SQL.table_exist.format(object_name))[0]:
            # print('object {0} exist'.format(object_name))
            return True
        else:
            # print('object {0} does not exist'.format(object_name))
            return False

    def object_structure(self, object_name, object_type=''):
        if not object_type:
            result = self.return_one(SQL.table_structure.format(object_name, object_name))[0]
        else:
            result = self.return_many(SQL.table_structure_type.format(object_name, object_name, object_type))[0]
        if result.lower().startswith('create view'):
            result = str(result).replace('\r\n', '').replace('\n', '')  # remove line breaks first
            result = str(result).replace(' from ', ' FROM ').replace(' select ', ' SELECT ').replace(' as ', ' AS ')
            print(result)
            full_field_list = result.split(' SELECT ')[1].split(' FROM ')[0].split(',')
            field_list = [field.split('.')[-1] for field in full_field_list]
        elif result.lower().startswith('create table'):
            field_list = result.split('(')[1].split(')')[0].split(',')
        # clear the list from spaces
        return [field.strip() for field in field_list]

    def object_create(self, object_name):
        if not self.return_one(SQL.table_exist.format(object_name)):
            print('creating object: ' + object_name)

    def object_all_rows(self, object_name):
        return self.return_many(SQL.select.format('*', object_name))

    def log_to_database(self, table_name, sql, ddl=''):
        time_stamp = sql.split('VALUES (')[-1].split(',')[-3].strip()
        object_name = sql.split('VALUES (')[-1].split(',')[0].strip()
        if not self.object_exist(table_name):
            if 'log' in table_name.lower():
                ddl_command = SQL.table_ddl_log
            elif 'dirlist' in table_name.lower():
                ddl_command = SQL.table_ddl_dir
            elif ddl:
                ddl_command = ddl
            else:
                print('please submit table ddl command, table not exist')

            self.execute(SQL.table_ddl.format(table_name, ddl_command))
            print('table ' + table_name + ' created')
        if not self.return_one(SQL.log_value_exist.format(table_name, time_stamp, object_name)):
            self.execute(sql)
        else:
            print('table {0} already contains ({1})'.format(table_name, time_stamp))

    def determine_id_col(self, table, field=''):
        i = 0
        for column in self.object_structure(table):
            if not field:
                if 'unique' in column.lower() or 'id' in column.lower():
                    if '\t' in column.split(' ')[0]:
                        column = column.replace('\t', ' ').replace('`', '').strip()
                    return column.split(' ')[0]
            else:
                if '\t' in column.split(' ')[0]:
                    column = column.replace('\t', ' ').replace('`', '').strip()
                if field == column.split(' ')[0]:
                    return i
                else:
                    i += 1


def compare_databases(db1, db2, concrete_table=''):
    db_left = DataBaseObject(db1)
    db_right = DataBaseObject(db2)

    table_list = db_left.obj_list
    if concrete_table:
        one_table_list = [x for x in table_list if concrete_table in x]
        table_list = one_table_list

    for table in table_list:
        print('*' * 100)
        print('*' * 100)
        if 'sqlite_sequence' in table:
            continue
        if not db_right.object_exist(table[0]):
            print('missing table "{0}" in {1}'.format(db1, db2))
        else:
            id_col = db_left.determine_id_col(table[0])
            id_col_id = db_left.determine_id_col(table[0], id_col)
            print("""table - {0} - ID column identified - {1}
            (index position {2})""".format(table[0], id_col, id_col_id))
            for row in db_left.object_all_rows(table[0]):
                where = id_col + ' = ' + str(row[id_col_id])
                col_num = 0
                for column in db_left.object_structure(table[0]):
                    if id_col in column or 'ts_' in column:
                        col_num += 1
                        continue
                    mirror = db_right.return_field_content(table[0], column.split(' ')[0], where)
                    if not mirror:
                        print('{0} !cannot get mirrored column: {1} for row: {2}'.format(' ' * 5, column, where))
                        continue
                    if difflib.SequenceMatcher(a=row[col_num].lower(), b=mirror[0].lower()).ratio() < 1:
                        try:
                            print('=' * 100)
                            print(row[col_num])
                            print('-' * 100)
                            print(mirror[0])
                            print('=' * 100)
                        except Exception as ex:
                            print(ex.args[0].replace('\n', ' '))
                            
                    col_num += 1


def get_query_type(sql, qry_type):
    """get table name from SQL text"""
    if qry_type == 'DDL':
        print('CREATE/DROP/ALTER/RENAME TABLE')
    elif qry_type == 'DML':
        print('INSERT/UPDATE/DELETE/SELECT TABLE')
    elif qry_type == 'DCL':
        print('GRANT/REVOKE')
    return 'sql result'


def temp_connect_database(database, do_some_work=''):
    # connect to database
    db = DataBaseObject(database, active=False)
    if not do_some_work:
        do_some_work = 'explore'
        print(db.obj_list)

