@echo off
Set mainHTML=%~dp0index.html
SET mlt_dir=%~dp0Multimedia\
SET py_file=%~dp0System\SO74.py

del "%mlt_dir%RestMenu\*.*?"
rem wscript %~dp0System\Reader\ReaderMenu.vbs --not properly set...
python %py_file% -g restaurant -w %~dp0 -l %mlt_dir%logfile.log

type %~dp0Structure\HTML_Base_Head.txt > %mainHTML%

echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %mainHTML%
type %~dp0Multimedia\text_horni_lista.txt >> %mainHTML%
echo ^</marquee^>^</div^> >> %mainHTML%

echo ^<div id="frame"^>^<iframe id="Left" src="Multimedia/RestMenu/bla.html" width="49%%" height="100%%"^>^</iframe^> >> %mainHTML%
echo    ^<iframe id="Right" src="Multimedia/RestMenu/bla.html" width="49%%" height="100%%"^>^</iframe^> >> %mainHTML%
echo ^</div^> >> %mainHTML%

echo ^<button onclick="loadPages()"^>Click Me^</button^> >> %mainHTML%
echo ^<script^> >> %mainHTML%
echo    function loadPages(){ >> %mainHTML%
echo        var left = "Multimedia/RestMenu/zat.html"; >> %mainHTML%
echo        var right = "Multimedia/RestMenu/sad.html"; >> %mainHTML%

REM for %%F in (%~dp0Multimedia\RestMenu\*.htm) do (
REM     echo process file %~dp0Multimedia\RestMenu\%%~nxF
REM )

echo        document.getElementById('Left').setAttribute('src', left); >> %mainHTML%
echo        document.getElementById('Right').setAttribute('src', right); >> %mainHTML%
echo     } >> %mainHTML%
echo ^</script^> >> %mainHTML%

rem echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %mainHTML%
echo ^</body^> >> %mainHTML%
echo ^</html^> >> %mainHTML%
