# -*- coding: utf-8 -*-
import os
import argparse
# Use Tkinter for python 2, tkinter for python 3
from Tkinter import *
from PIL import Image, ImageTk
# local project imports
import H808E
import TextProcess


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master, background="yellow")
        self.directory = directory

        # upper menu
        self.bar_main = Label(self.master, text=' Main Menu ...')
        self.bar_node = Label(self.master, text='Location : {0}'.format(directory))
        self.bar_main.grid(row=0, column=0, sticky=W)
        self.bar_node.grid(row=0, column=1, sticky=E)

        # buttons upper right
        self.one_up = Button(self.master, text='one level up', command=self.on_up_select)
        self.one_up.grid(row=0, column=2, sticky=W)

        # related data table down right
        self.rel_data = SimpleTable(self, 5, 3)
        self.rel_data.grid(row=2, column=2, sticky=N + S + E)
        self.rel_data.set(0, 0, 'gggg')

        # multimedia view window
        self.canvas = Canvas(self.master, bd=0, highlightthickness=0, width=600, height=600, background="white")
        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
        self.canvas.create_text(20, 30, anchor=W, font="Purisa", text="Most relationships seem so transitory")
        self.canvas.grid(row=1, column=0, rowspan=2, columnspan=2, sticky=N + S + W, pady=(10, 10), padx=(10, 10))

        # multimedia file list
        self.file_list = Listbox(self.master, height=7)
        self.file_list.bind('<<ListboxSelect>>', self.on_file_select)
        self.file_scroll = Scrollbar(self.master, orient=VERTICAL)
        self.file_list['yscrollcommand'] = self.file_scroll.set
        self.file_scroll['command'] = self.file_list.yview
        # place the widget
        self.file_list.grid(row=1, column=2, rowspan=1, columnspan=2, sticky=N + S + E)
        self.file_scroll.grid(row=1, column=2, rowspan=1, columnspan=2, sticky=N + S + E)

        # sub-directories list
        self.dir_list = Listbox(self.master, height=3)
        self.dir_list.bind('<<ListboxSelect>>', self.on_dir_select)
        self.dir_scroll = Scrollbar(self.master, orient=VERTICAL)
        self.dir_list['yscrollcommand'] = self.dir_scroll.set
        self.dir_scroll['command'] = self.dir_list.yview
        # place the widget
        self.dir_list.grid(row=1, column=4, rowspan=1, columnspan=1, sticky=N + S + E)
        self.dir_scroll.grid(row=1, column=4, rowspan=1, columnspan=1, sticky=N + S + E)

        # refresh list widgets
        self.mlt_lib = get_content(self.directory)
        self.refresh_list_items()

    def refresh_list_items(self):
        self.file_list.delete(0, END)
        self.dir_list.delete(0, END)
        self.bar_node['text'] = 'Location : {0}'.format(self.directory)
        for mlt_file in self.mlt_lib.keys():
            if os.path.isdir(self.mlt_lib[mlt_file]):
                self.dir_list.insert('end', mlt_file)
            elif os.path.isfile(self.mlt_lib[mlt_file]):
                self.file_list.insert('end', mlt_file)
            else:
                print 'item {0} does not fit ({1})'.format(mlt_file, self.mlt_lib[mlt_file])

    def on_up_select(self):
        directory = get_directory_from_file(self.mlt_lib[next(iter(self.mlt_lib))])
        separator = get_separator_from(directory)
        # TODO: check if not jumping outsine main dir
        self.directory = separator.join(directory.split(separator)[0:-1])
        print 'navigate one level up to: {0}'.format(self.directory)
        self.mlt_lib = get_content(self.directory)
        self.refresh_list_items()

    def on_dir_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'navigate to %d: "%s"' % (index, value)
        self.directory = get_proper_dir_path(self.directory) + value
        self.mlt_lib = get_content(self.directory)
        self.refresh_list_items()

    def on_file_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'You selected item %d: "%s"' % (index, value)
        self.canvas.delete('all')
        if 'gif' in value or '.jpg' in value or '.png' in value:
            if 'gif' in value:
                image_obj = PhotoImage(file=self.mlt_lib[value])
            elif '.jpg' in value or '.png' in value:
                image_obj = ImageTk.PhotoImage(Image.open(self.mlt_lib[value]))
            else:
                image_obj = PhotoImage(file=self.mlt_lib[value])
            if image_obj._PhotoImage__size[0] > 200:
                if image_obj._PhotoImage__size[0] > 600:
                    x = 0  # must resize picture
                    y = 0
                else:
                    x = 0
                    y = 0
            else:
                x = (600 / 2) - (image_obj._PhotoImage__size[0] / 2)
                y = (600 / 2) - (image_obj._PhotoImage__size[1] / 2)
            self.canvas.image = image_obj
            self.canvas.create_image(x, y, image=image_obj, anchor="nw")
        else:
            self.canvas.create_text(50, 150, text=read_file(self.mlt_lib[value]))
            self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
            # self.master.update_idletasks()


