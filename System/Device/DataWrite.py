""" File used to read all data downloaded from sensors
and aggregate to sqlite database
intermediate CSV files are being archived"""
import os
import sys
import shutil
import argparse
import sqlite3
import time
import datetime
#from collections import OrderedDict

# get tepmerature
# argument devicefile is the path of the sensor to be read,
# returns None on error, or the temperature as a float
import Control

def log_value(measure, velocity, c, ins_qry, timestamp):
    """store the value in the database
    measure - value which was measured
    velocity - type of measured value
    c - cursor in database being written
    insert query - query to insert/update
    timestamp - datetime value"""
    # timestamp value - maybe parse?
    now = '"'+str(timestamp)+'"'
    print '{0} - value - {1} ({2})'.format(now, str(measure), velocity)
    # prepare insert query
    fill_values = now+', '+str(measure)+', 0, 0, "0", 0, 0'
    column = '"' + velocity + '"'
    # check if row already exist
    value_select = dev.value_select.format(column, table_name, now)
    already = c.execute(value_select).fetchone()
    # print already
    if already:
        if already[0] <> measure:
            print """someting has happened - two different values
            for one timestamp {0}""".format(now)
        else:
            c.execute(dev.value_update.format(table_name, 'temp', already[0]+1, now))
    else:
        c.execute(ins_qry)

if __name__ == '__main__':
    start_time = time.clock()
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help='device name', type=str, default='')
    parser.add_argument('-l', help='location', type=str, default='')
    args = parser.parse_args()
    
    # create class for controlling device
    dev = Control.Device()
    # load settings from settings db
    sdb = os.path.dirname(os.path.realpath(__file__)) + '/settings.db'
    conn = sqlite3.connect(sdb)
    c = conn.cursor()
    # # build table structure
    col_list = '' # columns - string to create table
    col_vals = {} # columns - default values to insert query
    for row in c.execute(dev.get_structure).fetchall():
        col_list += row[1] + ' ' + row[2] + ','
        col_vals[row[1]] = row[4]
    # name of table being saved
    table_name = c.execute(dev.get_table_name).fetchone()[0]
    conn.close()
    
    # check if Archive directory present
    if not os.path.exists(args.l + 'Archive'):
        os.makedirs(args.l + 'Archive')
    
    # iterate csv files in given directory
    csv_cnt = 0 # counter for iterated files
    for csv_file in os.listdir(args.l):
        if csv_file.split('.')[-1].lower() <> 'csv':
            continue
            # only csv files
        # create connection to new database file
        base_name = args.l + csv_file[:6]
        conn = sqlite3.connect(base_name + '.sqlite')
        c = conn.cursor()
        # check if table exist - create new
        if not c.execute(dev.table_exist.format(table_name)).fetchone()[0]:
            table_create = dev.table_ddl.format(table_name, col_list[:-2])
            c.execute(table_create)
        # get csv file as dictionary
        ts = Control.readCSV(args.l + csv_file)
        if not ts:
            print '!!!!file was not proccessed ...'
            continue
        print 'file read: ' + args.l + csv_file
        csv_cnt += 1
        # timestamp = dictionary index 0
        for key, value in ts.iteritems():
            timestamp = key
        ts_exist = dev.value_exist.format(table_name, timestamp)
        # check if about to update or insert
        if not c.execute(ts_exist).fetchone():
            # construct insert query from device list
            ins_col = table_name + ' (timestamp, device'
            values = '"' + str(timestamp) + '", "' + args.d + '"'
            for timestamp_n, vals in ts.iteritems():
                for vel, val in vals.iteritems():
                    ins_col += ', ' + vel
                    values += ', "' + str(val) + '"'
            qry = dev.value_insert.format(ins_col + ')', values)
        else:
            # construct update query from device list
            values = ''
            for timestamp_n, vals in ts.iteritems():
                for vel, val in vals.iteritems():
                    values += vel + ' = "' + str(val) + '", '
            values = values[:-2]
            qry = dev.value_update.format(table_name, values, timestamp)
        # write values
        print qry
        c.execute(qry)
        conn.commit()
        # archive csv
        shutil.move(args.l + csv_file, args.l + 'Archive')
        print 'file archived ..'
        
    if csv_cnt < 1:
        print 'no csv files to proccess, running update'
        #json will be called here
    else:
        print 'processed ' + str(csv_cnt) + ' files'
    
    # todo: move below function to each cycle with sqlite database
    #write json
    Control.writeJSON(args.l, col_list, c)
    
    # finish changes
    conn.close()
    elapsed_time = time.clock() - start_time
    print "Time elapsed: {} seconds".format(elapsed_time)
else:
    print 'What is this file name? - ' + __name__
    print 'Something is wrong ...'
