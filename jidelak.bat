@ECHO off
SET mainHTML=%~dp0index.html
SET mlt_dir=%~dp0Multimedia\
SET py_file=%~dp0System\SO74.py

ECHO archiving ...
DEL "%mlt_dir%RestMenu\*.*?"
REM wscript %~dp0System\Convert\DataReaderWeb.vbs --not properly set...
python %py_file% -m restaurant -i %~dp0 -l %mlt_dir%logfile.log

TYPE %~dp0Structure\HTML_Base_Head.txt > %mainHTML%

ECHO ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %mainHTML%
TYPE %~dp0Multimedia\text_horni_lista.txt >> %mainHTML%
ECHO ^</marquee^>^</div^> >> %mainHTML%

ECHO ^<div id="west"^>0^</div^> >> %mainHTML%
ECHO ^<div id="east"^>0^</div^> >> %mainHTML%

ECHO ^<div id="frame"^> >> %mainHTML%
ECHO    ^<iframe id="Left" src="Multimedia/RestMenu/elb.html"^>^</iframe^> >> %mainHTML%
ECHO    ^<iframe id="Right" src="Multimedia/RestMenu/hus.html"^>^</iframe^> >> %mainHTML%
ECHO ^</div^> >> %mainHTML%

REM ECHO ^<button onclick="loadPages()"^>Click Me^</button^> >> %mainHTML%

ECHO ^<script^> >> %mainHTML%
ECHO    window.setInterval(function(){ >> %mainHTML%
ECHO    /// call your function here >> %mainHTML%
ECHO    /// var left = "Multimedia/RestMenu/zat.html"; >> %mainHTML%
ECHO    /// var right = "Multimedia/RestMenu/sad.html"; >> %mainHTML%

ECHO     var srcs = [ >> %mainHTML%
for %%F in (%~dp0Multimedia\RestMenu\*.htm) do (
    ECHO    , "Multimedia/RestMenu/%%~nxF"  >> %mainHTML%
)
ECHO    ] >> %mainHTML%

ECHO    document.getElementById('Left').setAttribute('src', srcs[Math.floor(Math.random() * srcs.length)); >> %mainHTML%
ECHO    document.getElementById('Right').setAttribute('src', srcs[Math.floor(Math.random() * srcs.length)); >> %mainHTML%
ECHO    // document.getElementById('Left').src += document.getElementById('Left').src; >> %mainHTML%
ECHO    // document.getElementById('Right').src += document.getElementById('Right').src; >> %mainHTML%
ECHO    document.getElementById('west').innerHTML = document.getElementById("Left").contentDocument.title; >> %mainHTML%
ECHO    document.getElementById('east').innerHTML = document.getElementById("Right").contentDocument.title; >> %mainHTML%
ECHO    }, 10000); >> %mainHTML%
ECHO ^</script^> >> %mainHTML%

REM ECHO ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %mainHTML%
ECHO ^</body^> >> %mainHTML%
ECHO ^</html^> >> %mainHTML%


REM     function randomFrom(array) {
REM        return array[Math.floor(Math.random() * array.length)];
REM    };