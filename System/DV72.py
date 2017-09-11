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
from OS74 import FileSystemObject, CurrentPlatform, DateTimeObject


class Device(object):
    def __init__(self):
        self.date_format = '%Y/%m/%d %H:%M:%S'
        self.date_file_format = '%Y%m%d_%H%M'
        local_path = os.path.dirname(os.path.realpath(__file__))
        self.setup_db = local_path + '/Settings.sqlite'
        self.port = 0
        self.br = 0
        self.timeout = 0
        self.interval_shift = 2
        self.table_name = '_'
        self.output_path = local_path
        current_device = CurrentPlatform()
        self.device_name = current_device.hostname
        self.device_user = current_device.environment
        self.device_platform = current_device.main

    def setup_device(self, device, sensor, timeout):
        if FileSystemObject(self.setup_db).is_file:
            dbc = DataBaseObject(self.setup_db)
            # port = port with device
            self.port = dbc.return_one(SQL.get_driver_loc.format(SQL.get_device_id.format(device), sensor))
            # br = baud rate
            self.br = dbc.return_one(SQL.select.format('baud', 'setting'))
            # table name, that will hold values
            self.table_name = dbc.return_one(SQL.select.format('table_name', 'setting'))
        else:
            # no available config - using default values
            self.port = 'COM4'
            self.br = 9600
            self.table_name = 'measured'
        # timeout waiting time
        self.timeout = timeout

    def setup_output_path(self, path):
        self.output_path = path
        
    def read_serial(self):
        """reading serial line and mirror it to CSV file"""
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
            # received = ser.readline().replace('\r\n', ' ')  # not used - instead
            to_read = ser.inWaiting()
            received = ser.read(to_read)
            # parse data / now = rounded to x min intervals
            if len(received) >= 1:
                vel_val = received.split(':')
                just_now = datetime.datetime.now()
                now = get_time(just_now, self.interval_shift)
                csv_fname = now.strftime(dev.date_file_format)+'.csv'
                csv = args.l + csv_fname
                # checking interval shifts
                if now > last_run:
                    CsvFile(csv, True, data_vals)
                    data_vals = {}  # clear the dictionaries
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
        fs = FileSystemObject(self.output_path + 'Measured')
        csv_cnt = 0
        for csv_file in fs.object_read():
            if not DataBaseObject(fs.append_file(csv_file[:6] + '.sqlite')).object_exist(self.table_name):
                print 'must create table first'
            csv_cnt += 1
            for time_stamp, value in CsvFile(fs.append_file(csv_file), read=True).content.iteritems():
                self.process_time_series()
        if csv_cnt < 1:
            print 'no csv files proccessed ...'
                
    def process_time_series(self, values):
        for vel, val in values.iteritems():
            print vel + val  # save to database


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

    
def min_between(d1, d2):
    """not used for now - just temp"""
    # d1 = datetime.strptime(d1, "%Y-%m-%d")
    # d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs(d2 - d1)
        
        
if __name__ == '__main__':

    from SO74DB import DataBaseObject

    from SO74TX import CsvFile
    from Template import SQL
    from log import Log

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
    FileSystemObject(args.l).object_create_neccesary()
    last_run = args.l + 'last.run'
    if not FileSystemObject(last_run).is_file:
        FileSystemObject(last_run).touch_file()
    # create class for controlling device # logging
    dev = Device()
    print args.l + ' / '+ FileSystemObject(args.l).one_dir_up() + 'logfile.log' 
    log_file = FileSystemObject(args.l).one_dir_up() + 'logfile.log'
    logger = Log(log_file, 'device', 'DV72.py',  True)
    # device settings: port, baud rate and timeout
    dev.setup_device(args.d, args.s, 0)
    dev.setup_output_path(args.l)
    # log sql (debug) print sql
    
    if 'read' in args.m or 'ser' in args.m:
        text = 'Reading serial input from: {0} - at {1}'.format(str(dev.port),str(dev.br))
        logger.log_operation(text)
        ready = True
        # compute last read time distance
        FileSystemObject(last_run).touch_file()
        while ready:
            ready = dev.read_serial()
    elif 'agg' in args.m:
        text = 'aggregating values in {0}, last run: {1}'.format(args.l, str(FileSystemObject(last_run).object_mod_date('%Y/%m/%d %H:%M:%S')))
        logger.log_operation(text)
        dev.write_to_database('now', 0, 'm/s')
    else:
        print 'not possible'
