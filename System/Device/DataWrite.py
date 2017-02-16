""" 1st argument - what kind of data temp/rain/wind/all
2nd argument - where to write
3rd argument - where to present"""
import os
import sys
import argparse
import sqlite3
import datetime
from collections import OrderedDict

# get tepmerature
# argument devicefile is the path of the sensor to be read,
# returns None on error, or the temperature as a float
class DeviceControl(object):
    table_exist = """SELECT EXISTS(
        SELECT 1 FROM sqlite_master 
        WHERE type="table" AND name = "{0}"
    );"""
    table_cr_temp = """CREATE TABLE {0} ({1});"""
    get_settings = """SELECT drivertype, driverloc 
    FROM driver 
    WHERE device = (
        SELECT ID from device where devicename = '{0}'
    )"""
    get_structure = 'SELECT * FROM structure'
    value_exist = 'SELECT timestamp FROM {0} WHERE timestamp = {1};'
    value_select = 'SELECT {0} FROM {1} WHERE timestamp = {2};'
    value_insert = 'INSERT INTO {0} VALUES ({1});'
    value_update = 'UPDATE {0} SET {1} = {2} WHERE timestamp = {3};'

def get_time(timevalue):
    if (timevalue.minute - timevalue.minute%5) > 2:
        min_new = timevalue.minute - timevalue.minute%5 + 5
    else:
        min_new = timevalue.minute - timevalue.minute%5
    return datetime.datetime(timevalue.year, timevalue.month, timevalue.day, timevalue.hour, min_new, 0, 0)

def get_value(devicefile):
    """read value from device"""
    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None
    # get the status from the end of line 1 
    status = lines[0][-4:-1]
    # is the status is ok, get the temperature from line 2
    if status=="YES":
        print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        print tempvalue
        return tempvalue
    else:
        print "There was an error."
        return None

def log_value(measure, velocity, c, ins_qry):
    """store the value in the database
    measure - value which was measured
    velocity - type of measured value
    c - cursor in database being written
    col_vals - default column values"""
    # timestamp value - maybe parse?
    now = '"'+str(get_time(datetime.datetime.now()))+'"'
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
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help='db file', type=str, default='')
    parser.add_argument('-p', help='device name', type=str, default='')
    args = parser.parse_args()
    
    # create class for controlling device
    dev = DeviceControl()
    # load settings from settings db
    sdb = os.path.dirname(os.path.realpath(__file__)) + '/settings.db'
    conn = sqlite3.connect(sdb)
    c = conn.cursor()
    col_list = '' # columns - string to create table
    col_vals = {} # columns - default values to insert query
    for row in c.execute(dev.get_structure).fetchall():
        col_list += row[1] + ' ' + row[2] + ','
        col_vals[row[1]] = row[4]
    col_defa = OrderedDict(sorted(col_vals.items(), key=lambda x: x[1]))
    # print col_defa
    # get all drivers to read from device
    lst = c.execute(dev.get_settings.format(args.p)).fetchall()
    conn.close()
    # name of table
    table_name = 'measured'
    # create connection
    conn = sqlite3.connect(args.d)
    c = conn.cursor()
    # check if table exist - create new
    table_create = dev.table_cr_temp.format(table_name, col_list[:-2])
    if not c.execute(dev.table_exist.format(table_name)).fetchone()[0]:
        c.execute(table_create)
    # log value - perform get value from device first
    for velocity, driver in lst:
        ins_col = ''
        ins_val = ''
        i = 0
        for column, defa in col_defa.iteritems():
            ins_col += column + ', '
            if column in ('timestamp', 'device', velocity):
                ins_val += '{' + str(i) + '}, '
                i += 1
            else:
                ins_val += defa + ', '
        ins_col = table_name + ' (' + ins_col[:-2] + ')'
        print ins_col
        print ins_val
        ins_qry = dev.value_insert.format(ins_col, ins_val[:-2])
        print ins_qry
        # log_value(get_value(driver), velocity, c, ins_qry)
        #log_value(11, velocity, c, ins_qry)
    # finish changes
    conn.commit()
    conn.close()
else:
    print 'What is this file name? - ' + __name__
    print 'Something is wrong ...'
