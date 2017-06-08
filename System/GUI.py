# -*- coding: utf-8 -*-
import os
import argparse
# https://www.youtube.com/watch?v=eL_sy9TqCBE
# http://www.sharpertradingimage.com/python-listbox-delete-text/
from Tkinter import *

# for other image support
from PIL import Image  # , ImageTk
import H808E


def get_image():
    """get values that user clicked on"""
    mlt_img['image'] = mlt_lib[lb.get('active')]


def get_mlt_lib(directory):
    """return multimedia library in format:
    mlt_lib = {'filename': PhotoImage(file='*.gif')}
    """
    mlt_lib = {}
    print 'running over ' + directory
    for mlt_file in os.listdir(directory):
        # for now just images
        if '.gif' in mlt_file:
            mlt_lib[mlt_file] = PhotoImage(file=directory + mlt_file)
        # elif '.jpg' in mlt_file or '.png' in mlt_file:
            # print 'jpeg image file'
            # image = Image.open(directory+mlt_file)
            # mlt_lib[mlt_file] = PhotoImage(image)
        else:
            # XLS, HTML, EPUB, DOC ... in future
            mlt_lib[mlt_file] = create_text(text=read_file(directory + mlt_file))
            continue
    return mlt_lib


def onselect(evt):
    w = evt.widget
    print w.curselection()
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)
    # mlt_img['image'] = mlt_lib[value]
    canvas.delete('all')
    canvas.create_image(0, 0, image=mlt_lib[value], anchor="nw")
    # root.update_idletasks()


def fill(image, color):
    """Fill image with a color=(r,b,g)"""
    r, g, b = color
    width = image.width()
    height = image.height()
    hexcode = '#%02x%02x%02x' % (r, b, g)
    horizontal_line = '{' + ' '.join([hexcode] * width) + '}'
    image.put(' '.join([horizontal_line] * width))


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
    #label = Label(root, text=str(node))
    label = Button(root, text = node)
    label["command"] = 'goto direcotry'
    label.grid(row = 0, column = level, pady = 1)


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


def build_window(directory, he):
    global root
    root = Tk()
    root.title('Hvězdná encyklopedie')
    root.resizable(0, 0)
    root.geometry('900x700')

    # img = PhotoImage(file=filename)
    # build directory multimedia list
    global mlt_lib
    if os.path.isdir(directory):
        mlt_lib = get_mlt_lib(directory)
    else:
        print 'cannot find the directory {0}'.format(directory)

    # content = Frame(root)
    # frame = Frame(content, borderwidth=5, relief="sunken", width=800, height=400)
    # photo = PhotoImage(width=32, height=32)
    # fill(photo, (255,0,0))
    # photo.grid(row=0, column=0)
    # part holding multimedia content
    # global mlt_img
    # mlt_img = Label(root, image=mlt_lib[next(iter(mlt_lib))])
    # bar = Menu(root, background='red', relief='flat')
    bar_main = Label(root, text=' Main Menu ...')
    bar_node = Label(root, text=' show location...')
    build_categories(he, 410)
    # implement max image size
    global canvas
    canvas = Canvas(root, bd=0, highlightthickness=0, width=700, height=700)
    # canvas.create_image(0, 0, image=mlt_lib[next(iter(mlt_lib))])
    canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
    canvas.create_text(20, 30, anchor=W, font="Purisa", text="Most relationships seem so transitory")

    # part holding list of multimedia files
    lb = Listbox(root, height=7)
    lb.bind('<<ListboxSelect>>', onselect)
    for img in mlt_lib.keys():
        lb.insert('end', img)
    yscroll = Scrollbar(root, orient=VERTICAL)
    lb['yscrollcommand'] = yscroll.set
    yscroll['command'] = lb.yview

    # positioning
    # mlt_img.grid(row=1, column=0, rowspan=3, sticky="wn")
    canvas.grid(row=1, column=0, rowspan=2, columnspan=2, sticky=N + S)
    lb.grid(row=1, column=2, rowspan=2, columnspan=2, sticky=N + S + E)
    yscroll.grid(row=1, column=2, rowspan=2, sticky=N + S + E)
    bar_main.grid(row=0, column=0)
    bar_node.grid(row=0, column=1)

    txtng = 'showing picture in list'
    # button = Button(root, text=txtng, command=get_image)
    # button.grid(row=1, column=0)

    root.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run over dir")
    parser.add_argument('-d', help='directory', type=str, default='')
    args = parser.parse_args()

    # construct encyklopedia
    he = H808E.h808e()

    # temporarily run over one dir, will be browser further
    build_window(args.d, he)

