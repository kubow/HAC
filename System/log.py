import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check difference of two files")
    parser.add_argument('-l', help='Log file', type=str, default='')
    parser.add_argument('-t', help='Text to log', type=str, default='')
    args = parser.parse_args()
    
    logfile = open(args.l, 'w+')
    print args
    try:
        logfile.write(args.t)
    except:
        print 'something happened'
    finally:
        logfile.close()
    