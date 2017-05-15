"""Serial reading from a device"""
import os
import sys
import time
import datetime
# - basic 
import argparse
import sqlite3
import serial
# - adv
import Control
global times_run
global last_run

def set_up(db, device, sensor):
    conn = sqlite3.connect(sdb)
    c = conn.cursor()
    #port = port with device
    sql = dev.get_driver_loc
    sub_sql = dev.get_device_id.format(device)
    sql = sql.format(sub_sql, sensor)
    port = c.execute(sql).fetchone()[0]
    #br = baud rate
    sql = 'SELECT baud FROM setting;'
    br = c.execute(sql).fetchone()[0]
    conn.close()
    return port, br
    

if __name__ == '__main__':
    argd = 'device name reading data'
    argz = 'sensor name'
    argl = 'where to write csv data'
    run_dir = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help=argd, type=str, default='')
    parser.add_argument('-s', help=argz, type=str, default='')
    parser.add_argument('-l', help=argl, type=str, default='')
    args = parser.parse_args()
    
    # create class for controlling device
    dev = Control.Device()
    #get settings: port and baud rate
    port, br = set_up(run_dir + '/settings.db', args.d, args.s)
    # log sql (debug) print sql
    
    print 'Reading serial input from: {0} - at {1}'.format(str(port),str(br))
    ser = serial.Serial(port, br, timeout=0)
    #dictionary holding all/interval values
    data_vals = {}
    data_int = {} # clear the dictionary
    int_shift = 2 # shift of intervals in minutes
    last_run = Control.get_time(datetime.datetime.now(), int_shift)
    csv = ''
    
    while 1:
        try:
            recieved = ser.readline().replace('\r\n', ' ')
            if len(recieved) >= 1:
                vel_val = recieved.split(':')
                just_now = datetime.datetime.now()
                now = Control.get_time(just_now, int_shift)
                csv_fname = now.strftime(dev.date_file_format)+'.csv'
                # checking interval shifts
                if now > last_run:
                    Control.writeCSV(csv, data_vals, just_now, 'RPi')
                    data_vals = {} # clear the dictionaries 
                    data_int = {} 
                    last_run = now
                csv = args.l + csv_fname
                print recieved + str(just_now.strftime(dev.date_format))
                #building dictionary
                data_int[vel_val[0]] = vel_val[-1]
                data_vals[just_now.strftime(dev.date_format)] = data_int 
            time.sleep(1)
        except Exception as ex:
            print ex.args[0].replace('\n', ' ')
            print 'now '+ str(now)
            print 'last_run' + str(last_run)
            #if error found, do timeout
            #print data_vals
            #raw_input("Press enter to continue")
            #os.system("pause")
            #time.sleep(1)
