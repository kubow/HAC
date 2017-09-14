"""Developped by Kube Kubow 2017
File contains class for controlling Device through sqlite settings
Class Device with these functions:
function time_aggregated to round (aggregate) timestamp
function time_aggregated_from_file to build date and time from file name
function to read CSV/JSON file content to a dictionary
function to write CSV/JSON file from downloaded data
and a logger module - currently not implemented
"""
import os
import time
import datetime
import serial
import argparse


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
        self.csv_file = ''
        self.last_run = FileSystemObject(self.output_path + 'last.run').object_mod_date(self.date_format)
        self.device_name = CurrentPlatform().hostname
        self.device_user = CurrentPlatform().environment
        self.device_platform = CurrentPlatform().main

    def setup_device(self, device, sensor=None, timeout=0):
        if FileSystemObject(self.setup_db).is_file:
            dbc = DataBaseObject(self.setup_db)
            # table name, that will hold values
            self.table_name = dbc.return_one(SQL.select.format('table_name', 'setting'))[0]
            # match device name, platform
            for device_check in dbc.return_many(SQL.get_device_name_list):
                if not str(device_check[0]).lower() in self.device_name.lower():
                    continue
                else:
                    self.port = dbc.return_one(SQL.get_driver_loc.format(device_check[0]))[0]
                    self.br = dbc.return_one(SQL.get_driver_br.format(device_check[0]))[0]
                    break
            if not self.port:
                self.port = dbc.return_one(SQL.get_driver_dummy_loc.format(self.device_platform))[0]
            if not self.br:
                self.br = dbc.return_one(SQL.get_driver_dummy_loc.format(self.device_platform))[0]
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
        ac_time = datetime.datetime.now()
        data_vals = {}  # dictionary holding all/interval values
        just_now = ac_time.strftime(self.date_format)
        now = self.time_aggregated(just_now)
        just_now_file = now.strftime(self.date_file_format)
        #last_run = time_aggregated(just_now, self.interval_shift)
        csv = self.output_path + 'Measured/' + just_now_file + '.csv'
        try:
            ser = serial.Serial(self.port, self.br, timeout=self.timeout)
            ser.flushInput()
            ser.flushOutput()
            time.sleep(5)
            # received = ser.readline().replace('\r\n', ' ')  # not used - instead read a stack, average with one ts
            to_read = ser.inWaiting()
            received = ser.read(to_read)
            # parse data / now = rounded to x min intervals
            if len(received) >= 1:
                data_vals[just_now] = dict(item.split(":") for item in received.split("\r\n") if len(item) > 1)
                # for row in received.split('\r\n'):
                # checking interval shifts
                CsvFile(csv, write=True, content=data_vals)
                print data_vals
                return data_vals
            else:
                print 'no text to receive ...'
                return 'some values might come ...'
        except serial.SerialException as se:
            print se.args
            print 'serial communication not accesible!'
            return None
        except Exception as ex:
            print ex.args[0].replace('\n', ' ')
            print 'timeframe now : '+ str(now) + ' / ' + 'last_run' + str(self.last_run)
            # if error found, do timeout
            # print data_vals
            # raw_input("Press enter to continue")
            # os.system("pause")
            return 'however error ocured .. '

    def write_to_database(self, timestamp, value, velocity):
        # check if Archive directory present
        fs = FileSystemObject(self.output_path + 'Measured')
        csv_cnt = 0
        for csv_file in fs.object_read():
            if not DataBaseObject(fs.append_file(csv_file[:6] + '.sqlite')).object_exist(self.table_name):
                print 'must create table first'
            csv_cnt += 1
            for time_stamp, value in CsvFile(fs.append_file(csv_file)).content.iteritems():
                self.process_time_series()
        if csv_cnt < 1:
            print 'no csv files proccessed ...'

    def time_aggregated(self, time_value):
        """function to return rounded time
        second parameter aggregation time interval """
        # saving in <self.interval_shift> minute intervals
        print '***************** debug *****************'
        print 'time_value : ' + time_value
        if isinstance(time_value, str):
            time_value = datetime.datetime.strptime(time_value, self.date_format)
        minute = float(time_value.minute) + float(time_value.second) / 60
        modulo = float(minute % self.interval_shift)
        print 'minutes : ' + str(minute) + ' / modulo: ' + str(modulo)
        print '***************** debug *****************'
        # decide where to put value
        if modulo >= float(self.interval_shift / 2):
            min_new = minute - modulo + self.interval_shift
        else:
            min_new = minute - modulo
        if min_new > 58:
            hour_new = time_value.hour + 1
            min_new = 0
        else:
            hour_new = time_value.hour
        value_aggregated = datetime.datetime(time_value.year,
                                             time_value.month, time_value.day, hour_new, int(min_new), 0, 0)
        # print 'timestamp: ' + str(time_value) + ' > ' + str(value_aggregated)
        return value_aggregated

    def process_time_series(self, values):
        for vel, val in values.iteritems():
            print vel + val  # save to database

    
def min_between(d1, d2):
    """not used for now - just temp"""
    # d1 = datetime.strptime(d1, "%Y-%m-%d")
    # d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs(d2 - d1)
        
        
if __name__ == '__main__':

    from OS74 import FileSystemObject, CurrentPlatform, DateTimeObject
    from SO74DB import DataBaseObject
    from SO74TX import CsvFile
    from Template import SQL
    from log import Log
    
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help='device name reading data', type=str, default='')
    parser.add_argument('-l', help='location to write final data', type=str, default='')
    parser.add_argument('-m', help='mode (read serial/aggregate values)', type=str, default='')
    args = parser.parse_args()
    # create class for controlling device # logging
    dev = Device()
    logger = Log(args.l + 'logfile.log', 'device', 'DV72.py',  True)
    # device settings: port, baud rate and timeout
    dev.setup_device(args.d, "all sensors", 0)
    dev.setup_output_path(args.l)
    # log sql (debug) print sql
    
    if 'read' in args.m or 'ser' in args.m:
        text = 'Reading serial input from: {0} - at {1}'.format(str(dev.port),str(dev.br))
        logger.log_operation(text)
        ready = 'prepare to run serial read ...'
        while ready:
            ready = dev.read_serial()
    elif 'agg' in args.m:
        text = 'aggregating values in {0}, last run: {1}'.format(args.l, dev.last_run)
        logger.log_operation(text)
        dev.write_to_database('now', 0, 'm/s')
    else:
        print 'not possible'
