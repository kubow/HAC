import argparse
import sqlite3

def open_db_connection(path):
    # conn.row_factory = sqlite3.Row
    # print "Opened database %s" % (path)
    return sqlite3.connect(path)


def close_db_connection(conn):
    try:
        print "Properly closing " + conn
        conn.close()
    except:
        print "connection cannot be closed"


def get_db_objects_list(db):
    return db.execute(SQL.select_tables_in_db()).fetchall()

    
def db_object_exist_noconnect(obj_name, db_name):
    conn = open_db_connection(db_name)
    exists = db_object_exist(obj_name, conn)
    close_db_connection(conn)
    return exists


def db_object_exist(obj_name, db):
    return db.execute(SQL.table_exist.format(obj_name)).fetchone()


def get_table_structure(table, db):
    definition = db.execute("""SELECT sql FROM sqlite_master
        WHERE tbl_name = "{0}" and name = "{1}"
        """.format(table, table)).fetchone()[0].replace('\n', '')
    field_list = definition.split('(')[1].split(')')[0].split(',')
    # clear the list from spaces
    return [field.strip() for field in field_list]


def fetch_one_from_tab(c, sql):
    result = c.execute(sql).fetch_one()
    if result:
        return result[0]
    else:
        return None


def execute_not_connected(database, sql):
    """execute command and return data set"""
    try:
        conn = open_db_connection(database)
        curs = conn.execute(sql)
        conn.commit()
        res_set = curs.fetchone()
        # log.log_operation('executed SQL (return one row): {0}'.format(sql))
        conn.close()
        if res_set:
            # print res_set
            return res_set[0]
        else:
            # print 'no node connected'
            return None
    except sqlite3.OperationalError:
        print 'cannot fetch dataset'
        return None
    except:
        print 'cannot find the database'
        return None

        
def execute_many_not_connected(database, sql):
    """execute command and return data set"""
    conn = open_db_connection(database)
    curs = conn.execute(sql)
    res_set = curs.fetchall()
    # log.log_operation(logfile, module, 'executed SQL: {0}'.format(sql))
    conn.close()
    
    return res_set


def log_to_database(db_path, table_name, sql):
    try:
        if not db_object_exist_noconnect(table_name, db_path):
            print 'must create table (currently doing nothing...)'
        # execute the query
        execute_not_connected(db_path, sql)
    except:
        print 'logging failed (to database {0})'.format(db_path)



def execute_connected(c, sql, logfile, module, debug=False):
    """execute a command on already connected database
    c - connected cursor (preferably sqlite database)
    sql - command to be executed
    module - that calls the execution
    logfile - that logs the statement
    """
    logger = Log(logfile, module)
    if debug:
        logger.log_operation('executing SQL: {0}'.format(sql))
    # main logic to distinguish between query types
    if 'CREATE TABLE' in sql or 'DROP TABLE' in sql:
        qry_type = 'DDL'
    elif 'INSERT' in sql or 'UPDATE' in sql or 'DELETE' in sql:
        qry_type = 'DML'
    else:
        # must be select
        qry_type = 'DML'
    table_name = SQL.get_table_name(sql, qry_type)

    c.execute()
    if debug:
        logger.log_operation('executed SQL: {0}'.format(sql))
        logger.log_operation('affected table: {0}'.format(table_name))


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


def databases_compare(db1, db2):
    db_left = open_db_connection(db1).cursor()
    db_right = open_db_connection(db2).cursor()

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
                    if SO74TX.similar(row[col_num], mirror[0]) < 1:
                        print '!!! difference !!!'
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

    import SO74TX
    from Template import SQL
    from log import Log

    parser = argparse.ArgumentParser(description="Compare two sqlite databases")
    parser.add_argument('-m', help='mode: compare/browse sqlite database', type=str, default='')
    parser.add_argument('-l', help='first file', type=str, default='')
    parser.add_argument('-r', help='second file', type=str, default='')
    args = parser.parse_args()
    if 'compare' in args.m:
        databases_compare(args.l, args.r)
    else:
        temp_connect_database(args.l)
