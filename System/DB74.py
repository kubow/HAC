import os, sys
import argparse
import sqlite3
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