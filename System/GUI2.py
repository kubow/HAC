#https://www.youtube.com/watch?v=eL_sy9TqCBE
#http://www.sharpertradingimage.com/python-listbox-delete-text/
from Tkinter import *

root = Tk()

filename = 'c:\\Users\\JAV\\Dropbox\\Web\\64\\Astrologie\\Planet2.gif'
txtng = 'showing picture in list'
img = PhotoImage(file=filename)

label = Label(root, image=img, text='sadasdsadassdds')
button = Button(root, text=txtng)

# listbox
lb = Listbox(root, height=5)
lb.insert(0, 'new')
lb.insert(0, 'two')
lb.insert(0, 'duo')

label.grid(row=0, column=0, sticky="wn")
button.grid(row=1, column=0)
lb.grid(row=0, column=1, rowspan=2)
root.mainloop()