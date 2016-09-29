' Created by Jakub Vajda on 29.9.2016 - use to read restaurant menu

Option Explicit
Dim fs: Set fs = CreateObject("Scripting.FileSystemObject")
Dim cf: cf = fs.GetAbsolutePathName(".") 'CurrentFolder
'Dim of: Set of = fs.GetFolder(cf) 'ObjectFolder
Dim DBPath: DBPath = cf & "\Reader.db"

Dim DBConn: Set DBConn = CreateObject("ADODB.Connection")
Dim oCS: oCS = "Driver={SQLite3 ODBC Driver};Database=" & DBPath & ";StepAPI=;Timeout="
DBConn.Open oCS

Dim sSQL: sSQL = "SELECT * FROM RestActive"
Dim oRS: Set oRS = DBConn.Execute(sSQL)

Do While Not oRS.EOF
	If Len(oRS.Fields.Item("Address"))<1 Then
		'MsgBox oRS.Fields.Item("ZomatoAddress")
		DataRead oRS.Fields.Item("ZomatoAddress"), oRS.Fields.Item("Shortcut")
	Else
		DataRead oRS.Fields.Item("Address"), oRS.Fields.Item("Shortcut")
	End If
	oRS.MoveNext
Loop

DBConn.Close
Set DBConn = Nothing

Function DataRead(sAddress, sName)
	Dim ie: Set ie = CreateObject("InternetExplorer.Application")   'open Internet Explorer in memory, and go to website
	ie.Visible = True 'True
    ie.navigate sAddress
	'READYSTATE_UNINITIALIZED = 0, READYSTATE_LOADING = 1, READYSTATE_LOADED = 2, READYSTATE_INTERACTIVE = 3, READYSTATE_COMPLETE = 4
	Do While ie.Busy Or ie.ReadyState <> 4 'READYSTATE_COMPLETE   'Wait until IE is done loading page
	    WScript.Sleep 100
	Loop
	Dim html: Set html = ie.Document  'show text of HTML document returned
	Dim MainBox: Set MainBox = html.getElemntById("daily-menu-container")
	MsgBox html
	ie.Quit
	Set ie = Nothing    'close down IE and reset status bar
	
	'Dim NewFile: Set NewFile = fs.GetFile(cf & "\trp.htm")
	
End Function

'Set AccessApp = GetObject(DBPath, "Access.Application")

'    On Error Resume Next
'    
'    Dim html 'to refer to the HTML document returned
'    Dim MainBox
'    Dim Elements
'   Dim Element
'	
' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'
'MsgBox of & "\trp.htm" &vbNewLine & html.innerText

'    Set MainBox = html.getElementById("content")
'    REM Set Elements = MainBox.Children

    REM For Each Element In Elements
        REM NewFile.WriteLine Element.innerText       'html.documentElement.innerHTML
    REM 'NewFile.WriteLine html.documentElement.innerHTML
    REM Next
'    NewFile.Close
'	
' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
