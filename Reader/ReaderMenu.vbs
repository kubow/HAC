Option Explicit
dim fs: Set fs = CreateObject("Scripting.FileSystemObject")
Dim cf: cf = fs.GetAbsolutePathName(".") 'CurrentFolder
Dim of: Set of = fs.GetFolder(cf) 'ObjectFolder
Dim outHTML: outHTML = "C:\_Run\Script\Reader\karty\index.htm" 'OutputFileName
dim CardURL: CardURL = "http://hifis/karty/index2.php"
dim xmlHTTP: Set xmlHTTP = CreateObject("MSXML2.XMLHTTP.6.0")
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
