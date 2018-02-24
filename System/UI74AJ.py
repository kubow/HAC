from appJar import gui
import sys
from SO74DB import DataBaseObject

def press(btn):
    if btn == "Storno":
        app.stop()
    elif btn == "Zapsat":
        print('db.commit')
    else:
        app.showSubWindow("Pets")

if len(sys.argv) > 1:
    db_file = sys.argv[1]

    app = gui("Database Editor", "500x500")
    app.setFont(20)

    db_obj = DataBaseObject(db_file)
    app.addLabel("title", "Hvezdna encyklopedie")
    # app.addOptionBox("optionbox", ["Assembler", "C", "C++", "Perl", "Python"])
    app.addOptionBox("optionbox", db_file.obj_list)
    app.addButtons(["Zapsat", "Storno"], press)
    app.startSubWindow("Pets")
    app.stopSubWindow()

    # start the GUI
    app.go()
else:
    print('please submit database file')