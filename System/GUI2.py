#https://www.youtube.com/watch?v=eL_sy9TqCBE
#http://www.sharpertradingimage.com/python-listbox-delete-text/
from Tkinter import *
import os
import argparse

def get_image():
    mlt_img['image'] = mlt_lib[lb.get('active')]

def get_mlt_lib(directory):
    """return multimedia library in format:
    mlt_lib = {'filename': PhotoImage(file='*.gif')}
    """
    mlt_lib = {}
    for mlt_file in os.listdir(directory):
        # for now just images
        if not '.gif' in mlt_file:
            continue
        mlt_lib[mlt_file] = PhotoImage(file=directory+mlt_file)
    return mlt_lib

def onselect(evt):
    w = evt.widget
    print w.curselection()
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)
    mlt_img['image'] = mlt_lib[value]

def multimedia_list():
    # list of multimedia files (gif images)
    lb = Listbox(root, height=7)
    lb.bind('<<ListboxSelect>>', onselect)
    for img in mlt_lib.keys():
        lb.insert('end', img)
    
    yscroll = Scrollbar(root, orient=VERTICAL)
    lb['yscrollcommand'] = yscroll.set
    yscroll['command'] = lb.yview

    mlt_img.grid(row=0, column=0, sticky="wn")
    
    lb.grid(row=0, column=1, rowspan=2, sticky=N+S)
    yscroll.grid(row=0, column=1, rowspan=2, sticky=N+S+E)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run over dir")
    parser.add_argument('-d', help='directory', type=str, default='')
    args = parser.parse_args()
    # temporarily run over one dir, will be browser further
    #implement max image size
    root = Tk()
    #img = PhotoImage(file=filename)
    if os.path.isdir('c:\\Users\\JAV\\Dropbox\\Web\\64\\Astrologie\\'):
        mlt_lib = get_mlt_lib('c:\\Users\\JAV\\Dropbox\\Web\\64\\Astrologie\\')
    else:
        mlt_lib = get_mlt_lib('/home/kubow/Dropbox/Web/64/Astrologie/')
        
    txtng = 'showing picture in list'
    mlt_img = Label(root, image=mlt_lib[next(iter(mlt_lib))])
    #button = Button(root, text=txtng, command=get_image)
    #button.grid(row=1, column=0)
    bar = Menu(root, background='red', relief='flat')
    multimedia_list()
    
    root.mainloop()
