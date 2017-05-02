import os
import argparse
import datetime

def file_write(logfile, module, text):
    logfile = open(logfile, 'a') #w+
    now = datetime.datetime.now()
    line_text = str(now) + ' - ' + module + ' - ' + text + '\n'
    try:
        logfile.write(line_text)
    except:
        print 'something happened'
    finally:
        logfile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="log to file")
    parser.add_argument('-l', help='Log file', type=str, default='')
    parser.add_argument('-m', help='module', type=str, default='none')
    parser.add_argument('-t', help='Text to log', type=str, default='')
    args = parser.parse_args()
    #print args
    file_write(args.l, args.m, args.t)
    