class SimpleTable(Frame):
    def __init__(self, master, rows=5, columns=3):
        # use black background so it "peeks through" to form grid lines
        self.master = master
        Frame.__init__(self, self.master.master, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = Label(self, text="%s/%s" % (row+2, column+2),
                                 borderwidth=0, width=10)
                label.grid(row=row+2, column=column+2, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column+2, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


def build_window(init_directory):
    root = Tk()

    root.title('Hvězdná encyklopedie')
    root.resizable(0, 0)
    root.geometry('900x750')

    global directory
    directory = init_directory
    # global mlt_lib
    # mlt_lib = get_mlt_lib(navigate_to(directory))

    MainWindow(root)  # .pack(side="top", fill="both", expand=True)
    root.mainloop()


def get_content(path_to):
    """return multimedia library in format:
    mlt_lib = {'filename': '/path/to/filename'}
    mlt_lib = {'/dirname': '/path/to/dir'}
    """
    path_to = get_proper_dir_path(path_to)
    mlt_lib = {}
    for mlt_file in os.listdir(path_to):
        if os.path.isdir(path_to + mlt_file):
            mlt_lib[mlt_file] = path_to + mlt_file
        else:
            mlt_lib[mlt_file] = path_to + mlt_file
    return mlt_lib


def get_sub_dirs(directory):
    sub_dir_lib = {}
    for sub_dir in directory:
        sub_dir_lib[sub_dir] = 'aaaa - build full pathh to file'


def get_proper_dir_path(path):
    separator = get_separator_from(path)
    if not path.endswith(separator):
        path += separator
    return path


def fill(image, color):
    """Fill image with a color=(r,b,g)"""
    r, g, b = color
    width = image.width()
    height = image.height()
    hexcode = '#%02x%02x%02x' % (r, b, g)
    horizontal_line = '{' + ' '.join([hexcode] * width) + '}'
    image.put(' '.join([horizontal_line] * width))


def get_directory_from_file(path):
    separator = get_separator_from(path)
    # strip filename from path
    return separator.join(path.split(separator)[0:-1])

def get_separator_from(path):
    if '\\' in path:
        separator = '\\'
    elif '/' in path:
        separator = '/'
    return separator

def build_categories(he, parent_node):
    for root_node in he.enc:
        print root_node['code']
        insert_menu_item(1, root_node['code'])
        for sub_node in root_node['child']:
            insert_menu_item(2, sub_node['code'])
            if sub_node['code'] == get_nth_node(2, parent_node):
                for sub_sub_node in sub_node:
                    insert_menu_item(3, root_node['code'])


def insert_menu_item(level, node):
    # label = Label(root, text=str(node))
    label = Button(root, text=node, command=on_button_click)
    label["command"] = 'goto direcotry'
    label.grid(row=0, column=level + 1, pady=1)


def get_nth_node(nth, parent_node):
    try:
        if nth == 1:
            return get_nth_number(nth, parent_node) * 100
        elif nth == 2:
            return (get_nth_number(nth - 1, parent_node) * 100) + (get_nth_number(nth, parent_node) * 10)
        else:
            return parent_node
    except:
        return 800
        # not defined node, return max


def get_nth_number(nth, node_number):
    return int(str(node_number)[nth - 1:nth])


def read_file(filename):
    with open(filename, 'r') as content_file:
        content = content_file.read()
    if 'htm' in filename.split()[-1]:
        content = TextProcess.htm_to_plain_txt(content)
    return content


def get_image():
    """get values that user clicked on"""
    mlt_img['image'] = mlt_lib[lb.get('active')]


def navigate_to(directory):
    if os.path.isdir(directory):
        checked_directory = directory
    else:
        checked_directory = os.path.basename(__file__)
        print 'cannot find the directory {0}, using {1}'.format(directory, checked_directory)

    return checked_directory


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run over dir")
    parser.add_argument('-d', help='directory', type=str, default='')
    args = parser.parse_args()

    build_window(args.d)
