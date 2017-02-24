"""File contains class for 
"""
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
    
    
def writeCSV(location, name, header, values):
    """header - list of columns"""
    if os.path.exists(fileName):
        f = open(fileName, "a")
    else:
        f = open(fileName, "a+")
        for element in header:
          f.write(element + ",")
        f.write("\n")