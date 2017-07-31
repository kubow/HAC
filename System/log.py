import os
import argparse
import datetime
import logging


class Log(object):
    def __init__(self, log_file, module, log_level='warning', advanced=False):
        if os.path.isfile(log_file):
            self.log_file = log_file
        else:
            print log_file + ' does not exist!'
        self.module = module
        self.log_level = log_level
        self.advanced = advanced
        self.date_format = '%d.%m.%Y %H:%M:%S'
        if advanced:
            self.logger = self.log_advanced()

    def log_simple(self, text):
        now = datetime.datetime.now().strftime(self.date_format)
        line_text = str(now) + ' - ' + self.module + ' - ' + text + '\n'
        print line_text
        try:
            log_file = open(self.log_file, 'a')  # w+
            log_file.write(line_text)
            lof_file.close()
        except:
            print 'something happened'
        finally:
            pass

    def log_advanced(self):
        text_format = '%(asctime)s ; ' + self.module + ' ; %(name)s ; %(levelname)s ; %(message)s'
        date_format = self.date_format 
        logging.basicConfig()
        logger = logging.getLogger('PY ; ' + self.module)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt=text_format, datefmt=date_format)
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger


def advanced_logger_test():
    logger.logger.log(10, '0 ; this is a debug message')
    logger.logger.log(20, '3 ; this is an error message')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="log to file")
    parser.add_argument('-l', help='Log file', type=str, default='')
    parser.add_argument('-m', help='module', type=str, default='none')
    parser.add_argument('-t', help='Text to log', type=str, default='')
    args = parser.parse_args()
    logger = Log(args.l, args.m, 'debug', True)
    if logger.advanced:
        advanced_logger_test()
    else:
        logger.log_simple(args.t)
