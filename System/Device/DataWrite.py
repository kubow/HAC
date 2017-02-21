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
    table_ddl = 'CREATE TABLE {0} ({1});'
    get_settings = """SELECT drivertype, driverloc 
    FROM driver 
    WHERE device = (
        SELECT ID from device where devicename = '{0}'
    );"""
    get_device_spec = """SELECT * 
    FROM driver
    WHERE device = (
        SELECT ID from device where devicename = '{0}'
    ;"""
    get_structure = 'SELECT * FROM structure'
    get_table_name = 'SELECT table_name FROM setting'
    value_exist = 'SELECT timestamp FROM {0} WHERE timestamp = {1};'
    value_select = 'SELECT {0} FROM {1} WHERE timestamp = {2};'
    value_insert = 'INSERT INTO {0} VALUES ({1});'
    value_update = 'UPDATE {0} SET {1} WHERE timestamp = {2};'

def get_time(timevalue, modnum):
    """function to return rounded time
    second parameter aggregation time interval """
    # saving in <modnum> minute intervals
    minute = timevalue.minute + float(timevalue.second)/60
    modulo = float(minute%modnum)
    # decide where to put value
    if modulo >= float(modnum/2):
        min_new = minute - modulo + modnum
        # print str(modulo) + 'is greater than' + str(float(modnum/2))
    else:
        min_new = minute - modulo
        # print str(modulo) + 'is less than' + str(float(modnum/2))
    timevalue_aggregated = datetime.datetime(timevalue.year,
     timevalue.month, timevalue.day, timevalue.hour, int(min_new), 0, 0)
    print 'timestamp: ' + str(timevalue) + ' > ' + str(timevalue_aggregated)
    return timevalue_aggregated

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
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help='db file', type=str, default='')
    parser.add_argument('-p', help='device name', type=str, default='')
    args = parser.parse_args()
    
    # create class for controlling device
    dev = DeviceControl()
    # load settings from settings db
    now = datetime.datetime.now()
    sdb = os.path.dirname(os.path.realpath(__file__)) + '/settings.db'
    conn = sqlite3.connect(sdb)
    c = conn.cursor()
    # # build table structure
    col_list = '' # columns - string to create table
    col_vals = {} # columns - default values to insert query
    for row in c.execute(dev.get_structure).fetchall():
        col_list += row[1] + ' ' + row[2] + ','
        col_vals[row[1]] = row[4]
    col_defa = OrderedDict(sorted(col_vals.items(), key=lambda x: x[1]))
    # get all drivers to read from device
    lst = c.execute(dev.get_settings.format(args.p)).fetchall()
    # name of table being saved
    table_name = c.execute(dev.get_table_name).fetchone()[0]
    conn.close()
    # create connection to new database file
    conn = sqlite3.connect(args.d)
    c = conn.cursor()
    # check if table exist - create new
    if not c.execute(dev.table_exist.format(table_name)).fetchone()[0]:
        table_create = dev.table_ddl.format(table_name, col_list[:-2])
        c.execute(table_create)
    # get proper timestamp - check if exist in database
    timestamp = get_time(now, 2) #now rounded to two minutes
    ts_exist = dev.value_exist.format(table_name, timestamp)
    print ts_exist
    if not c.execute(ts_exist).fetchone()[0]:
        # construct insert query from device list
        ins_col = table_name + ' (timestamp, device'
        ins_val = '"' + str(timestamp) + '", "' + args.p + '"'
        for velocity, driver in lst:
            ins_col += ', ' + velocity
            #ins_val += ', ' + get_value(driver)
            ins_val += ', ' + str(11)
            # get value for driver
        qry = dev.value_insert.format(ins_col + ')', ins_val)
        # print str(timestamp) + ' - real time: ' + str(now)
        print qry
        # log_value(get_value(driver), velocity, c, ins_qry)
        #log_value(11, velocity, c, ins_qry, timestamp)
    else:
        # construct update query from device list
        upd_val = ''
        for velocity, driver in lst:
            upd_val += velocity + ' = ' + str(11) + ', '
    #write values
    c.execute(qry)
    # finish changes
    conn.commit()
    conn.close()
else:
    print 'What is this file name? - ' + __name__
    print 'Something is wrong ...'
