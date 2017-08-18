"""A directory browser GUI / Text mode

TkInter loading when GUI enabled
"""
import os
import argparse
import glob
import datetime

try:
    import ttk
    import Tkinter as tk
    import platform
    from sys import platform as _platform
except ImportError:
    print 'some bad import happened'
    import tkinter as tk


class Window(object):
    """Class for maintain widgets related to directory"""

    def populate_tree(self, tree, node):
        if tree.set(node, "type") != 'directory':
            return

        path = tree.set(node, "fullpath")
        tree.delete(*tree.get_children(node))

        parent = tree.parent(node)
        special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

        for p in special_dirs + os.listdir(path):
            ptype = None
            p = os.path.join(path, p).replace('\\', '/')
            if os.path.isdir(p):
                ptype = "directory"
            elif os.path.isfile(p):
                ptype = "file"

            fname = os.path.split(p)[1]
            id = tree.insert(node, "end", text=fname, values=[p, ptype])

            if ptype == 'directory':
                if fname not in ('.', '..'):
                    tree.insert(id, 0, text="dummy")
                    tree.item(id, text=fname)
            elif ptype == 'file':
                size = os.stat(p).st_size
                tree.set(id, "size", "%d bytes" % size)

    def populate_roots(self, tree):
        dir = os.path.abspath('.').replace('\\', '/')
        node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
        self.populate_tree(tree, node)

    def update_tree(self, event):
        tree = event.widget
        self.populate_tree(tree, tree.focus())

    def change_dir(self, event):
        tree = event.widget
        node = tree.focus()
        if tree.parent(node):
            path = os.path.abspath(tree.set(node, "fullpath"))
            if os.path.isdir(path):
                os.chdir(path)
                tree.delete(tree.get_children(''))
                self.populate_roots(tree)

    def autoscroll(self, sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)


class app_browser(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        w = Window()

        vsb = ttk.Scrollbar(orient="vertical")
        hsb = ttk.Scrollbar(orient="horizontal")

        tree = ttk.Treeview(columns=("fullpath", "type", "size"),
                            displaycolumns="size", yscrollcommand=lambda f, l: w.autoscroll(vsb, f, l),
                            xscrollcommand=lambda f, l: w.autoscroll(hsb, f, l))

        vsb['command'] = tree.yview
        hsb['command'] = tree.xview

        tree.heading("#0", text="Directory Structure", anchor='w')
        tree.heading("size", text="File Size", anchor='w')
        tree.column("size", stretch=0, width=100)
        
        w.populate_roots(tree)
        tree.bind('<<TreeviewOpen>>', w.update_tree)
        tree.bind('<Double-Button-1>', w.change_dir)

        # Arrange the tree and its scrollbars in the toplevel
        tree.grid(column=0, row=0, sticky='nswe')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)


class DateTimeObject:
    def __init__(self):
        self.date = datetime.datetime.now()

    def date_string_format(self, float_num, format):
        dt_object = datetime.datetime.utcfromtimestamp(float_num)
        return dt_object.strftime(format)


class FileSystemObject:
    def __init__(self, from_path, to_path=''):
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
            self.destination = self.one_dir_up()

    def get_separator_from_path(self):
        if '\\' in self.path:
            separator = '\\'
        elif '/' in self.path:
            separator = '/'
        else:
            separator = None
        return separator

    def one_dir_up(self):
        # strip filename / last dir from path
        return self.separator.join(self.path.split(self.separator)[0:-1])

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

    def directory_lister(self, list_files=False):
        template_loc = self.append_directory(self.one_dir_up(get_current_dir()), 'Structure') + 'HTML_DirectoryList.txt'
        # print template_loc
        template = SO74TX.load_text_from(template_loc)
        template = template.replace('XXX', self.path)

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

        content = head.format(datetime.datetime.now(), str(total_size) + ' kb', folder_count) + '\n' + htm_content
        # print content
        # print template
        self.file_write(self.destination, content)

    def object_read(self):
        if self.is_file:
            with open(self.path, 'r') as content_file:
                content = content_file.read()
            return content
        elif self.is_folder:
            objects = []
            for file in os.path.dirname(self.path):
                objects.append(file)
            return objects

    def object_write(self, content='', mode='w+'):
        if self.is_file:
            if mode != 'w+' or mode != 'a':
                if 'app' in mode:
                    mode = 'a'
                else:
                    mode = 'w+'
            with open(self.path, mode) as target_file:
                target_file.write(content)
        else:
            print 'not a file'

    def object_size(self):
        # return file size in kilobytes
        if self.is_file:
            return '{0:.2f}'.format(os.path.getsize(self.path) / 1024)
        elif self.is_folder:
            return 'for all files sum size'

    def object_mod_date(self, format='%Y. %m. %d %H:%M:%S'):
        return DateTimeObject().date_string_format(os.path.getmtime(self.path), format)

    def object_create_neccesary(self):
        # must check if path is meaningful name
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print 'directory ' + self.path + ' folder created ...'

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

    @staticmethod
    def get_release(self):
        return platform.release()

    def print_system_description(self):
        # this is not working
        # return platform.version()
        # for debug purposes
        print 'system - {0} / release - {1}'.format(self.which_platform(), self.get_release())

    def get_username_domain(self):
        return os.environ.get('USERNAME'), os.environ.get('USERDOMAIN')


def run_command_line(command):
    plf = CurrentPlatform()
    if 'win' == plf.main:
        installation_dir = 'C:\\Program Files(x86)\\cherrytree\\'
        command = installation_dir + command
    elif 'lnx' == plf.main or 'linux' == plf.main:
        command = command
    print 'command: ' + command


def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


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

        
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    position = "%dx%d+%d+%d" % (size + (x, y))
    log_text = 'window position : ' + position + ' - full screen {0}/{1}'.format(str(w), str(h))
    logger.log_operation(log_text)
    toplevel.geometry(position)


if __name__ == '__main__':

    import SO74TX
    from log import Log

    parser = argparse.ArgumentParser(description="browse/list dirs")
    parser.add_argument('-b', help='browse dir', type=str, default='')
    parser.add_argument('-l', help='list dir', type=str, default='')
    parser.add_argument('-f', help='file output', type=str, default='')
    args = parser.parse_args()
    logger = Log(args.f, 'directory')
    if args.b:
        root = tk.Tk()
        app = app_browser(root)
        center(root)
        app.mainloop()
    elif args.l:
        fso = FileSystemObject(args.l, args.f)
        fso.directory_lister(list_files=True)
