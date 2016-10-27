Option Explicit
'Created by Jakub Vajda on 9.11.2013 - use to get relative structure of folder'
Dim fs: Set fs = CreateObject("Scripting.FileSystemObject")
Dim cf: cf = fs.GetAbsolutePathName(".") 'CurrentFolder
Dim of: Set of = fs.GetFolder(cf) 'ObjectFolder
Dim s: s = of & "\ListOfFiles.htm" 'OutputFileName
Dim ff: Set ff = fs.CreateTextFile(s, True) 'FolderFile
Dim fc: Set fc = of.Files 'FileCount
ff.Write "<HTML>" & vbCrLf & "<HEAD>" & vbCrLf & "<META HTTP-EQUIV=""Content-Type"" CONTENT=""text/html; charset=windows-1250"">" & vbCrLf
ff.Write "<TITLE>Directory Listing on " & cf & "</TITLE>" & vbCrLf & "<STYLE TYPE=""text/css"">" & vbCrLf & "<!--" & vbCrLf
ff.Write "BODY{background:""white"";}" & vbCrLf & "a:link {color:#FFFF00;}" & vbCrLf & "a:visited {color:#F3D900;}" & vbCrLf & "a:hover {color:#00FF00;}" & vbCrLf & "a:active {color:#FFFF00;}" & vbCrLf
ff.Write ".Head{background-color:#404040;color:#ffffff;border:1px solid #000000;text-align:center;font-size:8pt;font-family:""MS Sans Serif"";font-style:normal;font-weight:normal;}" & vbCrLf
ff.Write ".File{background-color:#e8e8ff;color:#080000;border:1px solid #000000;font-size:8pt;font-family:""MS Sans Serif"";font-style:normal;font-weight:normal;}" & vbCrLf
ff.Write ".Fldr{background-color:#404080;color:#ffffff;border:1px solid #000000;font-size:8pt;font-family:""MS Sans Serif"";font-style:normal;font-weight:normal;}-->" & vbCrLf
ff.Write "</STYLE>" & vbCrLf & "</HEAD>" & vbCrLf & "<BODY>" & vbCrLf
Dim nf: Set nf = of.Files
Dim ns: Set ns = of.Subfolders
ff.Write "<table><tr class=""Head""><td>FileFolder List Generated on " & Now & " / Total Folder Size - " & FormatNumber(of.Size/1000000) & "Mb / " & ns.Count & " Subfolders / " & nf.Count & " Files in Main Directory</td></tr>" & vbCrLf
ff.Write "<tr class=""Fldr""><td>Root - " & of.Path & "</td><td>" & FormatNumber(of.Size/1000) &" kb</td></tr>" & vbCrLf
Dim objFile
For Each objFile in fc
    ff.Write "<tr class=""File""><td>" & objFile.Name & "</td><td>" & Round(objFile.Size/1000,1) & " kb</td></tr>" & vbCrLf
Next
ShowSubfolders fs.GetFolder(cf)
Dim Subfolder
Sub ShowSubFolders(Folder)
    For Each Subfolder in Folder.SubFolders
        Set of = fs.GetFolder(Subfolder.Path)
        s = Len(cf)
        ff.Write "<tr class=""Fldr""><td>Root\<a href=""" & Replace(Mid(Subfolder.Path,s+2),"/","\") & """>" & Mid(Subfolder.Path,s+2) & "\" & "</a><td>" & FormatNumber(of.Size/1000) &" kb" & "</td></tr>"& vbCrLf
        Set fc = of.Files
        For Each objFile in fc
            ff.Write "<tr class=""File""><td>" & objFile.Name & "</td><td>" & Round(objFile.Size/1000,1) & " kb</td></tr>" & vbCrLf
        Next
        ShowSubFolders Subfolder
    Next
End Sub
ff.Write "</table>" & vbCrLf & "</BODY>" & vbCrLf & "</HTML>"
ff.Close
MsgBox "FolderList generated in" & vbCrLf & cf & vbCrLf & "directory. File ListOfFiles.htm"
Set ff = Nothing
Set of = Nothing
Set fs = Nothing