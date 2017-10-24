"""A directory browser GUI / Text mode

TkInter loading when GUI enabled
"""
import os
import argparse
import datetime
import platform
import shutil
from sys import platform as _platform


class DateTimeObject:
    def __init__(self, date_set=datetime.datetime.now(), format='%d.%m.%Y %H:%M:%S'):
        self.date = date_set
        self.date_string = self.date_string_format(self.date, format)

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
            print 'using path relative to running script location ...' + from_path
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
        return self.path + self.separator + directory + self.separator

    def append_file(self, file_name):
        return self.path + self.separator + file_name

    def get_another_directory_file(self, another):
        if self.is_file:
            # strip filename from path
            root_dir = self.one_dir_up(self.path)
            return self.separator.join(root_dir.split(self.separator)[0:-1]) + self.separator + another
        elif self.is_folder:
            return self.separator.join(self.path.split(self.separator)[0:-1]) + self.separator + another
        else:
            print 'not file nor folder ...'
            return None

    def move_file_to(self, another_directory, filename=''):
        if not filename:
            filename = FileSystemObject(self.path).last_part()
        if self.is_file:
            shutil.move(self.path, FileSystemObject(another_directory).append_file(filename))
            print 'file ' + self.path + ' archived'
        else:
            print 'directory move not implemented'

    def directory_lister(self, list_files=False, final_file=''):
        template_fld = FileSystemObject().one_dir_up()
        template_file = FileSystemObject(template_fld).append_directory('Structure') + 'HTML_DirectoryList.txt'
        if not final_file:
            final_file = FileSystemObject(template_fld).append_directory('Multimedia') + 'DirectoryList.html'
        print template_file + ' - will be writing to: ' + final_file
        template = SO74TX.load_text_from(template_file).replace('XXX', self.path)

        head = '<table><tr class="Head"><td>List Generated on {0} / Total Folder Size - {1} / {2} Subfolders </td></tr>'
        table_head = '<table><tr class="Head">{0}<td>{1}</table>'
        table_row = '<tr class="{0}"><td>{1}</td><td>{2}</td></tr>'

        htm_content = ''
        total_size = 0
        folder_count = 0
        # Walk the directory tree
        for root, directories, files in os.walk(self.path):
            print root
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
        # print content
        # print template
        FileSystemObject(final_file).object_write(content)

    def object_read(self, filter=''):
        if self.is_file:
            with open(self.path, 'r') as content_file:
                content = content_file.read()
            return content
        elif self.is_folder:
            obj_lib = {}
            for file in os.listdir(self.path):
                if filter in file or not filter:
                    obj_lib[file] = self.path + file
            return obj_lib

    def object_write(self, content='', mode='w+'):
        if self.is_file:
            if mode != 'w+' or mode != 'a':
                if 'app' in mode:
                    mode = 'a'
                else:
                    mode = 'w+'
            with open(self.destination, mode) as target_file:
                target_file.write(content)
        else:
            print 'is not a file, cannot write: ' + self.destination

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
                print 'directory ' + self.path + ' folder created ...'
            else:
                self.file_touch()

    def file_touch(self):
        with open(self.path, 'w+'):
            os.utime(self.path, None)

    def file_refresh(self, content):
        # print 'refreshing filename: ' + filename + ' with text: ' + text
        if content:
            if not self.is_file(self.path):
                print 'file {0} not exist, must create'.format(self.path)
                self.file_touch(self.path)
            self.object_write(content, 'w+')
        else:
            print 'no text to write, skipping file {0}'.format(self.path)


class CurrentPlatform:
    def __init__(self):
        self.main = self.which_platform()
        self.environment = self.get_username_domain()
        self.hostname = platform.node()

    @staticmethod
    def which_platform():
        if _platform == 'linux' or _platform == 'linux2':
            return 'lnx'
        elif _platform == 'darwin':
            return 'mac'
        elif _platform == 'win32' or _platform == 'win64':
            return 'win'
            print 'must create _winreg import and read ...'
        else:
            return _platform

    def print_system_description(self):
        # this is not working
        # return platform.version()
        # for debug purposes
        print 'system - {0} / release - {1}'.format(self.which_platform(), self.get_release())

    @staticmethod
    def get_release():
        return platform.release()

    @staticmethod
    def get_username_domain():
        return os.environ.get('USERNAME'), os.environ.get('USERDOMAIN')


def run_command_line(command):
    plf = CurrentPlatform()
    if 'win' == plf.main:
        installation_dir = 'C:\\Program Files(x86)\\cherrytree\\'
        command = installation_dir + command
    elif 'lnx' == plf.main or 'linux' == plf.main:
        command = command
    print 'command: ' + command


def compare_directories(dir1, dir2):
    if not os.path.isdir(dir1) or not os.path.isdir(dir2):
        print 'one of submitted directories do not exist, quitting...'
    else:
        found = True
        for root, directories, files in os.walk(dir1):
            corr = root.replace(dir1, dir2)
            # print root + ' :x: ' + corr
            if not os.path.isdir(corr):
                print 'not found ' + dir2 + '/' + root
                continue
            for filename in files:
                # print filename
                corr_file = filename.replace(dir1, dir2)
                if not os.path.exists(corr_file):
                    # print root + ' :x: ' + corr
                    # print 'not found ' + filename
                    found = False


if __name__ == '__main__':

    import SO74TX
    from log import Log
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
        print 'please specify at least input file ...'
