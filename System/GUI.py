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
        self.frame = Frame(self.master)

        # upper menu
        self.bar_main = Label(self.master, text=' Main Menu ...')
        self.bar_node = Label(self.master, text='Location : {0}'.format('C:\\'))
        self.bar_main.grid(row=0, column=0, sticky=W)
        self.bar_node.grid(row=0, column=1, sticky=E)

        # multimedia view window
        self.canvas = Canvas(self.master, bd=0, highlightthickness=0, width=600, height=600, background="white")
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
        # fill with values
        for mlt_file in mlt_lib.keys():
            self.file_list.insert('end', mlt_file)

        # sub-directories list
        self.dir_list = Listbox(self.master, height=3)
        self.dir_list.bind('<<ListboxSelect>>', self.on_dir_select)
        self.dir_scroll = Scrollbar(self.master, orient=VERTICAL)
        self.dir_list['yscrollcommand'] = self.dir_scroll.set
        self.dir_scroll['command'] = self.dir_list.yview
        # place the widget
        self.dir_list.grid(row=1, column=4, rowspan=1, columnspan=1, sticky=N + S + E)
        self.dir_scroll.grid(row=1, column=4, rowspan=1, columnspan=1, sticky=N + S + E)

        # buttons upper right
        self.one_up = Button(self.master, text='one level up', command=one_up)
        self.one_up.grid(row=0, column=2, sticky=W)

    def rebuild_window(self, master, directory):
        self.master = master
        self.refresh_file_list(get_mlt_lib(navigate_to(directory)))

    def refresh_file_list(self, master):
        self.master = master
        self.file_list.delete(0, END)
        print 'a'
        for mlt_file in mlt_lib.keys():
            self.file_list.insert('end', mlt_file)

    def on_file_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'You selected item %d: "%s"' % (index, value)
        self.canvas.delete('all')
        if 'jpg' in value or 'png' in value or 'gif' in value:
            if mlt_lib[value]._PhotoImage__size[0] > 200:
                if mlt_lib[value]._PhotoImage__size[0] > 600:
                    x = 0 # must resize picture
                    y = 0
                else:
                    x = 0
                    y = 0
            else:
                x = (600 / 2) - (mlt_lib[value]._PhotoImage__size[0] / 2)
                y = (600 / 2) - (mlt_lib[value]._PhotoImage__size[1] / 2)
            self.canvas.create_image(x, y, image=mlt_lib[value], anchor="nw")
        else:
            self.canvas.create_text(50, 50, text=read_file(mlt_lib[value]))
            # self.master.update_idletasks()

    def on_dir_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'navigate to %d: "%s"' % (index, value)
        self.rebuild_window(self, value)

    def on_button_click(self):
        print 'You clicked button: '
        # w = evt.widget
        # refresh_window(w.config('text')[-1])


def build_window(directory):
    root = Tk()

    root.title('Hvězdná encyklopedie')
    root.resizable(0, 0)
    root.geometry('900x700')

    global mlt_lib
    mlt_lib = get_mlt_lib(navigate_to(directory))

    MainWindow(root)  # .pack(side="top", fill="both", expand=True)
    root.mainloop()


def get_mlt_lib(directory):
    """return multimedia library in format:
    mlt_lib = {'filename': PhotoImage(file='*.gif')}
    """
    mlt_lib = {}
    # print 'running over ' + directory
    for mlt_file in os.listdir(directory):
        if os.path.isdir(directory + mlt_file):
            continue
        if '.gif' in mlt_file:
            mlt_lib[mlt_file] = PhotoImage(file=directory + mlt_file)
        elif '.jpg' in mlt_file or '.png' in mlt_file:
            # print 'jpeg image file'
            mlt_lib[mlt_file] = ImageTk.PhotoImage(Image.open(directory + mlt_file))
        else:
            # XLS, HTML, EPUB, DOC ... in future
            mlt_lib[mlt_file] = directory + mlt_file
    return mlt_lib


def get_sub_dirs(direcotry):
    sub_dir_lib = {}
    for sub_dir in directory:
        sub_dir_lib[sub_dir] = 'aaaa - build full pathh to file'


def fill(image, color):
    """Fill image with a color=(r,b,g)"""
    r, g, b = color
    width = image.width()
    height = image.height()
    hexcode = '#%02x%02x%02x' % (r, b, g)
    horizontal_line = '{' + ' '.join([hexcode] * width) + '}'
    image.put(' '.join([horizontal_line] * width))


def one_up():
    first_file = mlt_lib[next(iter(mlt_lib))]
    if '\\' in first_file:
        separator = '\\'
    elif '/' in first_file:
        separator = '/'

    # strip filename from path
    directory = separator.join(first_file.split(separator)[0:-1])

    # go one level up
    new_directory = separator.join(directory.split(separator)[0:-1])
    print 'should switch to: ' + new_directory
    # refresh_window(navigate_to(new_directory))


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
