import argparse
import datetime
import logging


class Log(object):
    def __init__(self, log_file, module, log_level='warning', advanced=False):
        self.log_file = log_file
        self.module = module
        self.log_level = log_level
        if advanced:
            self.logger = self.log_advanced()
        else:
            self.log_simple()

    def log_simple(self, text):
        now = datetime.datetime.now()
        line_text = str(now) + ' - ' + self.module + ' - ' + text + '\n'
        print line_text
        try:
            log_file = open(self.log_file, 'a')  # w+
            log_file.write(line_text)
        except:
            print 'something happened'
        finally:
            log_file.close()

    def log_advanced(self):
        text_format = '%(asctime)s ; ' + self.module + ' ; %(name)s ; %(levelname)s ; %(message)s'
        date_format = '%d.%m.%Y %H:%M:%S'
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


def advanced_logget_test():
    logger = Log().log_advanced('test_module')
    logger.log(10, '0 ; this is a debug message')
    logger.log(20, '3 ; this is an error message')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="log to file")
    parser.add_argument('-l', help='Log file', type=str, default='')
    parser.add_argument('-m', help='module', type=str, default='none')
    parser.add_argument('-t', help='Text to log', type=str, default='')
    args = parser.parse_args()
    logger = Log(args.l, args.m)
    logger.log_simple(args.t)
