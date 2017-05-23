#https://www.youtube.com/watch?v=eL_sy9TqCBE
#http://www.sharpertradingimage.com/python-listbox-delete-text/
from Tkinter import *
impoert os

def get_image():
    mlt_img['image'] = mlt_lib[lb.get('active')]

def get_mlt_lib(directory):
    mlt_lib = {}
    for mlt_file in os.listdir(directory):
        # for now just images
        if not '.gif' in mlt_file:
            continue
        mlt_lib[mlt_file]

root = Tk()

mlt_lib = {
    'new1': PhotoImage(file='/home/kubow/Dropbox/Web/64/Astrologie/Planet2.gif'),
    'new2': PhotoImage(file='/home/kubow/Dropbox/Web/64/Astrologie/tiamatsplit.gif'),
    'win1': PhotoImage(file='/home/kubow/Dropbox/Web/64/Astrologie/Nibiru-Smites-2.gif')
    #'win1': PhotoImage(file='c:\\Users\\JAV\\Dropbox\\Web\\64\\Astrologie\\Planet2.gif')
    }

#img = PhotoImage(file=filename)

txtng = 'showing picture in list'
mlt_img = Label(root, image=mlt_lib['new1'], text='sadasdsadassdds')
button = Button(root, text=txtng, command=get_image)

# listbox
lb = Listbox(root, height=7)
for img in mlt_lib.keys():
    lb.insert('end', img)

yscroll = Scrollbar(root, orient=VERTICAL)
lb['yscrollcommand'] = yscroll.set
yscroll['command'] = lb.yview

mlt_img.grid(row=0, column=0, sticky="wn")
button.grid(row=1, column=0)
lb.grid(row=0, column=1, rowspan=2, sticky=N+S)
yscroll.grid(row=0, column=1, rowspan=2, sticky=N+S+E)

root.mainloop()
