"""A Platform controlller

Files & Folder classes
"""
import os
import argparse
import datetime
import platform
import shutil
import re
from subprocess import call, check_call, check_output, STDOUT
from sys import platform as _platform

try:
    import win32com.client as w32
except ImportError:
    windows = False

from Template import SQL
from SO74DB import DataBaseObject


class DateTimeObject:
    def __init__(self, date_set=datetime.datetime.now(), date_format='%d.%m.%Y %H:%M:%S'):
        self.date = date_set
        self.date_string = self.date_string_format(self.date, date_format)

    def date_string_format(self, float_num, format_str):
        if isinstance(float_num, float):
            dt_object = datetime.datetime.utcfromtimestamp(float_num)
        else:
            dt_object = float_num
        return dt_object.strftime(format_str)


class FileSystemObject:
    def __init__(self, from_path='', to_path=''):
        if not from_path:
            from_path = os.path.dirname(os.path.realpath(__file__))
            print('using path relative to running script location ...' + from_path)
        self.path = from_path
        self.separator = self.get_separator_from_path()
        if os.path.isfile(from_path):
            self.exist = True
            self.is_file = True
            self.is_folder = False
        elif os.path.isdir(from_path):
            self.exist = True
            self.is_file = False
            self.is_folder = True
        else:
            self.exist = False
            if '.' in from_path:
                self.is_file = True
                self.is_folder = False
            else:
                self.is_file = False
                self.is_folder = True
        if to_path:
            self.destination = to_path
        else:
            self.destination = self.path

    def get_separator_from_path(self):
        if '\\' in self.path:
            separator = '\\'
        elif '/' in self.path:
            separator = '/'
        else:
            separator = None
        return separator

    def one_dir_up(self):
        # avoid separators in the end of path string
        if self.separator == self.path[-1:]:
            self.path = self.path[:-1]
        # strip filename / last dir from path
        return self.separator.join(self.path.split(self.separator)[:-1]) + self.separator

    def last_part(self):
        return self.path.split(self.separator)[-1]

    def append_directory(self, directory):
        return self.path + self.separator + directory

    def append_file(self, file_name):
        return self.path + self.separator + file_name

    def get_another_directory_file(self, another):
        if self.is_file:
            # strip filename from path
            root_dir = self.one_dir_up()
            return self.separator.join(root_dir.split(self.separator)[0:-1]) + self.separator + another
        elif self.is_folder:
            return self.separator.join(self.path.split(self.separator)[0:-1]) + self.separator + another
        else:
            print('not file nor folder ...')
            return None

    def move_file_to(self, another_directory, filename=''):
        if not filename:
            filename = self.last_part()
        if self.is_file:
            shutil.move(self.path, FileSystemObject(another_directory).append_file(filename))
            print('file ' + self.path + ' archived')
        else:
            print('directory move not implemented')
            
    def copy_file_to(self, another_directory, filename=''):
        if not filename:
            shutil.copy(self.path, another_directory)
        else:
            if self.is_file:
                shutil.copy(self.path, FileSystemObject(another_directory).append_file(filename))
                print('file ' + self.path + ' archived')
            else:
                print('directory copy not implemented')

    def directory_lister(self, list_files=False, final_file=''):
        template_fld = FileSystemObject().one_dir_up()
        template_file = FileSystemObject(template_fld).append_directory('Structure') + 'HTML_DirectoryList.txt'
        if not final_file:
            final_file = FileSystemObject(template_fld).append_directory('Multimedia') + 'DirectoryList.html'
        print(template_file + ' - will be writing to: ' + final_file)
        template = TextContent(file_name=template_file).replace('XXX', self.path)

        head = '<table><tr class="Head"><td>List Generated on {0} / Total Folder Size - {1} / {2} Subfolders </td></tr>'
        table_head = '<table><tr class="Head">{0}<td>{1}</table>'
        table_row = '<tr class="{0}"><td>{1}</td><td>{2}</td></tr>'

        htm_content = ''
        total_size = 0
        folder_count = 0
        # Walk the directory tree
        for root, directories, files in os.walk(self.path):
            print(root)
            folder_size = 0
            file_count = 0
            tmp_content = ''
            for filename in files:
                folder_size += (os.path.getsize(root + '/' + filename) / 1024)
                if list_files:
                    file_size = str('{0:.2f}'.format(os.path.getsize(root + '/' + filename) / 1024)) + ' kb'
                    tmp_content = tmp_content + table_row.format('File', filename, file_size) + '\n'
                file_count += 1
            ref = '<a href="file:///' + root + '">' + root + '</a> (' + str(file_count) + ' files in folder)'
            htm_content = htm_content + '\n' + table_row.format('Fldr', ref,
                                                                str(folder_size) + ' kb') + '\n' + tmp_content
            total_size = total_size + folder_size
            folder_count += 1

        content = head.format(DateTimeObject().date_string, str(total_size) + ' kb', folder_count) + '\n' + htm_content
        # print(content)
        # print(template)
        FileSystemObject(final_file).object_write(content)

    def object_read_split(self):
        folder_list = []
        file_list = []
        object_dict = self.object_read()
        for object in object_dict:
            if FileSystemObject(object_dict[object]).is_folder:
                folder_list.append(object)
            else:
                file_list.append(object)
        return folder_list, file_list
    
    def object_read(self, filter=''):
        if self.is_file:
            with open(self.path, 'r') as content_file:
                content = content_file.read()
            return content
        elif self.is_folder:
            obj_lib = {}
            for file_name in os.listdir(self.path):
                if filter in file_name or not filter:
                    obj_lib[file_name] = self.path + self.separator + file_name
            return obj_lib

    def object_write(self, content='', mode='w+'):
        if self.is_file:
            if mode != 'w+' or mode != 'a':
                if 'app' in mode:
                    mode = 'a'
                else:
                    mode = 'w+'
            with open(self.destination, mode,  encoding="utf-8") as target_file:
                target_file.write(content)
        else:
            print('is not a file, cannot write: ' + self.destination)

    def object_size(self):
        # return file size in kilobytes
        if self.is_file:
            return '{0:.2f}'.format(os.path.getsize(self.path) / 1024)
        elif self.is_folder:
            return 'for all files sum size'

    def object_mod_date(self, format='%Y. %m. %d %H:%M:%S'):
        if self.exist:
            return DateTimeObject().date_string_format(os.path.getmtime(self.path), format)
        else:
            self.object_create_neccesary()
            return DateTimeObject().date_string

    def object_create_neccesary(self):
        # must check if path is meaningful name
        if not self.exist:
            if self.is_folder:
                os.makedirs(self.path)
                print('directory ' + self.path + ' folder created ...')
            else:
                self.file_touch()

    def file_touch(self):
        with open(self.path, 'w+'):
            os.utime(self.path, None)

    def file_refresh(self, content):
        # print('refreshing filename: ' + filename + ' with text: ' + text)
        if content:
            if not self.is_file(self.path):
                print('file {0} not exist, must create'.format(self.path))
                self.file_touch(self.path)
            self.object_write(content, 'w+')
        else:
            print('no text to write, skipping file {0}'.format(self.path))


