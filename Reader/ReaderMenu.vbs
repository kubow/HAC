Const DBPath = "C:\_Run\Script\Reader\Reader.accdb"

Set AccessApp = GetObject(DBPath, "Access.Application")
AccessApp.Run "RestLogVar"
Set AccessApp = Nothing
