echo on
Set index=%~dp0iisstart.htm
wscript %~dp0Reader\ReaderMenu.vbs
echo ^<html^> > %index%
echo ^<head^> >> %index%
echo ^<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" /^> >> %index%
echo ^<title^>Jidelni_listek^</title^> >> %index%
echo ^<link rel="stylesheet" type="text/css" href="Reader/style.css"^> >> %index%
echo ^</head^> >> %index%
echo ^<body^> >> %index%
echo ^<div id="frame"^>^<iframe src="Reader/jidelak/jidlo1.htm" width="100%%" height="100%%"^>^</iframe^>^</div^> >> %index%
echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %index%
rem echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %index%
type %~dp0Presenter\text.txt >> %index%
echo ^</marquee^>^</div^> >> %index%
echo ^</body^> >> %index%
echo ^</html^> >> %index%
