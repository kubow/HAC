Const NETHOOD = &H13&

Set objWSHShell = CreateObject("Wscript.Shell")
Set objShell = CreateObject("Shell.Application")

Set objFolder = objShell.Namespace(NETHOOD)
Set objFolderItem = objFolder.Self
strNetHood = objFolderItem.Path

'------------------------------------------------------------------------------------------

networkAddress = "\\192.168.6.20\"

strShortcutName = "Documents"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "Documents"
objShortcut.Save

strShortcutName = "Install"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "Install"
objShortcut.Save


strShortcutName = "Office"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "Office"
objShortcut.Save

strShortcutName = "PS"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "PS"
objShortcut.Save

strShortcutName = "Software"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "Software"
objShortcut.Save

strShortcutName = "Temp"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "Temp"
objShortcut.Save

'------------------------------------------------------------------------------------------

networkAddress = "\\192.168.6.18\"

strShortcutName = "VMWare"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "sybshare\vmw"
objShortcut.Save

strShortcutName = "Sybinst"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "sybshare\sybinst"
objShortcut.Save

strShortcutName = "Education"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "sybshare\Education"
objShortcut.Save

strShortcutName = "Public"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = networkAddress & "public"
objShortcut.Save

Public Function MapNetworkLocation(sName, oLnk)
	strShortcutName = sName
	Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
	objShortcut.TargetPath = networkAddress & sName
	objShortcut.Save
End Function