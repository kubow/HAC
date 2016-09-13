import os
import wx
from ObjectListView import ObjectListView, ColumnDefn
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers
 
########################################################################
class GenericDBClass(object):
    """"""
    pass
 
########################################################################
class MainPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.db_data = []
        self.current_directory = os.getcwd()
 
        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.dataOlv.Hide()
 
        # Allow the cell values to be edited when double-clicked
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
 
        # load DB
        loadDBBtn = wx.Button(self, label="Load DB")
        loadDBBtn.Bind(wx.EVT_BUTTON, self.loadDatabase)
        self.table_names = []
        self.tableCbo = wx.ComboBox(self, value="", choices=self.table_names)
        self.tableCbo.Bind(wx.EVT_COMBOBOX, self.loadTable)
 
        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
 
        mainSizer.Add(loadDBBtn, 0, wx.ALL|wx.CENTER, 5)
        mainSizer.Add(self.tableCbo, 0, wx.ALL|wx.CENTER, 5)
        mainSizer.Add(self.dataOlv, 1, wx.ALL|wx.EXPAND, 5)
 
        self.SetSizer(mainSizer)
 
    #----------------------------------------------------------------------
    def loadTable(self, event):
        """"""
        print
        current_table = self.tableCbo.GetValue()
        metadata = MetaData(self.engine)
        table = Table(current_table, metadata, autoload=True, autoload_with=self.engine)
        self.columns = table.columns.keys()
 
        clear_mappers() #http://docs.sqlalchemy.org/en/rel_0_6/orm/mapper_config.html#sqlalchemy.orm.clear_mappers
        mapper(GenericDBClass, table)
 
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.db_data = session.query(GenericDBClass).all()
 
        self.setData()
        self.dataOlv.Show()
        self.Layout()
 
    #----------------------------------------------------------------------
    def loadDatabase(self, event):
        """"""
        wildcard = "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.current_directory,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            db_path = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
 
        self.engine = create_engine('sqlite:///%s' % db_path, echo=True)
 
        self.table_names = self.engine.table_names()
        self.tableCbo.SetItems(self.table_names)
        self.tableCbo.SetValue(self.table_names[0])
        self.loadTable("")
 
    #----------------------------------------------------------------------
    def setData(self, data=None):
        olv_columns = []
        for column in self.columns:
            olv_columns.append(ColumnDefn(column.title(), "left", 120, column.lower()))
        self.dataOlv.SetColumns(olv_columns)
 
        self.dataOlv.SetObjects(self.db_data)
 
########################################################################
class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title="Database Viewer", size=(800,600))
        panel = MainPanel(self)
 
########################################################################
class GenApp(wx.App):
 
    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
 
    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True
 
#----------------------------------------------------------------------
def main():
    """
    Run the demo
    """
    app = GenApp()
    app.MainLoop()
 
if __name__ == "__main__":
    main()
