import argparse
import sqlite3

import SO74TX
from Template import SQL
from log import Log


class DataBaseObject:
    """db_path can be a log_file, it creates in sqlite in the same path"""
    def __init__(self, db_path, active=False):
        self.db_file = db_path.replace('.log', '.sqlite')
        self.type = 'sqlite3'
        self.active = active
        self.sql = SQL.select_tables_in_db
        self.obj_list = self.return_many(self.sql)
        if self.active:
            self.obj_conn = sqlite3.connect(db_path)

    def result_set(self, sql):
        if self.active:
            return self.obj_conn.execute(sql)
        else:
            return sqlite3.connect(self.db_file).execute(sql)

    def execute(self, sql):
        if self.active:
            self.obj_conn.execute(sql)
            self.obj_conn.commit()
        else:
            sqlite3.connect(self.db_file).execute(sql)
            sqlite3.connect(self.db_file).commit()

    def return_one(self, sql):
        return self.result_set(sql).fetchone()

    def return_many(self, sql):
        return self.result_set(sql).fetchall()

    def return_field_content(self, table, field, condition):
        return self.return_one(SQL.select_where.format(field, table, condition))

    def object_exist(self, object_name):
        if self.return_one(SQL.table_exist.format(object_name)):
            return True
        else:
            return False

    def object_structure(self, object_name, object_type=''):
        if not object_type:
            result = self.return_one(SQL.table_structure.format(object_name, object_name))[0]
        else:
            result = self.return_many(SQL.table_structure.format(object_name, object_type))[0]
        field_list = result.split('(')[1].split(')')[0].split(',')
        # clear the list from spaces
        return [field.strip() for field in field_list]

    def object_create(self, object_name):
        if not self.return_one(SQL.table_exist.format(object_name)):
            print 'creating object: ' + object_name

    def object_all_rows(self, object_name):
        return self.return_many(SQL.select.format('*', object_name))

    def log_to_database(self, table_name, sql):
        if not self.object_exist(table_name):
            print 'must create table (currently doing nothing...)'
        self.execute(sql)

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


def databases_compare(db1, db2, concrete_table=''):
    db_left = DataBaseObject(db1)
    db_right = DataBaseObject(db2)
    logger.log_operation('comparing databases: {0} / {1}'.format(db1, db2))

    table_list = db_left.obj_list
    if concrete_table:
        one_table_list = [x for x in table_list if concrete_table in x]
        table_list = one_table_list

    for table in table_list:
        print '*' * 100
        print '*' * 100
        if 'sqlite_sequence' in table:
            continue
        if not db_right.object_exist(table[0]):
            print 'missing table "{0}" in {1}'.format(db1, db2)
        else:
            id_col = db_left.determine_id_col(table[0])
            id_col_id = db_left.determine_id_col(table[0], id_col)
            print """table - {0} - ID column identified - {1}
            (index position {2})""".format(table[0], id_col, id_col_id)
            for row in db_left.object_all_rows(table[0]):
                where = id_col + ' = ' + str(row[id_col_id])
                col_num = 0
                for column in db_left.object_structure(table[0]):
                    if id_col in column or 'ts_' in column:
                        col_num += 1
                        continue
                    mirror = db_right.return_field_content(table[0], column.split(' ')[0], where)
                    if not mirror:
                        print '{0}!!cannot get mirrored column: {1} for row:'.format(' ' * 5, column, where)
                        continue
                    if SO74TX.similar(row[col_num], mirror[0]) < 1:
                        try:
                            print '=' * 100
                            print row[col_num]
                            print '-' * 100
                            print mirror[0]
                            print '=' * 100
                        except Exception as ex:
                            print ex.args[0].replace('\n', ' ')
                            
                    col_num += 1


def get_query_type(sql, qry_type):
    """get table name from SQL text"""
    if qry_type == 'DDL':
        print 'CREATE/DROP/ALTER/RENAME TABLE'
    elif qry_type == 'DML':
        print 'INSERT/UPDATE/DELETE/SELECT TABLE'
    elif qry_type == 'DCL':
        print 'GRANT/REVOKE'
    return 'sql result'


def temp_connect_database(database, do_some_work=''):
    # connect to database
    try:
        conn = open_db_connection(database)
        if not do_some_work:
            do_some_work = 'explore'
        # show the text menu
    except:
        print 'cannot find main db file! > ' + database + ' ?'
        # make connection to a temporary database?
        conn = sqlite3.connect(':memory:')
    finally:
        conn.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Compare two sqlite databases")
    parser.add_argument('-m', help='mode: compare/browse sqlite database', type=str, default='')
    parser.add_argument('-a', help='first file', type=str, default='') #l
    parser.add_argument('-b', help='second file', type=str, default='') #r
    parser.add_argument('-f', help='focus one table', type=str, default='')
    parser.add_argument('-l', help='log file', type=str, default='')
    args = parser.parse_args()
    logger = Log(args.l, 'Database', __file__, True)
    if 'compare' in args.m:
        databases_compare(args.a, args.b, args.f)
    else:
        temp_connect_database(args.a)
