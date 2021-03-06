#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Developped by Kube Kubow 2017
File contains class for controlling Device through sqlite settings
Class Device with these functions:
function time_aggregated to round (aggregate) timestamp
function time_aggregated_from_file to build date and time from file name
function to read CSV/JSON file content to a dictionary
function to write CSV/JSON file from downloaded data
and a logger module - currently not implemented
"""
import time
import datetime
from pprint import pprint
import argparse

try:
    import serial
    serial_read = True
except ImportError:
    print('!!! cannot read serial input, missing python library..')
    serial_read = False

from OS74 import FileSystemObject, CurrentPlatformControl
from DB74 import DataBaseObject
from TX74 import CsvContent, JsonContent


class ControlDevice(object):
    def __init__(self, aggregate_time_step=2):
        this_file = FileSystemObject(__file__)
        current_platform = CurrentPlatformControl()
        self.date_format = '%Y.%m.%d %H:%M:%S'
        self.date_file_format = '%Y%m%d_%H%M'
        self.setup_db = this_file.get_another_directory_file('Settings.sqlite')
        self.port = 0
        self.br = 0
        self.timeout = 0
        self.interval_shift = aggregate_time_step
        self.table_name = '_'
        self.table_fields = ''
        self.table_default_val = ''
        self.output_path = this_file.dir_up(2)
        self.csv_file = ''
        self.last_run = ''
        # pprint(vars(current_platform))
        self.device_sender = ''
        self.device_name = current_platform.hostname
        self.device_user = current_platform.environment
        self.device_platform = current_platform.main
        b = FileSystemObject(self.output_path).get_another_directory_file('list_senzor.sh')
        self.usb_list2 = current_platform.check_output(b).decode().split('\n')
        self.usb_list = current_platform.list_attached_peripherals()

    def setup_device(self, device, timeout=0):
        # override values: table_fields, table_default_val, port, br, timeout, last_run
        self.device_sender = device
        if FileSystemObject(self.setup_db).is_file:
            db = DataBaseObject(self.setup_db)
            # table name, that will hold values
            self.table_name = db.return_one(SQL.select.format('table_name', 'setting'))[0]
            # # build table structure
            col_list = ''  # columns - string to create table
            col_vals = {}  # columns - default values to insert query
            for row in db.return_many(SQL.select.format('*', 'structure')):
                col_list += row[1] + ' ' + row[2] + ','
                col_vals[row[1]] = row[4]
                # name of table being saved
            self.table_fields = col_list[:-1]
            self.table_default_val = col_vals
            # match device name, platform
            for device_check in db.return_many(SQL.get_device_name_list):
                if str(device_check[0]).lower() in self.device_name.lower():
                    self.port = db.return_one(SQL.get_driver_loc.format(device_check[0]))[0]
                    self.br = db.return_one(SQL.get_driver_br.format(device_check[0]))[0]
                    str_device_id = 'identified device %s' % self.device_name
                    str_device_adress = 'should read from %s' % self.port
                    logger.log_operation(str_device_id+' / '+str_device_adress)
                    break
            if not self.port:
                print(SQL.get_driver_dummy_loc.format(self.device_platform))
                self.port = db.return_one(SQL.get_driver_dummy_loc.format(self.device_platform))[0]
            if not self.br:
                print(SQL.get_driver_dummy_br.format(self.device_platform))
                self.br = db.return_one(SQL.get_driver_dummy_br.format(self.device_platform))[0]
        else:
            # no available config - using default values
            self.port = 'COM4'
            self.br = 9600
            self.table_name = 'measured'
            print_text = 'not able to load setup database, using default {0} / {1}'
            logger.log_operation(print_text.format(self.port, self.br))
        # validate port & br (that the device is really connected)
        if self.validate_usb_driver():
            print('corresponding driver found, currently set: ' + self.port)
        else:
            print('no corresponding driver found, currently set: ' + self.port)
        # timeout waiting time
        self.timeout = timeout
        # last run file
        last_run_file = FileSystemObject(self.output_path).append_objects(file='last.run')
        self.last_run = FileSystemObject(last_run_file).object_mod_date(self.date_format)

    def setup_output_path(self, path):
        self.output_path = path

    def validate_usb_driver(self):
        for device in self.usb_list2:
            if len(device) < 1:
                continue
            if device.split(' - ')[0] in self.port:
                print(device.split(' - ')[0], self.port)
                return True
            elif self.device_sender in str(device.split(' - ')[-1]).lower():
                print('found ' + self.device_sender + ' string - changing to it')
                self.port = device.split(' - ')[0]
                return True
        return False
        
    def read_serial(self):
        """reading serial line and mirror it to CSV file"""
        if not serial_read:
            return None
        ac_time = datetime.datetime.now()
        data_vals = {}  # dictionary holding all/interval values
        just_now = ac_time.strftime(self.date_format)
        now = self.time_aggregated(just_now)
        just_now_file = now.strftime(self.date_file_format)
        # last_run = time_aggregated(just_now, self.interval_shift)
        csv = self.output_path + 'Measured/' + just_now_file + '.csv'
        try:
            ser = serial.Serial(self.port, self.br, timeout=self.timeout)
            ser.flushInput()
            ser.flushOutput()
            time.sleep(self.timeout + 2)
            # received = ser.readline().replace('\r\n', ' ')  # not used - instead read a stack, average with one ts
            to_read = ser.inWaiting()
            received = ser.read(to_read).decode()
            # parse data / now = rounded to x min intervals
            if len(received) >= 1:
                data_vals[just_now] = dict(item.split(":") for item in received.split("\r\n") if len(item) > 1)
                # for row in received.split('\r\n'):
                # checking interval shifts
                CsvContent(csv, write=True, content=data_vals)
                print(data_vals)
                return data_vals
            else:
                print('no text to receive ...')
                return 'some values might come ...'
        except serial.SerialException as se:
            logger.log_operation(se.args[-1])
            logger.log_operation(','.join(d['tag'] for d in dev.usb_list))
            pprint(vars(self))
            # print('serial communication not accesible!')
            return None
        except Exception as ex:
            print(ex.args[0].replace('\n', ' '))
            print('timeframe now : '+ str(now) + ' / ' + 'last_run' + str(self.last_run))
            # pprint(vars(self))
            # if error found, do timeout
            # raw_input("Press enter to continue")
            return 'however error ocured .. '

    def write_to_database(self, timestamp='now', value=0, velocity='m/s'):
        # check if Archive directory present
        csv_cnt = 0
        ac_time = self.time_aggregated(datetime.datetime.now()).strftime(self.date_format)
        fs = FileSystemObject(self.output_path + 'Measured')
        fs.object_create_neccesary()
        for csv_file in fs.object_read(filter='csv').items():
            print('processing file: ' + str(csv_file))
            db = DataBaseObject(fs.append_objects(file=csv_file[0][:6] + '.sqlite'))
            csv = CsvContent(fs.append_objects(file=csv_file[0]), date_format=self.date_format)
            print(csv)
            into = 'timestamp, '
            values = '"' + csv.time_stamp + '", '
            print(dir(csv))
            print(type(csv))
            for time_series, average in csv.content().items():
                into += time_series + ', '
                values += str(average) + ', '
            into = self.table_name + ' (' + into[:-2] + ')'
            if ac_time == csv.time_stamp:
                continue  # avoid just being written files
            db.log_to_database(self.table_name, SQL.insert.format(into, values[:-2]), self.table_fields)
            csv.archive(fs.append_objects(dir='Archive'))
            csv_cnt += 1
        if csv_cnt < 1:
            print('no csv files proccessed ...')
        else:
            print('{0} files processed ...'.format(str(csv_cnt)))

    def time_aggregated(self, t_val=False, debug=False):
        """use to return rounded time
        second parameter aggregation time interval """
        # saving in <self.interval_shift> minute intervals
        if isinstance(t_val, str):
            t_val = datetime.datetime.strptime(t_val, self.date_format)
        else:
            t_val = datetime.datetime.now()
            print('time value not submited, using now: ', t_val)
        minute = float(t_val.minute) + float(t_val.second) / 60
        modulo = float(minute % self.interval_shift)
        if debug:
            print('***************** debug *****************')
            print('time value : ' + t_val)
            print('in minutes : ' + str(minute) + ' / modulo: ' + str(modulo))
            print('***************** debug *****************')
        # decide where to put value
        hour_new = t_val.hour
        if modulo >= float(self.interval_shift / 2):
            min_new = minute - modulo + self.interval_shift
            if min_new > 60 - self.interval_shift:
                min_new = 0
                hour_new = t_val.hour + 1
                if hour_new > 23:
                    hour_new = 0
                    nd = datetime.date(t_val.year, t_val.month, t_val.day)
                    ndn = nd + datetime.timedelta(days=1)
                    t_val.year = ndn.year
                    t_val.month = ndn.month
                    t_val.day = ndn.day
        else:
            min_new = minute - modulo
        value_aggregated = datetime.datetime(t_val.year,
                                             t_val.month, t_val.day, hour_new, int(min_new), 0, 0)
        # print('timestamp: ' + str(t_val) + ' > ' + str(value_aggregated))
        return value_aggregated

    def process_time_series(self, values):
        for vel, val in values.items():
            print(vel + val)  # save to database

    
def min_between(d1, d2):
    """not used for now - just temp"""
    # d1 = datetime.strptime(d1, "%Y-%m-%d")
    # d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs(d2 - d1)
        
        
if __name__ == '__main__':
    from Template import SQL
    from log import Log
    
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-l', help='location to write final data', type=str, default='')
    parser.add_argument('-m', help='mode (read serial/aggregate values)', type=str, default='')
    args = parser.parse_args()
    # create class for controlling device # logging
    dev = ControlDevice()
    logger = Log(args.l + 'logfile.log', 'device', 'DV72.py',  True)
    dev.setup_output_path(args.l)
    # device settings: port, baud rate and timeout
    dev.setup_device('arduino', timeout=0)
    # log sql (debug) print(sql)
    
    if 'read' in args.m or 'ser' in args.m:
        text = 'Reading serial input from: {0} - at {1}'.format(str(dev.port),str(dev.br))
        logger.log_operation(text)
        ready = 'prepare to run serial read ... '
        while ready:
            ready = dev.read_serial()
    elif 'agg' in args.m:
        text = 'aggregating values in {0}, last run: {1}'.format(args.l, dev.last_run)
        logger.log_operation(text)
        dev.write_to_database()
        JsonContent(args.l + 'Measured', write=True)
    else:
        logger.log_operation(','.join(d['tag'] for d in dev.usb_list))
