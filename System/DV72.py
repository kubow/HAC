"""Developped by Kube Kubow 2017
File contains class for controlling Device through sqlite settings
function get_time to round (aggregate) timestamp
function get_time_from_file to build date and time from file name
function to read CSV/JSON file content to a dictionary
function to write CSV/JSON file from downloaded data
and a logger module - currently not implemented
"""
import os
import time
import datetime
import serial
import argparse

import DB74
import TX74
from Template import SQL


class Device(object):
    def __init__(self):
        self.date_format = '%Y/%m/%d %H:%M:%S'
        self.date_file_format = '%Y%m%d_%H%M'
        self.setup_db = os.path.dirname(os.path.realpath(__file__)) + '/Settings.sqlite'
    
    def setup_device(self, device, sensor, timeout):
        conn = DB74.open_db_connection(self.setup_db)
        c = conn.cursor()
        # port = port with device
        sql = SQL.get_driver_loc
        sub_sql = SQL.get_device_id.format(device)
        sql = sql.format(sub_sql, sensor)
        port = c.execute(sql).fetchone()[0]
        # br = baud rate
        sql = 'SELECT baud FROM setting;'
        br = c.execute(sql).fetchone()[0]
        DB74.close_db_connection(conn)
        self.port = port
        self.br = br
        self.timeout = timeout
        self.interval_shift = 2

    def setup_output_path(self, path):
        self.output_path = path
        
    def read_serial(self):
        data_vals = {} #dictionary holding all/interval values
        data_int = {} # clear the dictionary
        last_run = get_time(datetime.datetime.now(), self.interval_shift)
        csv = ''
        ser = serial.Serial(self.port, self.br, timeout=self.timeout)
        ser.flushInput()
        ser.flushOutput()
        try:
            time.sleep(self.timeout)
            print 'running with timeout {0} seconds.'.format(self.timeout)
            #received = ser.readline().replace('\r\n', ' ') #not used - instead
            to_read = ser.inWaiting()
            received = ser.read(to_read)
            # parse data
            if len(received) >= 1:
                vel_val = received.split(':')
                just_now = datetime.datetime.now()
                now = get_time(just_now, self.interval_shift)
                csv_fname = now.strftime(dev.date_file_format)+'.csv'
                # checking interval shifts
                if now > last_run:
                    TX74.writeCSV(csv, data_vals, just_now, 'RPi')
                    data_vals = {} # clear the dictionaries 
                    data_int = {} 
                    last_run = now
                csv = args.l + csv_fname
                print received + str(just_now.strftime(SQL.date_format))
                #building dictionary
                data_int[vel_val[0]] = vel_val[-1]
                data_vals[just_now.strftime(SQL.date_format)] = data_int 
                return 
            else:
                print 'received no text !!!!'
                return None
        except Exception as ex:
            print ex.args[0].replace('\n', ' ')
            print 'now '+ str(now)
            print 'last_run' + str(last_run)
            #if error found, do timeout
            #print data_vals
            #raw_input("Press enter to continue")
            #os.system("pause")
            return None
    
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
    file_name = file.replace('\\', '/').split('/')[-1]
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
        
        
if __name__ == '__main__':
    argd = 'device name reading data'
    argz = 'sensor name'
    argl = 'location to write final data'
    
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help=argd, type=str, default='')
    parser.add_argument('-s', help=argz, type=str, default='')
    parser.add_argument('-l', help=argl, type=str, default='')
    args = parser.parse_args()
    
    # create class for controlling device
    dev = Device()
    # device settings: port, baud rate and timeout
    dev.setup_device(args.d, args.s, 0)
    dev.setup_output_path(args.l)
    # log sql (debug) print sql
    
    print 'Reading serial input from: {0} - at {1}'.format(str(dev.port),str(dev.br))
    while 1:
        dev.read_serial()
        