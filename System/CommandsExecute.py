import os, syss
import argparse
import sqlite3
import log

def get_table_name(sql, qry_type):
    """get table name from SQL text"""
    if qry_type == 'DDL':
        print 'CREATE/DROP/ALTER/RENAME TABLE'
    elif qry == 'DML':
        print 'INSERT/UPDATE/DELETE/SELECT TABLE'
    elif qry == 'DCL':
        print 'GRANT/REVOKE'
    return table_name

def execute_connected(c, sql, logfile, module, debug=False):
    """execute a command withon already connected database
    c - connected cursor (preferably sqlite datbase)
    sql - command to be executed
    module - that calls the execution
    logfile - that logs the stament
    """
    if debug:
        log.file_write(logfile, module, 'executing SQL: {0}'.format(sql))
    # main logic to distinguish between query types
    if 'CREATE TABLE' in sql or 'DROP TABLE' in sql:
        qry_type = 'DDL'
        table_name = get_table_name(sql, qry_type)
        log.file_write(logfile, module, 'modyfing table: {0}'.format(table_name))
    elif 'INSERT' in sql or 'UPDATE' in sql or 'DELETE' in sql:
        qry_type = 'DML'
        table_name = get_table_name(sql, qry_type)
    elif 'SELECT' in sql:
        qry_type = 'DML'
        table_name = get_table_name(sql, qry_type)
    else:
        print 'some bad happened'
    c.execute()
    if debug:
        log.file_write(logfile, module, 'executed SQL: {0}'.format(sql))
