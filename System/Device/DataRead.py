import os
import argparse
import sqlite3
import serial
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-d', help='device name', type=str, default='')
    parser.add_argument('-s', help='sensor name', type=str, default='')
    args = parser.parse_args()
    
    sdb = os.path.dirname(os.path.realpath(__file__)) + '/settings.db'
    conn = sqlite3.connect(sdb)
    c = conn.cursor()
    #port = port with device
    sql = 'SELECT driverloc FROM driver WHERE device = {0} AND drivertype = "{1}";'
    sub_sql = '(SELECT ID from device WHERE devicename ="{0}")'.format(args.d)
    sql = sql.format(sub_sql, args.s)
    print sql
    port = c.execute(sql).fetchone()[0]
    #br = baud rate
    sql = 'SELECT baud FROM setting;'
    br = c.execute(sql).fetchone()[0]
    
    print 'Reading serial input from: ' + str(port) + ' - at ' + str(br)
    ser = serial.Serial(port, br, timeout=0)
     
    while 1:
     try:
      print ser.readline()
      time.sleep(1)
     except ser.SerialTimeoutException:
      print('Data could not be read')
      time.sleep(1)