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

def press(link):
    app.infoBox("Info", "You clicked the link!")

db_file = "C:\_Run\H808E_tab.db"
db_obj = DataBaseObject(db_file)
db_obj_list = [obj[0] for obj in db_obj.view_list]

app = gui("Database Editor", "500x500")
app.setFont(20)
app.addHorizontalSeparator(0,0,4, colour="red")
# app.addLabel("title", "Hvezdna encyklopedie")
# app.addOptionBox("optionbox", ["Assembler", "C", "C++", "Perl", "Python"])
app.addOptionBox("optionbox", db_obj_list)

app.addEntry("e1")
app.addEntry("e2")
app.addEntry("e3")
app.addButtons(["Zapsat", "Storno"], press)
app.startSubWindow("Pets")
app.stopSubWindow()

# start the GUI
app.go()