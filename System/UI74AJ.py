from appJar import gui
from OS74 import FileSystemObject
from DB74 import DataBaseObject
from Template import SQL


def opt_changed():
    result_set = db_obj.return_many('SELECT * FROM {0};'.format(app.getOptionBox("optionbox")))
    first_columns = [record[0] for record in result_set]
    app.clearListBox("list", callFunction=False)
    app.addListItems("list", first_columns)
    i = 1
    result_flds = db_obj.object_structure(app.getOptionBox("optionbox"))
    for field in result_flds:
        if i > 9:
            break
        app.setLabel('en' + str(i), field)
        i += 1
    i += 1
    if i <= 9:
        app.setLabel('en' + str(i), '')
        i += 1


def lst_changed():
    table = app.getOptionBox("optionbox")
    field_name = app.getLabel('en1')
    if app.getListBox("list"):
        record_value = app.getListBox("list")[0]
        result_vals = db_obj.return_many(SQL.select_where.format('*', table, field_name + '= "' + record_value + '"'))
        if result_vals:
            i = 1
            for field in result_vals[0]:
                if i > 6:
                    break
                app.setEntry('e' + str(i), field)
                i += 1


def press(btn):
    if btn == "Storno":
        app.stop()
    elif btn == "Zapsat":
        list_select()
    else:
        print('not defined yet')


def list_select():
    app.infoBox("Info", "You selected " + app.getOptionBox("optionbox") + "\nBrowsing " + app.getListBox("list")[0][0])

root = FileSystemObject().dir_up(2)
print(root)
db_file = FileSystemObject(root).append_objects(file="H808E_tab.db")
db_obj = DataBaseObject(db_file)
db_obj_list = [obj[0] for obj in db_obj.view_list]

app = gui("Database Editor", "800x500")
app.setPadding(10, 10)
app.setFont(12)
# app.addHorizontalSeparator(0,0,4, colour="red")
app.addLabel("title", "Hvezdna encyklopedie", 0, 0, 2)
app.addOptionBox("optionbox", db_obj_list, 0, 2)

app.addLabel("en1", "nazev", 1, 0)
app.addEntry("e1", 1, 1)
app.addLabel("en2", "hodnota", 2, 0)
app.addEntry("e2", 2, 1)
app.addLabel("en3", "neco_jineho", 3, 0)
app.addEntry("e3", 3, 1)
app.addLabel("en4", "dalsi", 4, 0)
app.addEntry("e4", 4, 1)
app.addLabel("en5", "jeste_jedna", 5, 0)
app.addEntry("e5", 5, 1)
app.addLabel("en6", "neco_jinakeho", 6, 0)
app.addEntry("e6", 6, 1)
app.addLabel("en7", "blabla", 7, 0)
app.addEntry("e7", 7, 1)
app.addLabel("en8", "hohoho", 8, 0)
app.addEntry("e8", 8, 1)
app.addLabel("en9", "neco_neco", 9, 0)
app.addEntry("e9", 9, 1)

app.addListBox("list", db_obj.return_many('SELECT nazev FROM suroviny;'), 1, 2, 1, 9)
app.addButtons(["Zapsat", "Storno"], press, 10, 0, 2)

app.setOptionBoxChangeFunction("optionbox", opt_changed)
app.setListBoxChangeFunction("list", lst_changed)

# start the GUI
app.go()
