from Tkinter import *
import ttk
import os.path
import sqlite3

def conectar(quien):
    conexion = sqlite3.connect(quien)
    return conexion

def enviar_orden_anterior_a_db(conexion):
    conexion.commit()

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def resetCliente(event):
    # 4 = raton izq
    # 2 = enter
    if int(event.type) == 2:
        #print "enter"
        accion()
    if int(event.type) == 4:
        var2.set("")

def resetStatus(event):
    status.set("Status")

def creardb():
    conexion = conectar('data.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE clientes (cliente VARCHAR(10) NOT NULL, producto VARCHAR(10) NOT NULL)''')
    enviar_orden_anterior_a_db(conexion)
    conexion.close()

def accion():
    txt = str(var2.get())

    if not os.path.isfile('data.db'):
         creardb()

    conexion = conectar('data.db')
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO clientes (cliente, producto) VALUES ('"+txt+"','"+txt+"')")
    enviar_orden_anterior_a_db(conexion)
    cursor.execute("SELECT cliente, producto FROM clientes")
    db = []
    for i in cursor:
        a = [ "Cliente: " +i[0] , " Producto: " +i[1] ]
        db.append(a)
    print(db)
    status.set(db[-1][0])

    conexion.commit()
    conexion.close()

def new_win():
    window = Tk()
    window.geometry("200x120")
    center(window)
    ttk.Label(window, text="ventana modal 1").place(x= 10, y= 10)
    ttk.Button(window, text="salir", command=window.destroy).place(x= 120, y=9)

mainwindow = Tk()
mainwindow.title("aplicacion beta v00")

mainwindow.geometry("200x120")
center(mainwindow)

status = StringVar()
status.set("Status")

var2 = StringVar()
var2.set("Cliente")


entry_text = ttk.Entry(mainwindow, width=7, textvariable=var2)
entry_text.place(x=10, y=30)
entry_text.bind("<Button-1>",resetCliente)
entry_text.bind("<Return>",resetCliente)
entry_text.focus()

# para alinear cada elemento hacia la arriba izq der abajo
ttk.Label(mainwindow, text="Aplicacion v00").place(x=10 , y=10)
be = ttk.Button(mainwindow, text="Ejecutar", command=accion).place(x= 100, y=30)
bnw = ttk.Button(mainwindow, text="New Window", command=new_win).place(x= 100, y=60)
sl = ttk.Label(mainwindow, textvariable=status)
sl.place(x=10 , y=100)
sl.bind("<Button-1>",resetStatus)

mainwindow.mainloop()