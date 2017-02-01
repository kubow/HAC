from Tkinter import *
import os.path
import sqlite3

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

mainwindow = Tk()
mainwindow.title("aplicacion beta v00")

mainwindow.geometry("200x120")
center(mainwindow)

mainwindow.mainloop()