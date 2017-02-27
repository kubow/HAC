"""Developped by Kube Kubow 2017
File contains class for controlling Device through sqlite settings
function get_time to round (aggregate) timestamp
function get_time_from_file to build date and time from file name
function to read CSV file content to a dictionary
function to write CSV file from downloaded data
and a logger module - currently not implemented
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
        hour_new = timevalue.hour
    else:
        min_new = minute - modulo
        if min_new > 58:
            hour_new = timevalue.hour + 1
            min_new = 0
        else:
            hour_new = timevalue.hour
    timevalue_aggregated = datetime.datetime(timevalue.year,
     timevalue.month, timevalue.day, hour_new, int(min_new), 0, 0)
    #print 'timestamp: ' + str(timevalue) + ' > ' + str(timevalue_aggregated)
    return timevalue_aggregated

def get_time_from_file(file):
    """build a date-time stamp from file name
    ... presuming structure <YYYYMMDD_hhmm>"""
    file_name = file.split('/')[-1]
    not_csv = file_name.split('.')[0]
    file_date = not_csv.split('_')[0]
    file_time = not_csv.split('_')[1]
    file_year = int(file_date[:4])
    file_month = int(file_date[4:6])
    file_day = int(file_date[6:])
    file_hour = int(file_time[:2])
    file_minute = int(file_time[2:])
    return datetime.datetime(file_year, file_month, file_day, file_hour, file_minute, 0)

def min_between(d1, d2):
    '''not used for now - just temp'''
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

def readCSV(csvfile):
    """read value from csv file
    return in dictionary"""
    try:
        fileobj = open(csvfile,'r')
        lines = fileobj.readlines()
        timestamp = get_time_from_file(csvfile)
        fileobj.close()
        # load field names as variables
        val = 0
        timestamps = {}
        flds = []  # field number
        vels = []  # velocities
        values = {}
        velocities = {}
        # load values to dictionary
        for row in lines:
            hd = row.split(',')
            if val == 0:
                # various columns save
                for i in range(len(hd)):
                    if hd[i] not in ('datetime', None, '\n'):
                        flds.append('val_'+str(i))
                        vels.append(hd[i].strip())
                        values['val_'+str(i)] = 0
                val += 1
            else:
                for fld in flds:
                    idx = int(fld.split('_')[-1])
                    values[fld] = int(values[fld]) + int(hd[idx])
                val += 1
        for field, sum_vals in values.iteritems():
            values[field] = sum_vals/val
            # get index of field - change to proper list
            velocities[vels[flds.index(field)]] = sum_vals/val
        timestamps[timestamp] = velocities
        return timestamps
    except Exception as ex:
        print ex.args[0]
        return None
