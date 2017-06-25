#import argparse
#import win32com.client
import os

def monitor_command_output(cmd):
    os.system(cmd)
    f = open('conn.tmp', 'r')
    f.readline();f.readline();f.readline()
    conn = []
    host = f.readline()
    while host[0] == '\\':
        conn.append(host[2:host.find(' ')])
    host = f.readline()
    f.close()
    print conn
    

def adodb_conn():
    conn = win32com.client.Dispatch(r'ADODB.Connection')
    DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/MyDB.mdb;'
    conn.Open(DSN)

    conn.Close(DSN)

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description="Monitor network")
    #parser.add_argument('-d', help='directory', type=str, default='')
    #args = parser.parse_args()

    monitor_command_output('net view > conn.tmp')
