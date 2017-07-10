import os, sys
import argparse
import sqlite3

import TX74
import log


def get_table_name(sql, qry_type):
    """get table name from SQL text"""
    if qry_type == 'DDL':
        print 'CREATE/DROP/ALTER/RENAME TABLE'
    elif qry_type == 'DML':
        print 'INSERT/UPDATE/DELETE/SELECT TABLE'
    elif qry_type == 'DCL':
        print 'GRANT/REVOKE'
    return 'sql result'


def execute_not_connected(database, sql):
    """execute command and return dataset"""
    conn = sqlite3.connect(database)
    curs = conn.execute(sql)
    res_set = curs.fetchall()
    # log.log_operation(logfile, module, 'executed SQL: {0}'.format(sql))
    conn.close()
    if res_set:
        print res_set
        return res_set[0]
    else:
        print 'no node connected'
        return None


def fetch_one_from_tab(c, sql):
    result = c.execute(sql).fetch_one()
    if result:
        return result[0]
    else:
        return None


def execute_connected(c, sql, logfile, module, debug=False):
    """execute a command withon already connected database
    c - connected cursor (preferably sqlite datbase)
    sql - command to be executed
    module - that calls the execution
    logfile - that logs the stament
    """
    if debug:
        log.log_operation(logfile, module, 'executing SQL: {0}'.format(sql))
    # main logic to distinguish between query types
    if 'CREATE TABLE' in sql or 'DROP TABLE' in sql:
        qry_type = 'DDL'
        table_name = get_table_name(sql, qry_type)
        log.log_operation(logfile, module, 'modyfing table: {0}'.format(table_name))
    elif 'INSERT' in sql or 'UPDATE' in sql or 'DELETE' in sql:
        qry_type = 'DML'
        table_name = get_table_name(sql, qry_type)
    elif 'SELECT' in sql:
        qry_type = 'DML'
        table_name = get_table_name(sql, qry_type)
    else:
        print 'some bad happened, cannot find qery type'
    c.execute()
    if debug:
        log.log_operation(logfile, module, 'executed SQL: {0}'.format(sql))


def temp_connect_database(database):
    # connect to database
    try:
        conn = sqlite3.connect(database)
        # show the text menu
    except:
        print 'cannot find main db file! > ' + database + ' ?'
        # make connection to a temporary database?
        conn = sqlite3.connect(':memory:')
    finally:
        conn.close()

def open_db_connection(path):
    conn = sqlite3.connect(path)
    # conn.row_factory = sqlite3.Row
    print "Openned database %s as %r" % (path, conn)
    return conn
    
def close_db_connection(conn):
    try:
        conn.close()
    except:
        print "connection cannot be closed"

def databases_compare(db1, db2):
    db_left = sqlite3.connect(db1).cursor()
    db_right = sqlite3.connect(db2).cursor()

    table_list = get_db_objects_list(db_left)

    for table in table_list:
        if 'sqlite_sequence' in table:
            continue
        if not db_object_exist(table[0], db_right):
            print 'missing table {0} in {1}'.format(db_right, db2)
        else:
            id_col = determine_id_col(table[0], db_left)
            id_col_id = get_field_index(id_col, table[0], db_left)
            print """table - {0} - ID column identified - {1}
            (index position {2})""".format(table[0], id_col, id_col_id)
            for row in get_table_rows(table[0], db_left):
                where = id_col + ' = ' + str(row[id_col_id])
                col_num = 0
                for column in get_table_structure(table[0], db_left):
                    if id_col in column:
                        col_num += 1
                        continue
                    mirror = get_field_content(where,
                                               column.split(' ')[0], table[0], db_right)
                    diff = TX74.similar(row[col_num], mirror[0])
                    if diff < 1:
                        print '!!! difference !!!'
                    col_num += 1


def get_db_objects_list(db):
    return db.execute("""SELECT tbl_name, type
        FROM sqlite_master
        WHERE type = "table"
        ;""").fetchall()


def db_object_exist(obj_name, db):
    return db.execute("""SELECT EXISTS(
        SELECT 1 FROM sqlite_master
        WHERE type = "table" AND name = "{0}"
        );""".format(obj_name)).fetchone()


def get_table_rows(table, db):
    return db.execute("SELECT * FROM {0};".format(table))


def get_field_content(condition, field, table, db):
    return db.execute("""SELECT {0} FROM {1}
        WHERE {2}""".format(field, table, condition)).fetchone()


def determine_id_col(table, db):
    for field in get_table_structure(table, db):
        if 'unique' in field.lower() or 'id' in field.lower():
            if '\t' in field.split(' ')[0]:
                field = field.replace('\t', ' ').replace('`', '').strip()
            return field.split(' ')[0]


def get_field_index(field, table, db):
    i = 0
    for column in get_table_structure(table, db):
        if '\t' in column.split(' ')[0]:
            column = column.replace('\t', ' ').replace('`', '').strip()
        if field == column.split(' ')[0]:
            return i
        else:
            i += 1


def get_table_structure(table, db):
    definition = db.execute("""SELECT sql FROM sqlite_master
        WHERE tbl_name = "{0}" and name = "{1}"
        """.format(table, table)).fetchone()[0].replace('\n', '')
    field_list = definition.split('(')[1].split(')')[0].split(',')
    # clear the list from spaces
    return [field.strip() for field in field_list]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare two sqlite databases")
    parser.add_argument('-l', help='first file', type=str, default='')
    parser.add_argument('-r', help='second file', type=str, default='')
    args = parser.parse_args()

    databases_compare(args.l, args.r)
