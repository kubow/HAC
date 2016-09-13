Const DBPath = "C:\_Run\Script\Reader\Reader.accdb"

Set AccessApp = GetObject(DBPath, "Access.Application")
AccessApp.Run "RestLogVar"
Set AccessApp = Nothing

'Option Explicit
' Tools / References / Microsoft HTML Object Library - Getting at parts of an HTML page
' Tools / References / Microsoft Internet Controls - Getting at Internet Explorer in VBA
' Created by Jakub Vajda on 25.1.2015 - use to read restaurant menu
'    On Error Resume Next
'    Dim ie: Set ie = CreateObject("InternetExplorer.Application")   'open Internet Explorer in memory, and go to website
'	Dim FSO: Set FSO = CreateObject("Scripting.FileSystemObject")'File System Object
'		Dim cf: cf = FSO.GetAbsolutePathName(".") 'CurrentFolder
'		Dim of: Set of = fs.GetFolder(cf) 'ObjectFolder
'    Dim html 'to refer to the HTML document returned
'    Dim MainBox
'    Dim Elements
'   Dim Element
'	Dim NewFile: Set NewFile = FSO.GetFile(of & "\trp.htm")
' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'    ie.Visible = True 'True
'    ie.navigate "http://restaurace-trpaslik.webnode.cz/poledni-menu/"
'READYSTATE_UNINITIALIZED = 0, READYSTATE_LOADING = 1, READYSTATE_LOADED = 2, READYSTATE_INTERACTIVE = 3, READYSTATE_COMPLETE = 4
'Do While ie.Busy Or ie.ReadyState <> 4 'READYSTATE_COMPLETE   'Wait until IE is done loading page
'    WScript.Sleep 100
'Loop

'Set html = ie.Document  'show text of HTML document returned
'MsgBox of & "\trp.htm" &vbNewLine & html.innerText

'    Set MainBox = html.getElementById("content")
'    REM Set Elements = MainBox.Children

    REM For Each Element In Elements
        REM NewFile.WriteLine Element.innerText       'html.documentElement.innerHTML
    REM 'NewFile.WriteLine html.documentElement.innerHTML
    REM Next
'    NewFile.Close
'	ie.Quit
' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'Set ie = Nothing    'close down IE and reset status bar

'Application.StatusBar = ""
'Set of = Nothing
'Set FSO = Nothing

' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~