' Created by Jakub Vajda on 29.9.2016 - use to read restaurant menu

Option Explicit
'Dim ws: Set ws = CreateObject("WScript.Shell")
Dim fs: Set fs = CreateObject("Scripting.FileSystemObject")
Dim cf: cf = fs.GetParentFolderName(WScript.ScriptFullName) 'ws.CurrentDirectory 'fs.GetAbsolutePathName(".") 'CurrentFolder
Dim rm: rm = cf & "\RestMenu"
'Dim of: Set of = fs.GetFolder(cf) 'ObjectFolder
Dim DBPath: DBPath = cf & "\Reader.db"

Dim DBConn: Set DBConn = CreateObject("ADODB.Connection")
Dim oCS: oCS = "Driver={SQLite3 ODBC Driver};Database=" & DBPath & ";StepAPI=;Timeout="
DBConn.Open oCS

Dim sSQL: sSQL = "SELECT * FROM RestActive"
Dim oRS: Set oRS = DBConn.Execute(sSQL)

Dim sf: sf = GetFileContent(cf & "\HTML_head.txt")
Dim ef: ef = GetFileContent(cf & "\HTML_tail.txt")

Do While Not oRS.EOF
	If Len(oRS.Fields.Item("Address"))<1 Then
		DataRead oRS.Fields.Item("ZomatoAddress"), oRS.Fields.Item("Shortcut"), "daily-menu-container"
	Else
		DataRead oRS.Fields.Item("Address"), oRS.Fields.Item("Shortcut"), oRS.Fields.Item("Shortcut")
	End If
	oRS.MoveNext
Loop

DBConn.Close
Set DBConn = Nothing

Function DataRead(sAddress, sName, sID)
	Dim ie: Set ie = CreateObject("InternetExplorer.Application") 'open IE in memory, and go to website
	ie.Visible = False 'True
	ie.navigate sAddress
	'READYSTATE_UNINITIALIZED = 0, READYSTATE_LOADING = 1, READYSTATE_LOADED = 2, READYSTATE_INTERACTIVE = 3, READYSTATE_COMPLETE = 4
	Do While ie.Busy Or ie.ReadyState <> 4 'READYSTATE_COMPLETE   'Wait until IE is done loading page
		WScript.Sleep 100
	Loop
	Dim html: Set html = ie.Document  'HTML document returned
	Dim MainBox: Set MainBox = html.getElementById(sID)
	Dim shtml: shtml = MainBox.innerHTML
	'MsgBox MainBox.innerText
	ie.Quit
	Set ie = Nothing    'close down IE and reset status bar
	If fs.FileExists(rm & "\" & sName & ".htm") Then
		fs.DeleteFile(rm & "\" & sName & ".htm")
	End If
	fs.CreateTextFile(rm & "\" & sName & ".htm")
	Dim NewFile: Set NewFile = fs.OpenTextFile(rm & "\" & sName & ".htm",2)
	NewFile.Write(sf)
	NewFile.Write(shtml)
	NewFile.Write(ef)
	NewFile.Close
End Function

Function GetFileContent(sFileAddress)
	Dim sContent: sContent = ""
	Dim nf: Set nf = fs.OpenTextFile(sFileAddress)
	Do Until nf.AtEndOfStream
		sContent = sContent & nf.ReadLine & vbCrLf
	Loop
	nf.Close
	GetFileContent = sContent
End Function