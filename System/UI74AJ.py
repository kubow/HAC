from appJar import gui
from OS74 import FileSystemObject
from SO74DB import DataBaseObject

def opt_changed():
    result_set = db_obj.return_many('SELECT * FROM {0};'.format(app.getOptionBox("optionbox")))
    first_columns = [record[0] for record in result_set]
    app.clearListBox("list", callFunction=False)
    app.addListItems("list", first_columns)

def lst_changed():
    record_value = app.getListBox("list")
    print(record_value)

def press(btn):
    if btn == "Storno":
        app.stop()
    elif btn == "Zapsat":
        list_select()
    else:
        print('not defined yet')

def list_select():
    app.infoBox("Info", "You selected " + app.getOptionBox("optionbox") + "\nBrowsing " + app.getListBox("list")[0][0])

root = FileSystemObject(FileSystemObject().one_dir_up()).one_dir_up()
print(root)
db_file = FileSystemObject(root).append_file("H808E_tab.db")
db_obj = DataBaseObject(db_file)
db_obj_list = [obj[0] for obj in db_obj.view_list]

app = gui("Database Editor", "500x500")
app.setPadding(10, 10)
app.setFont(12)
# app.addHorizontalSeparator(0,0,4, colour="red")
app.addLabel("title", "Hvezdna encyklopedie", 0, 0)
app.addOptionBox("optionbox", db_obj_list, 0, 2)

app.addLabel("en1", "nazev", 1, 0)
app.addEntry("e1", 1, 1)
app.addLabel("en2", "hodnota", 2, 0)
app.addEntry("e2", 2, 1)
app.addLabel("en3", "neco_jineho", 3, 0)
app.addEntry("e3", 3, 1)

app.addListBox("list", db_obj.return_many('SELECT nazev FROM suroviny;'), 1, 2)
app.addButtons(["Zapsat", "Storno"], press, 4, 0)

app.setOptionBoxChangeFunction("optionbox", opt_changed)
app.setListBoxChangeFunction("list", lst_changed)

# start the GUI
app.go()
