import os
import argparse
import datetime
import logging

def log_operation(log_file, module, text):
    log_file = open(log_file, 'a') #w+
    now = datetime.datetime.now()
    line_text = str(now) + ' - ' + module + ' - ' + text + '\n'
    try:
        log_file.write(line_text)
    except:
        print 'something happened'
    finally:
        log_file.close()
        
        
def advanced_logger(log_file, module):
    logging.basicConfig()
    logger = logging.getLogger('PY ; '+module)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s ; '+module+' ; %(name)s ; %(levelname)s ; %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
    
def advanced_logget_test():
    logger = advanced_logger('log_file.log')
    logger.log(10, '0 ; this is a debug message')
    logger.log(20, '3 ; this is an error message')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="log to file")
    parser.add_argument('-l', help='Log file', type=str, default='')
    parser.add_argument('-m', help='module', type=str, default='none')
    parser.add_argument('-t', help='Text to log', type=str, default='')
    args = parser.parse_args()
    #print args
    log_operation(args.l, args.m, args.t)
    
