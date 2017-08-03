@echo off
Set mainHTML=%~dp0index.html
SET mlt_dir=%~dp0Multimedia\
Set subHTML1=%mlt_dir%showing1.htm
Set subHTML2=%mlt_dir%showing2.htm
Set subHTML3=%mlt_dir%showing3.htm
rem need to log vbs script outputs
rem wscript %~dp0System\Reader\ReaderMenu.vbs
python %~dp0System\SO74.py -g restaurant -w %~dp0 -l %mlt_dir%logfile.log
rem echo ^<html^> > %mainHTML%
rem echo ^<head^> >> %mainHTML%
rem echo ^<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" /^> >> %mainHTML%
rem echo ^<meta http-equiv="refresh" content="3;url=%subHTML1%" /^> >> %mainHTML%
rem echo ^<title^>Jidelni_listek^</title^> >> %mainHTML%
rem echo ^<link rel="stylesheet" type="text/css" href="Structure/style.css"^> >> %mainHTML%
rem echo ^</head^> >> %mainHTML%
rem echo ^<body^> >> %mainHTML%
type %~dp0Structure\HTML_Base_Head.txt > %mainHTML%
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
