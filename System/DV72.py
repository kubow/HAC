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
    def __init__(self, aggregate_time_step=2):
        self.date_format = '%Y.%m.%d %H:%M:%S'
        self.date_file_format = '%Y%m%d_%H%M'
        local_path = os.path.dirname(os.path.realpath(__file__))
        self.setup_db = local_path + '/Settings.sqlite'
        self.port = 0
        self.br = 0
        self.timeout = 0
        self.interval_shift = aggregate_time_step
        self.table_name = '_'
        self.table_fields = ''
        self.table_default_val = ''
        self.output_path = local_path
        self.csv_file = ''
        self.last_run = ''
        self.device_name = CurrentPlatform().hostname
        self.device_user = CurrentPlatform().environment
        self.device_platform = CurrentPlatform().main

    def setup_device(self, device, sensor=None, timeout=0):
        # override values: table_fields, table_default_val, port, br, timeout, last_run
        if FileSystemObject(self.setup_db).is_file:
            dbc = DataBaseObject(self.setup_db)
            # table name, that will hold values
            self.table_name = dbc.return_one(SQL.select.format('table_name', 'setting'))[0]
            # # build table structure
            col_list = ''  # columns - string to create table
            col_vals = {}  # columns - default values to insert query
            for row in dbc.return_many(SQL.select.format('*', 'structure')):
                col_list += row[1] + ' ' + row[2] + ','
                col_vals[row[1]] = row[4]
                # name of table being saved
            self.table_fields = col_list[:-1]
            self.table_default_val = col_vals
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
        # last run file
        last_run_file = FileSystemObject(self.output_path).append_file('last.run')
        self.last_run = FileSystemObject(last_run_file).object_mod_date(self.date_format)

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
            time.sleep(self.timeout)
            # received = ser.readline().replace('\r\n', ' ')  # not used - instead read a stack, average with one ts
            to_read = ser.inWaiting()
            received = ser.read(to_read)
            # parse data / now = rounded to x min intervals
            if len(received) >= 1:
                data_vals[just_now] = dict(item.split(":") for item in received.split("\r\n") if len(item) > 1)
                # for row in received.split('\r\n'):
                # checking interval shifts
                CsvContent(csv, write=True, content=data_vals)
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
        csv_cnt = 0
        ac_time = self.time_aggregated(datetime.datetime.now()).strftime(self.date_format)
        fs = FileSystemObject(self.output_path + 'Measured')
        fs.object_create_neccesary()
        for csv_file in fs.object_read(filter='csv'):
            db = DataBaseObject(fs.append_file(csv_file[:6] + '.sqlite'))
            csv = CsvContent(fs.append_file(csv_file), date_format=self.date_format)
            into = 'timestamp, '
            values = '"' + csv.time_stamp + '", '
            for time_series, average in csv.content.iteritems():
                into += time_series + ', '
                values += str(average) + ', '
            into = self.table_name + ' (' + into[:-2] + ')'
            if ac_time == csv.time_stamp:
                continue
            db.log_to_database(self.table_name, SQL.insert.format(into, values[:-2]), self.table_fields)
            csv.archive(fs.append_directory('Archive'))
            csv_cnt += 1
        if csv_cnt < 1:
            print 'no csv files proccessed ...'
        else:
            print '{0} files processed ...'.format(str(csv_cnt))

    def time_aggregated(self, time_value, debug=False):
        """function to return rounded time
        second parameter aggregation time interval """
        # saving in <self.interval_shift> minute intervals
        if isinstance(time_value, str):
            time_value = datetime.datetime.strptime(time_value, self.date_format)
        minute = float(time_value.minute) + float(time_value.second) / 60
        modulo = float(minute % self.interval_shift)
        if debug:
            print '***************** debug *****************'
            print 'time_value : ' + time_value
            print 'minutes : ' + str(minute) + ' / modulo: ' + str(modulo)
            print '***************** debug *****************'
        # decide where to put value
        hour_new = time_value.hour
        if modulo >= float(self.interval_shift / 2):
            min_new = minute - modulo + self.interval_shift
            if min_new > 60 - self.interval_shift:
                min_new = 0
                hour_new = time_value.hour + 1
                if hour_new > 23:
                    hour_new = 0
                    nd = datetime.date(time_value.year, time_value.month, time_value.day)
                    ndn = nd + timedelta(days=1)
                    time_value.year = ndn.year
                    time_value.month = ndn.month
                    time_value.day = ndn.day
        else:
            min_new = minute - modulo
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
    from SO74TX import CsvContent
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
    dev.setup_output_path(args.l)
    # device settings: port, baud rate and timeout
    dev.setup_device(args.d, "all sensors", 0)
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
