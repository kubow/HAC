import sys
import sqlite3
# get tepmerature
# argument devicefile is the path of the sensor to be read,
# returns None on error, or the temperature as a float
class DeviceControl(object):
    table_exist = """SELECT EXISTS(SELECT 1 FROM sqlite_master 
    WHERE type="table" AND name = "{0}");"""
    table_create = """CREATE TABLE {0} 
    (timestamp text
    , temp number
    , humi number
    , fall number
    , windir text
    , windsp number
    , device number
    );"""
    value_exist = 'SELECT timestamp FROM {0} WHERE timestamp = {1};'
    value_select = 'SELECT {0} FROM {1} WHERE timestamp = {2};'
    value_insert = 'INSERT INTO {0} VALUES ({1});'
    value_update = 'UPDATE {0} SET {1} = {2} WHERE timestamp = {3};'
    
def get_temp(devicefile):
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

# store the temperature in the database
def log_temperature(measure, column, dbname):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    now = "02.02.2017 15:50"
    table_name = 'measured'
    fill_values = '"now", '+str(measure)+', 0, 0, "0", 0, 0'
    # check if table exist
    if not curs.execute(dev.table_exist.format(table_name)).fetchone()[0]:
        curs.execute(dev.table_create.format(table_name))
    # check if row already exist
    print curs.execute(dev.value_select.format(column, table_name, '"now"')).fetchone()
    already = curs.execute(dev.value_select.format(column, table_name, '"now"')).fetchone()
    if already:
        if already[0] <> measure:
            print """someting has happened - two different values 
            for one timestamp {0}""".format('now')
        else:
            curs.execute(dev.value_update.format(table_name, 'temp', already[0]+1, '"now"'))
    else:
        curs.execute(dev.value_insert.format(table_name, fill_values))
    # commit the changes
    conn.commit()
    conn.close()

dev=DeviceControl()
print '**************************'
print sys.argv
print '**************************'
if sys.argv > 2:
    log_temperature(11, '"temp"', sys.argv[1])
    # dev.log_temperature(get_temp(sys.argv[2]), sys.argv[1])
else:
    print 'no database submitted'
