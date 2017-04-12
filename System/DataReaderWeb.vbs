Option Explicit
'Dim ws: Set ws = CreateObject("WScript.Shell")
Dim fs: Set fs = CreateObject("Scripting.FileSystemObject")
Dim cf: cf = fs.GetAbsolutePathName(".") 'CurrentFolder
'Dim cf: cf = fs.GetParentFolderName(WScript.ScriptFullName) 'ws.CurrentDirectory 'fs.GetAbsolutePathName(".") 'CurrentFolder
Dim of: Set of = fs.GetFolder(cf) 'ObjectFolder

'''''''''''' main logic ''''''''''''
Dim mode: mode = 0
If mode = 0 then 'websites reading
    Dim outHTML: outHTML = "C:\_Run\Script\Reader\karty\index.htm" 'OutputFileName
    Dim CardURL: CardURL = "http://hifis/karty/index2.php"
    Dim xmlHTTP: Set xmlHTTP = CreateObject("MSXML2.XMLHTTP.6.0")
    xmlHTTP.open "get", CardURL, False 'True
    xmlHTTP.send
    Wscript.Sleep 5000	'wait till ie finishes loading (ms)
    rem workaround http://stackoverflow.com/questions/16566594/can-someone-tell-me-why-i-am-not-getting-a-response-to-msxml2-serverxmlhttp-6-0
    If xmlHTTP.Status = 200 Then
        If (fs.FileExists(outHTML)) Then
            fs.DeleteFile outHTML, True
        End If
        dim outFile: Set outFile = fs.CreateTextFile(outHTML, True, True) 'overwrite, unicode
        'MsgBox xmlHTTP.ResponseText
        dim html: Set html = CreateObject("HTMLFile")
        'dim html: Set html = CreateObject("ADODB.Stream")
        dim textstream: textstream = BinaryToString(xmlHTTP.ResponseBody)
        html.write "<html><body></body></html>"
        html.body.innerHTML = textstream
        dim objTable: objTable = html.getElementsByTagName("table") 
        'MsgBox html.body.innerHTML
        outFile.Write("<!DOCTYPE html>" & vbNewLine & "<html>" & vbNewLine & "<head>" & vbNewLine & "<meta charset=" & Chr(34) & "windows-1250" & Chr(34) & ">" & vbNewLine & "<title>Karty</title>" & vbNewLine)
        outFile.Write("<link rel=" & Chr(34) & "stylesheet" & Chr(34) & " type=" & Chr(34) & "text/css" & Chr(34) & " href=" & Chr(34) & "../style.css" & Chr(34) & ">" & vbNewLine & "</head>" & vbNewLine & "<body>" & vbNewLine & "<table>" & vbNewLine)
        outFile.Write(objTable.innerHTML) 'xmlHTTP.ResponseText
        outFile.Write("</table>" & vbNewLine & "</body>" & vbNewLine & "</html>")
    End If
    Set fs = Nothing
    outFile.Close
Else 'run access version
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
    End If

Function BinaryToString(byVal Binary)	'--- Converts the binary content to text using ADODB Stream

    BinaryToString = ""		'--- Set the return value in case of error

    Dim BinaryStream		'--- Creates ADODB Stream
    Set BinaryStream = CreateObject("ADODB.Stream")

    '--- Specify stream type.
    BinaryStream.Type = 1 '--- adTypeBinary

    BinaryStream.Open		'--- Open the stream And write text/string data To the object
    BinaryStream.Write Binary

    BinaryStream.Position = 0	'--- Change stream type to text
    BinaryStream.Type = 2 '--- adTypeText

    '--- Specify charset for the source text (unicode) data.
    BinaryStream.CharSet = "windows-1250" '"UTF-8"

    BinaryToString = BinaryStream.ReadText	'--- Return converted text from the object
End Function

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