Attribute VB_Name = "Internet"
Option Compare Database

Sub RestLog()

Dim InSet As DAO.Recordset
Set InSet = CurrentDb.OpenRecordset("Restaurants")  'otevøít tab pro pøeètení seznamu

Dim OutSet As DAO.Recordset
Set OutSet = CurrentDb.OpenRecordset("Log")  'otevøít tab Log pro záznam
'''''''''''''''''''' volitelná souèást - metoda Addnew vždy pøidá na konec
If OutSet.RecordCount <> 0 Then 'kontrola zda  vstupní tab obsahuje data
    OutSet.MoveLast     'posun na poslední zánam v seznamu pøístupù - pøíprava na append
End If
'''''''''''''''''''' konec volitelné souèásti

Dim Network As WshNetwork   'windows script host - tools/references
Set Network = New WshNetwork    'použito pro názvy uživatele/domény
Dim FSO As FileSystemObject
Dim NewFile As Object   'použito pro zápis souborù html

On Error Resume Next
    Set File = CreateObject("Msxml2.XMLHTTP")
    File.setTimeout 2000, 2000, 2000, 2000
    
If Not (InSet.EOF And InSet.BOF) Then 'kontrola zda  vstupní tab obsahuje data
    InSet.MoveFirst 'posun na první øádek - pro jistotu
    Do Until InSet.EOF = True
        On Error Resume Next
        'spustit procedury s pøíslušnými parametry
        OutSet.AddNew
        OutSet!Connection = InSet!Shortcut
        OutSet!LogDate = Now()
        OutSet!User = Network.UserName   'UserNameWin()
        OutSet!Domain = Network.UserDomain
        OutSet!CPName = InSet!RestName
        
        File.Open "GET", InSet!Address, False
        'This is IE 8 headers
        File.setRequestHeader "User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET4.0C; .NET4.0E; BCD2000; BCD2000)"
        File.send
        
        OutSet!Report = File.responseText
        
        Set FSO = New FileSystemObject
        Set NewFile = FSO.GetFile(CurrentProject.Path & "\" & InSet!Shortcut & ".htm")
        
        If Err.Number = 0 Then
            Set NewFile = FSO.OpenTextFile(CurrentProject.Path & "\" & InSet!Shortcut & ".htm")
        Else
            Set NewFile = FSO.CreateTextFile(CurrentProject.Path & "\" & InSet!Shortcut & ".htm")
        End If
        NewFile.WriteLine File.responseText
        NewFile.Close
        Set FSO = Nothing
        
        On Error GoTo 0
        
        OutSet.Update
        InSet.MoveNext  'Move to the next record. Don't ever forget to do this.
    Loop
Else
    MsgBox "Tabulka se seznamem výpoèetek je prázdná."
End If

MsgBox "Dokonèeno. Vygenerován log s tagem "

OutSet.Close 'Close the recordset
Set OutSet = Nothing 'Clean up

InSet.Close 'Close the recordset
Set InSet = Nothing 'Clean up

End Sub

Sub RestLogVar()

' Tools / References / Microsoft HTML Object Library - Getting at parts of an HTML page
' Tools / References / Microsoft Internet Controls - Getting at Internet Explorer in VBA
    On Error Resume Next
    Dim ie As InternetExplorer  'to refer to the running copy of Internet Explorer
    Dim html As HTMLDocument    'to refer to the HTML document returned
    Dim MainBox As IHTMLElement
    Dim Elements As IHTMLElementCollection
    Dim Element As IHTMLElement
    
    Dim InSet As DAO.Recordset
    Set InSet = CurrentDb.OpenRecordset("Restaurants")  'otevøít tab pro pøeètení seznamu

    Dim OutSet As DAO.Recordset
    Set OutSet = CurrentDb.OpenRecordset("Log")  'otevøít tab Log pro záznam
'''''''''''''''''''' volitelná souèást - metoda OutSet.Addnew vždy pøidá na konec
    If OutSet.RecordCount <> 0 Then 'kontrola zda  vstupní tab obsahuje data
        OutSet.MoveLast     'posun na poslední zánam v seznamu pøístupù - pøíprava na append
    End If
'''''''''''''''''''' konec volitelné souèásti
    Dim Network As WshNetwork   'windows script host - tools/references
    Set Network = New WshNetwork    'použito pro názvy uživatele/domény
    Dim FSO As FileSystemObject
    Dim NewFile As Object   'použito pro zápis souborù html
    Dim PassedText As String
    Dim RegExp As Object    'MS vbscript regular expressions - tools/references
    Set RegExp = CreateObject("vbscript.regexp")
'READYSTATE_UNINITIALIZED = 0, READYSTATE_LOADING = 1, READYSTATE_LOADED = 2, READYSTATE_INTERACTIVE = 3, READYSTATE_COMPLETE = 4
    DoCmd.RunSQL ("DELETE Log.* FROM Log;") 'vymazání log soboru

If Not (InSet.EOF And InSet.BOF) Then 'kontrola zda  vstupní tab obsahuje data
    InSet.MoveFirst 'posun na první øádek - pro jistotu
    Do Until InSet.EOF = True
        On Error Resume Next
        Set ie = New InternetExplorer   'open Internet Explorer in memory, and go to website
        ie.Visible = False
        ie.navigate InSet!Address

        Do While ie.ReadyState <> READYSTATE_COMPLETE   'Wait until IE is done loading page´
            DoEvents
        Loop

        Set html = ie.Document  'show text of HTML document returned

        'spustit procedury s pøíslušnými parametry
        OutSet.AddNew
        OutSet!Connection = InSet!Shortcut
        OutSet!LogDate = Now()
        OutSet!User = Network.UserName   'UserNameWin()
        OutSet!Domain = Network.UserDomain
        OutSet!CPName = InSet!RestName
        
        If InSet!Type = "tagID" Then
            Set MainBox = html.getElementById(InSet!Tag)
        ElseIf InSet!Type = "tagCLASS" Then
            Set MainBox = html.getElementsByClassName(InSet!Tag)
        End If
        If MainBox Is Nothing Then
            Set MainBox = html.getElementById(InSet!backup)
        End If
        OutSet!Report = MainBox.innerText
        
        Set FSO = New FileSystemObject
        Set NewFile = FSO.GetFile(CurrentProject.Path & "\jidelak\" & InSet!Shortcut & ".htm")
        
        If Len(Dir(CurrentProject.Path & "\jidelak\" & InSet!Shortcut & ".htm")) <> 0 Then
            Kill (CurrentProject.Path & "\jidelak\" & InSet!Shortcut & ".htm")
            Set NewFile = FSO.CreateTextFile(CurrentProject.Path & "\jidelak\" & InSet!Shortcut & ".htm")
        Else
            Set NewFile = FSO.CreateTextFile(CurrentProject.Path & "\jidelak\" & InSet!Shortcut & ".htm")
        End If
        
        NewFile.WriteLine "<!DOCTYPE html>" & vbNewLine & "<html>" & vbNewLine & "<head>" & vbNewLine & "<meta charset=" & Chr(34) & "windows-1250" & Chr(34) & ">" & vbNewLine & "<title>XXX</title>" & vbNewLine
        NewFile.WriteLine "<link rel=" & Chr(34) & "stylesheet" & Chr(34) & " type=" & Chr(34) & "text/css" & Chr(34) & " href=" & Chr(34) & "../style.css" & Chr(34) & ">" & vbNewLine & "</head>" & vbNewLine & "<body>" & vbNewLine
        NewFile.WriteLine "<div id=" & Chr(34) & "Box" & Chr(34) & " class=" & Chr(34) & InSet!Shortcut & Chr(34) & ">" & vbNewLine
        
        Set Elements = MainBox.Children
        For Each Element In Elements
        If Len(Element.toString) > 10 Then
            If InSet!inner_type = "HTML" Then
                With RegExp
                    .Global = True
                    .IgnoreCase = True
                    .Multiline = True
                    .Pattern = "style=" & Chr(34) & ".*?" & Chr(34)
                End With    'load regular expressions into variable
                PassedText = RegExp.Replace(Element.innerHTML, vbNullString)    'clear all style definitions from Box
                'MsgBox Pattern
                PassedText = Replace(PassedText, "&nbsp; ", vbNullString)   'speciály kvùli trpaslíkovi
                PassedText = Replace(PassedText, "&nbsp;&nbsp;", vbNullString)
                PassedText = Replace(PassedText, "<p></p>", vbNullString)
                PassedText = Replace(PassedText, "<p>&nbsp;</p>", vbNullString)
                PassedText = Replace(PassedText, "<p >&nbsp;</p>", vbNullString)
                PassedText = Replace(PassedText, "<h4 >&nbsp;</h4>", vbNullString)
                PassedText = Replace(PassedText, "<p ><strong>&nbsp;&nbsp;</strong></p>", vbNullString) 'konec speciálù kvùli trpaslíkovi
                NewFile.WriteLine PassedText & vbNewLine
                PassedText = ""
            Else
                NewFile.WriteLine Element.innerText & vbNewLine
            End If
        End If
        Next
        
        NewFile.WriteLine "</div>" & vbNewLine & "</body>" & vbNewLine & "</html>"

        NewFile.Close
        Set FSO = Nothing
        
        On Error GoTo 0
        
        OutSet.Update
        Set ie = Nothing    'close down IE and reset status bar
        Set MainBox = Nothing
        InSet.MoveNext  'Move to the next record. Don't ever forget to do this.
    Loop
Else
    MsgBox "Tabulka se seznamem restaurací ."
End If

'MsgBox "Dokonèeno. Vygenerován log s tagem "

OutSet.Close 'Close the recordset
Set OutSet = Nothing 'Clean up

InSet.Close 'Close the recordset
Set InSet = Nothing 'Clean up

End Sub

Sub ReadCards()
    On Error Resume Next
    Dim ie As InternetExplorer  'to refer to the running copy of Internet Explorer
    Dim html As HTMLDocument    'to refer to the HTML document returned
    Dim MainBox As IHTMLElement
    Dim Elements As IHTMLElementCollection
    Dim Element As IHTMLElement
    Dim FSO As FileSystemObject
    Dim KartyFile As Object   'použito pro zápis souborù html
    Dim PassedText As String
    
    Set KartyFile = FSO.CreateTextFile("c:\_Run\Script\Reader\karty\index.html", True)
    Set KartyFile = FSO.CreateTextFile(CurrentProject.Path & "\karty\index.html")
    
    Set ie = New InternetExplorer   'open Internet Explorer in memory, and go to website
                ie.Visible = False
        ie.navigate "http://hifis/karty/index2.php"
    
    Do While ie.ReadyState <> READYSTATE_COMPLETE   'Wait until IE is done loading page´

        DoEvents
    Loop
        
    Set html = ie.Document
    Set MainBox = html.getElementsByName("TABLE")
           
    PassedText = MainBox.innerHTML  '.documentElement.innerHTML
      
    KartyFile.WriteLine "<html>" & vbNewLine & "<head>"
    KartyFile.WriteLine PassedText
    KartyFile.WriteLine "</div>" & vbNewLine & "</body>" & vbNewLine & "</html>"

    KartyFile.Close
    Set FSO = Nothing
    Set ie = Nothing    'close down IE and reset status bar
    Set MainBox = Nothing
    
    
End Sub

Sub ReadCards2()

    Dim myHTMLString As String

        Dim myDoc As HTMLDocument
        Dim myTables As IHTMLElementCollection
        Dim myTable As IHTMLElement

        Dim myAllTags As IHTMLElementCollection
        Dim myHTMLTag As IHTMLElement

        myHTMLString = "http://hifis/karty/index2.php"
        WebBrowser1.DocumentText = myHTMLString

        myDoc = WebBrowser1.Document.OpenNew(True)
        myDoc.Write (myHTMLString)

        myTables = myDoc.getElementsByTagName("table")
        myTable = myTables.Item(0)

        For Each HtmlElement In myTable.Children
            child.outerText = child.innerText
        Next

        myAllTags = myDoc.getElementsByTagName("html")
        myHTMLTag = myAllTags.Item(0)

        'WriteAllText("C:\Users\Geoffrey Van Wyk\Desktop\myPage2.txt", myHTMLTag.OuterHtml)

End Sub

Sub Ping()
Dim strComputer As String
    strComputer = "192.168.0.8"
If Not CheckMachines(strComputer) Then
    MsgBox "This computer is currently unreachable: " & strComputer, vbOKOnly, "Computer Status"
    '....your logic
Else
    '...your logic
    MsgBox "This computer is Online!", vbOKOnly, "Computer Status"
End If
End Sub

Sub RunPS()
pscommand = " get-service | Foreach-Object { $_.Name } "
pscommand = "C:\Users\jav\Documents\Patalie\Projekty\ELSO\Programming\Bash_WIN\PowerScript\Get-CP_Name.ps1"
cmd = "powershell.exe -noprofile -executionpolicy bypass -file " & pscommand

Set SO = CreateObject("WScript.Shell")
Set executor = SO.Exec(cmd)
executor.StdIn.Close
MsgBox executor.StdOut.ReadAll
End Sub

Sub myWebTest()
' Tools / References / Microsoft XML, v 6.0
    On Error Resume Next
    Set File = CreateObject("Msxml2.XMLHTTP")
    Dim FSO As FileSystemObject
    Dim NewFile As Object   'použito pro zápis souborù html

    File.setTimeout 2000, 2000, 2000, 2000
    File.Open "GET", "http://www.starakotelna.cz/denni-menu", False
    'File.Open "GET", "http://www.microsoft.com/en-au/default.aspx:80", False
    'This is IE 8 headers
    File.setRequestHeader "User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET4.0C; .NET4.0E; BCD2000; BCD2000)"
    File.send
    
    Set FSO = New FileSystemObject
    Set NewFile = FSO.GetFile(CurrentProject.Path & "\trp.htm")
        
    If Err.Number = 0 Then
        Set NewFile = FSO.OpenTextFile(CurrentProject.Path & "\trp.htm")
    Else
        Set NewFile = FSO.CreateTextFile(CurrentProject.Path & "\trp.htm")
    End If
    NewFile.WriteLine File.responseText
    NewFile.Close
    Set FSO = Nothing
    
    On Error GoTo 0

    Set dom = CreateObject("Msxml2.DOMDocument")
    'Dim dom As New DOMDocument60
    dom.loadXML File.responseText
    MsgBox File.responseText
    'MsgBox dom.childNodes.length
End Sub

Sub ReadKarty()

' Tools / References / Microsoft HTML Object Library - Getting at parts of an HTML page
' Tools / References / Microsoft Internet Controls - Getting at Internet Explorer in VBA
    On Error Resume Next
    Dim ie As InternetExplorer  'to refer to the running copy of Internet Explorer
    Dim html As HTMLDocument    'to refer to the HTML document returned
    Dim MainBox As IHTMLElement
    Dim Elements As IHTMLElementCollection
    Dim Element As IHTMLElement
    
    Dim Final As String
  
    Dim FSO As FileSystemObject
    Dim NewFile As Object   'použito pro zápis souborù html
    Dim PassedText As String
    Dim RegExp As Object    'MS vbscript regular expressions - tools/references
    Set RegExp = CreateObject("vbscript.regexp")
'READYSTATE_UNINITIALIZED = 0, READYSTATE_LOADING = 1, READYSTATE_LOADED = 2, READYSTATE_INTERACTIVE = 3, READYSTATE_COMPLETE = 4

    On Error Resume Next
    Set ie = New InternetExplorer   'open Internet Explorer in memory, and go to website
    ie.Visible = False
    ie.navigate "http://localhost:8080/Karty_src.htm"
    Do While ie.ReadyState <> READYSTATE_COMPLETE   'Wait until IE is done loading page´
        DoEvents
    Loop

    Set html = ie.Document  'show text of HTML document returned
    Set MainBox = html
    Final = MainBox.innerText
    
    Set FSO = New FileSystemObject
    Set NewFile = FSO.GetFile(CurrentProject.Path & "\index.htm")
        
    If Len(Dir(CurrentProject.Path & "\index.htm")) <> 0 Then
        Kill (CurrentProject.Path & "\index.htm")
        Set NewFile = FSO.CreateTextFile(CurrentProject.Path & "jidelak\index.htm")
    Else
        Set NewFile = FSO.CreateTextFile(CurrentProject.Path & "jidelak\index.htm")
    End If
        
    NewFile.WriteLine "<!DOCTYPE html>" & vbNewLine & "<html>" & vbNewLine & "<head>" & vbNewLine & "<meta charset=" & Chr(34) & "windows-1250" & Chr(34) & ">" & vbNewLine & "<title>XXX</title>" & vbNewLine
    NewFile.WriteLine "<link rel=" & Chr(34) & "stylesheet" & Chr(34) & " type=" & Chr(34) & "text/css" & Chr(34) & " href=" & Chr(34) & "style.css" & Chr(34) & ">" & vbNewLine & "</head>" & vbNewLine & "<body>" & vbNewLine
    NewFile.WriteLine "<div id=" & Chr(34) & "Box" & Chr(34) & " class=" & Chr(34) & InSet!Shortcut & Chr(34) & ">" & vbNewLine
        
    Set Elements = MainBox.Children
    For Each Element In Elements
        If Len(Element.toString) > 10 Then
            With RegExp
                .Global = True
                .IgnoreCase = True
                .Multiline = True
                .Pattern = "style=" & Chr(34) & ".*?" & Chr(34)
            End With    'load regular expressions into variable
            PassedText = RegExp.Replace(Element.innerHTML, vbNullString)    'clear all style definitions from Box
        End If
    Next
        
    NewFile.WriteLine "</div>" & vbNewLine & "</body>" & vbNewLine & "</html>"

    NewFile.Close
    Set FSO = Nothing
        
    On Error GoTo 0
        
    Set ie = Nothing    'close down IE and reset status bar
    Set MainBox = Nothing
    
'MsgBox "Dokonèeno. Vygenerován log s tagem "

End Sub



Sub CreateLog()

Dim InSet As DAO.Recordset
Set InSet = CurrentDb.OpenRecordset("Devices")  'otevøít tab Devices pro pøeètení seznamu

Dim OutSet As DAO.Recordset
Set OutSet = CurrentDb.OpenRecordset("Log")  'otevøít tab Log pro záznam pøístupù
'''''''''''''''''''' volitelná souèást - metoda Addnew vždy pøidá na konec
If OutSet.RecordCount <> 0 Then 'kontrola zda  vstupní tab obsahuje data
    OutSet.MoveLast     'posun na poslední zánam v seznamu pøístupù - pøíprava na append
End If
'''''''''''''''''''' konec volitelné souèásti

Dim Network As WshNetwork   'windows script host - tools/references
Set Network = New WshNetwork    'použito pro názvy uživatele/domény

If Not (InSet.EOF And InSet.BOF) Then 'kontrola zda  vstupní tab obsahuje data
    InSet.MoveFirst 'posun na první øádek - pro jistotu
    Do Until InSet.EOF = True
        'spustit procedury s pøíslušnými parametry
        OutSet.AddNew
        OutSet!Connection = InSet!IPAddress 'OutSet("VendorYN") = True 'jiny zpusob odkazu na pole
        OutSet!LogDate = Now()
        OutSet!User = Network.UserName   'UserNameWin()
        OutSet!Domain = Network.UserDomain
        OutSet!CPName = InSet!MachineName
        If CheckMachines(InSet!MachineName) Then
            OutSet!Ping = True
        End If
        OutSet.Update
        InSet.MoveNext  'Move to the next record. Don't ever forget to do this.
    Loop
Else
    MsgBox "Tabulka se seznamem výpoèetek je prázdná."
End If

MsgBox "Dokonèeno. Vygenerován log s tagem "

OutSet.Close 'Close the recordset
Set OutSet = Nothing 'Clean up

InSet.Close 'Close the recordset
Set InSet = Nothing 'Clean up
Dim SQL_Text As String
eSQL = "SELECT Log.* FROM Log;"
DoCmd.RunSQL (eSQL)
End Sub

'Determine if device is online
Function CheckMachines(ByVal ComputerName As String)
Dim oShell, oExec As Variant
Dim strText, strCmd As String
strText = ""
strCmd = "ping -n 1 -w 1000 " & ComputerName
Set oShell = CreateObject("WScript.Shell")
Set oExec = oShell.Exec(strCmd)
Do While Not oExec.StdOut.AtEndOfStream
strText = oExec.StdOut.ReadLine()
If InStr(strText, "Reply") > 0 Then
CheckMachines = True
Exit Do
End If
Loop
End Function

Function SystemOnline(ByVal ComputerName As String)
' This function returns True if the specified host could be pinged.
' HostName can be a computer name or IP address.
' The Win32_PingStatus class used in this function requires Windows XP or later.
' Standard housekeeping
Dim colPingResults As Variant
Dim oPingResult As Variant
Dim strQuery As String
' Define the WMI query
strQuery = "SELECT * FROM Win32_PingStatus WHERE Address = '" & ComputerName & "'"
' Run the WMI query
Set colPingResults = GetObject("winmgmts://./root/cimv2").ExecQuery(strQuery)
' Translate the query results to either True or False
For Each oPingResult In colPingResults
If Not IsObject(oPingResult) Then
SystemOnline = False
ElseIf oPingResult.StatusCode = 0 Then
SystemOnline = True
Else
SystemOnline = False
End If
Next
End Function

Function UserNameWin() As String
     UserName = Environ("USERNAME") 'http://stackoverflow.com/questions/677112/how-to-get-logged-in-users-name-in-access-vba
End Function
