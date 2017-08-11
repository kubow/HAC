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
import OS74
import TX74
from Template import SQL


class Device(object):
    def __init__(self):
        self.date_format = '%Y/%m/%d %H:%M:%S'
        self.date_file_format = '%Y%m%d_%H%M'
        self.setup_db = os.path.dirname(os.path.realpath(__file__)) + '/Settings.sqlite'
        self.port = 0
        self.br = 0
        self.timeout = 0
        self.interval_shift = 2
        self.table_name = '_'
        self.output_path = os.path.dirname(os.path.realpath(__file__))

    def setup_device(self, device, sensor, timeout):
        # port = port with device
        sub_sql = SQL.get_device_id.format(device)
        sql = SQL.get_driver_loc.format(sub_sql, sensor)
        self.port = DB74.execute_not_connected(self.setup_db, sql)
        # br = baud rate
        self.br = DB74.execute_not_connected(self.setup_db, 'SELECT baud FROM setting;')
        # timeout waiting time
        self.timeout = timeout
        self.table_name = DB74.execute_not_connected(self.setup_db, 'SELECT table_name FROM setting;')

    def setup_output_path(self, path):
        self.output_path = path
        
    def read_serial(self):
        '''reading serial line and mirror it to CSV file'''
        data_vals = {}  # dictionary holding all/interval values
        data_int = {}  # clear the dictionary
        last_run = get_time(datetime.datetime.now(), self.interval_shift)
        csv = ''
        try:
            ser = serial.Serial(self.port, self.br, timeout=self.timeout)
            ser.flushInput()
            ser.flushOutput()
            time.sleep(self.timeout)
            print 'running with timeout {0} seconds.'.format(self.timeout)
            # received = ser.readline().replace('\r\n', ' ') #not used - instead
            to_read = ser.inWaiting()
            received = ser.read(to_read)
            # parse data
            if len(received) >= 1:
                vel_val = received.split(':')
                just_now = datetime.datetime.now()
                now = get_time(just_now, self.interval_shift)
                csv_fname = now.strftime(dev.date_file_format)+'.csv'
                csv = args.l + csv_fname
                # checking interval shifts
                if now > last_run:
                    TX74.writeCSV(csv, data_vals, just_now, 'RPi')
                    data_vals = {} # clear the dictionaries 
                    data_int = {} 
                    last_run = now

                print received + str(just_now.strftime(SQL.date_format))
                # building dictionary
                data_int[vel_val[0]] = vel_val[-1]
                data_vals[just_now.strftime(SQL.date_format)] = data_int 
                return data_vals
            else:
                print 'received no text !!!!'
                return None
        except serial.SerialException as se:
            print se.args
            print 'serial communication not accesible!'
            return None
        except Exception as ex:
            print ex.args[0].replace('\n', ' ')
            print 'now '+ str(now)
            print 'last_run' + str(last_run)
            # if error found, do timeout
            # print data_vals
            # raw_input("Press enter to continue")
            # os.system("pause")
            return None

    def write_to_database(self, timestamp, value, velocity):
        # check if Archive directory present
        if not os.path.exists(self.output_path + 'Archive'):
            os.makedirs(self.output_path + 'Archive')
        csv_cnt = 0
        for csv_file in os.listdir(self.output_path):
            if csv_file.split('.')[-1].lower() <> 'csv':
                continue
                # only csv files
            ts = TX74.readCSV(self.output_path + csv_file)
            if not DB74.db_object_exist_noconnect(self.table_name, self.output_path + csv_file[:6] + '.sqlite'):
                print 'must create table first'
            csv_cnt += 1



def get_time(timevalue, modnum):
    """function to return rounded time
    second parameter aggregation time interval """
    # saving in <modnum> minute intervals
    minute = timevalue.minute + float(timevalue.second)/60
    modulo = float(minute%modnum)
    # decide where to put value
    if modulo >= float(modnum/2):
        min_new = minute - modulo + modnum
        print min_new
        hour_new = timevalue.hour
    else:
        min_new = minute - modulo
        if min_new > 58:
            hour_new = timevalue.hour + 1
            min_new = 0
        else:
            hour_new = timevalue.hour
    value_aggregated = datetime.datetime(timevalue.year,
     timevalue.month, timevalue.day, hour_new, int(min_new), 0, 0)
    # print 'timestamp: ' + str(timevalue) + ' > ' + str(value_aggregated)
    return value_aggregated

    
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
    """not used for now - just temp"""
    # d1 = datetime.strptime(d1, "%Y-%m-%d")
    # d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs(d2 - d1)
        
        
if __name__ == '__main__':
    argd = 'device name reading data'
    argz = 'sensor name'
    argl = 'location to write final data'
    argm = 'mode (read serial/aggregate values)'
    
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help=argd, type=str, default='')
    parser.add_argument('-s', help=argz, type=str, default='')
    parser.add_argument('-l', help=argl, type=str, default='')
    parser.add_argument('-m', help=argl, type=str, default='')
    args = parser.parse_args()
    last_run = args.l + 'last.run'
    if not OS74.is_file(last_run):
        OS74.touch_file(last_run)
    # create class for controlling device
    dev = Device()
    # device settings: port, baud rate and timeout
    dev.setup_device(args.d, args.s, 0)
    dev.setup_output_path(args.l)
    # log sql (debug) print sql
    
    if 'read' in args.m or 'ser' in args.m:
        print 'Reading serial input from: {0} - at {1}'.format(str(dev.port),str(dev.br))
        ready = True
        # compute last read time distance
        OS74.touch_file(last_run)
        while ready:
            ready = dev.read_serial()
    elif 'agg' in args.m:
        print 'aggregating values in {0}'.format(args.l)
        print 'last run ' + str(OS74.get_file_mod_date(last_run, '%Y/%m/%d %H:%M:%S'))
        dev.write_to_database('now', 0, 'm/s')
    else:
        print 'not possible'