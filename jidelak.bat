@echo off
Set mainHTML=%~dp0index.html
SET mlt_dir=%~dp0Multimedia\
SET py_file=%~dp0System\SO74.py

del "%~dp0Multimedia\RestMenu\*.*?"
rem wscript %~dp0System\Reader\ReaderMenu.vbs --not properly set...
python %py_file% -g restaurant -w %~dp0 -l %mlt_dir%logfile.log

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
