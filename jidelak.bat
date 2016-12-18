@echo off
Set mainHTML=%~dp0%index.html
Set subHTML1=%~dp0Multimedia\showing1.htm
Set subHTML2=%~dp0Multimedia\showing2.htm
Set subHTML3=%~dp0Multimedia\showing3.htm
rem need to log vbs script outputs
rem wscript %~dp0System\Reader\ReaderMenu.vbs
python %~dp0System\Reader\Reader.py
echo ^<html^> > %mainHTML%
echo ^<head^> >> %mainHTML%
echo ^<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" /^> >> %mainHTML%
echo ^<meta http-equiv="refresh" content="3;url=%subHTML1%" /^> >> %mainHTML%
echo ^<title^>Jidelni_listek^</title^> >> %mainHTML%
echo ^<link rel="stylesheet" type="text/css" href="Structure/style.css"^> >> %mainHTML%
echo ^</head^> >> %mainHTML%
echo ^<body^> >> %mainHTML%
for %%F in (%~dp0Multimedia\RestMenu\*.htm) do (
    echo process file %~dp0Multimedia\RestMenu\%%~nxF
)
echo ^<div id="frame"^>^<iframe src="Multimedia/showing1.htm" width="100%%" height="100%%"^>^</iframe^>^</div^> >> %mainHTML%
echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %mainHTML%
rem echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %mainHTML%
type %~dp0Multimedia\text_horni_lista.txt >> %mainHTML%
echo ^</marquee^>^</div^> >> %mainHTML%
echo ^</body^> >> %mainHTML%
echo ^</html^> >> %mainHTML%
