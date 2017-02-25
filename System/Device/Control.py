"""File contains class for controlling Device through sqlite settings
function get_time to round 
"""
import os
import time
import datetime

class Device(object):
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
    get_driver_loc = """SELECT driverloc 
    FROM driver 
    WHERE device = {0} AND drivertype = "{1}";"""
    get_device_id = '(SELECT ID from device WHERE devicename ="{0}")'
    get_structure = 'SELECT * FROM structure'
    get_table_name = 'SELECT table_name FROM setting;'
    value_exist = 'SELECT timestamp FROM {0} WHERE timestamp = "{1}";'
    value_select = 'SELECT {0} FROM {1} WHERE timestamp = "{2}";'
    value_insert = 'INSERT INTO {0} VALUES ({1});'
    value_update = 'UPDATE {0} SET {1} WHERE timestamp = "{2}";'
    date_format = '%Y/%m/%d %H:%M:%S'
    date_file_format = '%Y%m%d_%H%M'
    
    
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
    #print 'timestamp: ' + str(timevalue) + ' > ' + str(timevalue_aggregated)
    return timevalue_aggregated

def min_between(d1, d2):
    #d1 = datetime.strptime(d1, "%Y-%m-%d")
    #d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs(d2 - d1)    
    
def writeCSV(file_name, values, timestamp, device):
    """write a CSV file
    values - in dictionary
    timestamp of exact time measured
    device - which perform data read"""
    if os.path.exists(file_name):
        f = open(file_name, "a")
    else:
        f = open(file_name, "a+")
        line = 1
        # write time series and header
        for actime, vals in values.iteritems():
            row = ''
            if line == 1:
                for d, v in vals.iteritems():
                    row += str(d) + ','
                row = 'datetime, ' + row
                f.write(row + "\n")
            row = str(actime) + ','
            for d, v in vals.iteritems():
                row += str(v) + ','
            f.write(row+"\n")
            line += 1
    f.close()
