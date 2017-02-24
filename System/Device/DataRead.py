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

if __name__ == '__main__':
    run_dir = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help='device name', type=str, default='')
    parser.add_argument('-s', help='sensor name', type=str, default='')
    parser.add_argument('-l', help='location to write', type=str, default='')
    args = parser.parse_args()
    
    #get settings
    sdb = run_dir + '/settings.db'
    conn = sqlite3.connect(sdb)
    c = conn.cursor()
    #load querries
    dev = Control.Device()
    #port = port with device
    sql = dev.get_driver_loc
    sub_sql = dev.get_device_id.format(args.d)
    sql = sql.format(sub_sql, args.s)
    port = c.execute(sql).fetchone()[0]
    #br = baud rate
    sql = 'SELECT baud FROM setting;'
    br = c.execute(sql).fetchone()[0]
    # log sql (debug) print sql
    
    print 'Reading serial input from: ' + str(port) + ' - at ' + str(br)
    ser = serial.Serial(port, br, timeout=0)
    #dictionary holding all values
    data_vals = {}
    
    while 1:
    #try:
        now = Control.get_time(datetime.datetime.now(), 2)
        #if last_run <> now
        
        #else 
        print str(now) + ' ' + ser.readline()
        time.sleep(1)
        
    #except ser.SerialTimeoutException:
        #print('Data could not be read')
        #time.sleep(1)