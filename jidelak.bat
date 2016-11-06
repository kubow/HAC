@echo off
Set iname=iisstart
Set index1=%~dp0%iname%.htm
Set index2=%~dp0%iname%1.htm
Set index3=%~dp0%iname%2.htm
wscript %~dp0Reader\ReaderMenu.vbs
echo ^<html^> > %index1%
echo ^<head^> >> %index1%
echo ^<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" /^> >> %index1%
echo ^<meta http-equiv="refresh" content="3;url=%index2%" /^> >> %index1%
echo ^<title^>Jidelni_listek^</title^> >> %index1%
echo ^<link rel="stylesheet" type="text/css" href="Reader/style.css"^> >> %index1%
echo ^</head^> >> %index1%
echo ^<body^> >> %index1%
echo ^<div id="frame"^>^<iframe src="Reader/jidelak/jidlo1.htm" width="100%%" height="100%%"^>^</iframe^>^</div^> >> %index1%
echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %index1%
rem echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %index1%
type %~dp0Presenter\text.txt >> %index1%
echo ^</marquee^>^</div^> >> %index1%
echo ^</body^> >> %index1%
echo ^</html^> >> %index1%
