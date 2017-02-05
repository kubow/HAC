Const NETHOOD = &H13&

Set objWSHShell = CreateObject("Wscript.Shell")
Set objShell = CreateObject("Shell.Application")

strDesktopFolder=objWSHShell.SpecialFolders("Desktop") & "\"
Set objFolder = objShell.Namespace(NETHOOD)
Set objFolderItem = objFolder.Self
strNetHood = objFolderItem.Path

strShortcutName = "_work"
strShortcutPath = "\\czprg1-stor\_work"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save

strShortcutName = "Projects"
strShortcutPath = "\\czprg1-stor\Projects"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save

strShortcutName = "Scan2PDF"
strShortcutPath = "\\czprg1-stor\ScanToPDF"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save

strShortcutName = "Install"
strShortcutPath = "\\czprg1-stor\Projects\99320001\Install"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save

strShortcutName = "Education CZ-SOL"
strShortcutPath = "\\czprg1-stor.hif.cz\Projects\32019130"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save

strShortcutName = "Static Data"
strShortcutPath = "\\czprg1-stor.hif.cz\Projects\99320000"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save

strShortcutName = "Monitoring"
strShortcutPath = "\\czprg1-stor.hif.cz\Projects\32019632"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save

strShortcutName = "Templates"
strShortcutPath = "\\czprg1-stor.hif.cz\Projects\99320100"
Set objShortcut = objWSHShell.CreateShortcut(strNetHood & "\" & strShortcutName & ".lnk")
objShortcut.TargetPath = strShortcutPath
objShortcut.Save