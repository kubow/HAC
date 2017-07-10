"""A directory browser GUI / Text mode

TkInter loading when GUI enabled
"""
import os
import argparse
import glob
import datetime

import platform
from sys import platform as _platform

import TX74

import ttk

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class Window(object):
    """Class for maintain widgets related to directory"""

    def populate_tree(tree, node):
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

    def autoscroll(sbar, first, last):
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

        print dir(w)
        w.populate_roots()
        tree.bind('<<TreeviewOpen>>', w.update_tree)
        tree.bind('<Double-Button-1>', w.change_dir)

        # Arrange the tree and its scrollbars in the toplevel
        tree.grid(column=0, row=0, sticky='nswe')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)


class Platform:
    def __init__(self):
        self.main = self.which_platform()

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

    def get_release(self):
        return platform.release()

    def print_system_description(self):
        # this is not working
        # return platform.version()
        # for debug purposes
        print 'system - {0} / release - {1}'.format(self.which_platform(), self.get_release())


def directory_lister(directory, output, list_files=False):
    template_loc = append_dir(one_dir_up(get_current_dir()), 'Structure') + 'HTML_DirectoryList.txt'
    print template_loc
    template = TX74.load_text_from(template_loc)
    template = template.replace('XXX', directory)

    head = '<table><tr class="Head"><td>List Generated on {0} / Total Folder Size - {1} / {2} Subfolders </td></tr>'
    table_head = '<table><tr class="Head">{0}<td>{1}</table>'
    table_row = '<tr class="{0}"><td>{1}</td><td>{2}</td></tr>'

    htm_content = ''
    total_size = 0
    folder_count = 0
    # Walk the directory tree
    for root, directories, files in os.walk(directory):
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
        htm_content = htm_content + '\n' + table_row.format('Fldr', ref, str(folder_size) + ' kb') + '\n' + tmp_content
        total_size = total_size + folder_size
        folder_count += 1

    content = head.format(datetime.datetime.now(), str(total_size) + ' kb', folder_count) + '\n' + htm_content
    # print content
    print template
    htm = open(output, 'w+')
    htm.write(template.replace('YYY', content))
    htm.close()


def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


def one_dir_up(directory):
    separator = get_separator_from(directory)
    # strip filename from path
    return separator.join(directory.split(separator)[0:-1])


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


def append_dir(path, string):
    separator = get_separator_from(path)
    return path + separator + string + separator


def get_separator_from(path):
    if '\\' in path:
        separator = '\\'
    elif '/' in path:
        separator = '/'
    else:
        separator = None
    return separator


def read_file(filename):
    with open(filename, 'r') as content_file:
        content = content_file.read()
    if 'htm' in filename.split()[-1]:
        content = TX74.htm_to_plain_txt(content)
    return content


def refresh_file(filename, content):
    # print 'refreshing filename: ' + filename + ' with text: ' + text
    if content:
        if not os.path.isfile(filename):
            print 'file {0} not exist, must create'.format(filename)
            touch_file(filename)
        file_write(filename, content)

    else:
        print 'no text to write, skipping file {0}'.format(filename)


def file_write(filename, content):
    with open(filename, 'w+') as target_file:
        target_file.write(content)


def get_file_size(file_path):
    # return file size in kilobytes
    return '{0:.2f}'.format(os.path.getsize(file_path) / 1024)


def touch_file(path):
    with open(path, 'a'):
        os.utime(path, None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="browse/list dirs")
    parser.add_argument('-b', help='browse dir', type=str, default='')
    parser.add_argument('-l', help='list dir', type=str, default='')
    parser.add_argument('-f', help='file output', type=str, default='')
    args = parser.parse_args()
    if args.b:
        root = tk.Tk()
        app = app_browser(root)
        app.mainloop()
    elif args.l:
        directory_lister(args.l, args.f, True)
