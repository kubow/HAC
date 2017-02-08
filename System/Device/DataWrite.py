""" 1st argument - what kind of data temp/rain/wind/all
2nd argument - where to write
3rd argument - where to present"""
import sys
import argparse
import sqlite3
import datetime

# get tepmerature
# argument devicefile is the path of the sensor to be read,
# returns None on error, or the temperature as a float
class DeviceControl(object):
    table_exist = """SELECT EXISTS(
        SELECT 1 FROM sqlite_master 
        WHERE type="table" AND name = "{0}"
    );"""
    table_create = """CREATE TABLE {0} (
    timestamp text,
    temp number,
    humi number,
    fall number,
    windir text,
    windsp number,
    device number
    );"""
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
    """read """
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

def log_value(measure, column, dbname):
    """store the temperature in the database"""
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    now = '"'+str(get_time(datetime.datetime.now()))+'"'
    print str(now) + ' - value - ' + str(measure)
    table_name = 'measured'
    fill_values = now+', '+str(measure)+', 0, 0, "0", 0, 0'
    # check if table exist
    if not curs.execute(dev.table_exist.format(table_name)).fetchone()[0]:
        curs.execute(dev.table_create.format(table_name))
    # check if row already exist
    print curs.execute(dev.value_select.format(column, table_name, now)).fetchone()
    already = curs.execute(dev.value_select.format(column, table_name, now)).fetchone()
    if already:
        if already[0] <> measure:
            print """someting has happened - two different values 
            for one timestamp {0}""".format(now)
        else:
            curs.execute(dev.value_update.format(table_name, 'temp', already[0]+1, now))
    else:
        curs.execute(dev.value_insert.format(table_name, fill_values))
    # commit the changes
    conn.commit()
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check difference of two files")
    parser.add_argument('-d', help='database file', type=str, default='')
    parser.add_argument('-p', help='device path', type=str, default='')
    args = parser.parse_args()

    # create class for controlling device
    dev=DeviceControl()
    # log value
    log_value(11, '"temp"', args.d)
    # dev.log_value(get_value(args.p), args.d)
else:
    print 'no database submitted'
