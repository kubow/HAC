import os
import argparse
import datetime
import logging


class Log(object):
    def __init__(self, log_file, module, log_level='warning', advanced=False):
        self.date_format = '%d.%m.%Y %H:%M:%S'
        if os.path.isfile(log_file):
            self.log_file = log_file
        else:
            print log_file + ' does not exist! - create new one?'
        self.module = module
        self.line_text = ''
        self.log_level = log_level
        if advanced:
            self.advanced = advanced
            self.logger = self.init_logger()
        else:
            self.advanced = False

    def log_operation(self, text, level=20):
        now = datetime.datetime.now().strftime(self.date_format)
        if self.advanced:
            line_text = text
            self.logger.log(level, text)
        else:
            line_text = str(now) + ' ; ' + self.module + ' ; ' + text + '\n'
            file_append(self.log_file, line_text)
        self.line_text = line_text

    def init_logger(self):
        text_format = '%(asctime)s ; ' + self.module + ' ; %(message)s ; %(name)s ; %(levelname)s'
        date_format = self.date_format 
        logging.basicConfig()
        log_start = logging.getLogger('PY ; ' + self.module)
        log_start.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt=text_format, datefmt=date_format)
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        log_start.addHandler(fh)
        log_start.addHandler(ch)
        return log_start


def file_append(filename, content):
    with open(filename, 'a') as target_file:
        target_file.write(content)
        

def advanced_logger_test():
    logger.log_operation('0 ; this is a debug message', 10)
    logger.log_operation('3 ; this is an error message', 20)


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
        logger.log_operation(args.t)