class CurrentPlatform:
    def __init__(self):
        if _platform == 'linux' or _platform == 'linux2':
            self.main = 'lnx'
        elif _platform == 'darwin':
            self.main = 'mac'
        elif _platform == 'win32' or _platform == 'win64':
            print('must create _winreg import and read ...')
            self.main = 'win'
        else:
            self.main = _platform
        if self.main == "win":
            self.environment = os.environ.get('USERNAME'), os.environ.get('USERDOMAIN')
        else:
            self.environment = os.environ.get('USERNAME'), os.environ.get('HOSTNAME')
        self.hostname = platform.node()
        if self.main == "lnx":
            self.homepath = os.environ.get('HOME')
        else:
            self.homepath = os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        self.release = platform.release()

    def print_system_description(self):
        # this is not working
        # return platform.version()
        # for debug purposes
        print('system - {0} / release - {1}'.format(self.main, self.release))


    def get_home_dir_path(self):
        if self.main == "lnx":
            return os.environ.get('HOME') 
        else:
            return os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')

        
class CurrentPlatformControl(CurrentPlatform):
    def __init__(self, application=''):
        CurrentPlatform.__init__(self)
        if application:
            self.app_name = application
            d = os.path.dirname(os.path.realpath(__file__)) + '/Settings.sqlite'
            sql = SQL.get_app_command.format(application, self.main)
            #print(sql)
            self.app_run_path = DataBaseObject(d).return_one(sql)[0]
        else:
            self.app_name = 'not_defined'
            self.app_run_path = ''
        if not self.app_run_path:
            self.app_run_path = application
        
    def run_with_argument(self, arg_1='', arg_2=''):
        print(self.app_run_path + ' %s' % arg_1)
        call([self.app_run_path, arg_1])
        # if self.main == 'lnx':
            # call([self.app_run_path, arg_1])
        # elif self.main == 'win':
            # call([self.app_run_path, arg_1])

    def check_output(self, arg='', timeout=2):
        try:
            command_input = self.app_run_path + ' ' + arg
            return check_output(command_input, stderr=STDOUT, timeout=timeout, shell=True)
        except:
            return None

    def list_attached_peripherals(self):
        if self.main == 'win':
            wmi = w32.GetObject("winmgmts:")
            for usb in wmi.InstancesOf("Win32_USBHub"):
                return usb.DeviceID
        else:
            device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
            df = check_output("lsusb")
            devices = []
            for i in df.split(b'\n'):
                if i and device_re.match(str(i)):
                    dinfo = device_re.match(str(i)).groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)
            return devices


def compare_directories(dir1, dir2):
    if not os.path.isdir(dir1) or not os.path.isdir(dir2):
        print('one of submitted directories do not exist, quitting...')
    else:
        found = True
        for root, directories, files in os.walk(dir1):
            corr = root.replace(dir1, dir2)
            # print(root + ' :x: ' + corr)
            if not os.path.isdir(corr):
                print('not found ' + dir2 + '/' + root)
                continue
            for filename in files:
                # print(filename)
                corr_file = filename.replace(dir1, dir2)
                if not os.path.exists(corr_file):
                    # print(root + ' :x: ' + corr)
                    # print('not found ' + filename)
                    found = False


if __name__ == '__main__':

    from log import Log
    from SO74TX import TextContent
    from UI74 import main_app_view

    parser = argparse.ArgumentParser(description="browse/list dirs")
    parser.add_argument('-i', help='input dir', type=str, default='')
    parser.add_argument('-m', help='extra graphic mode', type=str, default='')
    parser.add_argument('-f', help='file output', type=str, default='')
    parser.add_argument('-l', help='log file', type=str, default='')
    args = parser.parse_args()
    logger = Log(args.l, 'directory', __file__, True)
    if args.m:
        logger.log_operation('opening new window - browse: ' + args.i)
        main_app_view()
    elif args.i:
        fso = FileSystemObject(args.i, args.f)
        fso.directory_lister(list_files=True)
    else:
        logger.log_operation('please specify at least input file ...') 
