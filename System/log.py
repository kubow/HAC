import argparse
import datetime
import logging
from OS74 import FileSystemObject


class Log(object):
    def __init__(self, log_file, module, caller_file='log.py', advanced=True):
        self.date_format = '%d.%m.%Y %H:%M:%S'
        if not FileSystemObject(log_file).exist:
            print(log_file + ' does not exist! - create new one in actual path')
        self.log_file = log_file
        self.module = module
        self.line_text = ''
        self.caller_file = caller_file
        if advanced:
            self.advanced = advanced
            self.logger = self.init_logger()
        else:
            self.advanced = False

    def log_operation(self, text, level=20):
        now = datetime.datetime.now().strftime(self.date_format)
        if level > 20:
            print(text)
        if self.advanced:
            self.logger.log(level, text)
        else:
            self.line_text = str(now) + ' ; ' + self.module + ' ; ' + text + '\n'
            with open(self.log_file, 'a') as target_file:
                target_file.write(self.line_text)

    def init_logger(self):
        text_format = '%(asctime)s ; ' + self.module + ' ; %(message)s ; %(name)s ; %(levelname)s'
        logging.basicConfig()
        log_start = logging.getLogger('PY ; ' + self.module)
        log_start.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt=text_format, datefmt=self.date_format)
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        log_start.addHandler(fh)
        log_start.addHandler(ch)
        return log_start


def advanced_logger_test():
    logger.log_operation('this is a debug message', 10)
    logger.log_operation('this is an error message', 20)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="log to file")
    parser.add_argument('-l', help='Log file', type=str, default='')
    parser.add_argument('-m', help='module', type=str, default='none')
    parser.add_argument('-t', help='Text to log', type=str, default='')
    args = parser.parse_args()
    logger = Log(args.l, args.m, 'log.py', True)
    if not args.m or not args.t:
        advanced_logger_test()
    else:
        logger.log_operation(args.t)
