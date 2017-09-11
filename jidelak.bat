@echo off
Set mainHTML=%~dp0index.html
SET mlt_dir=%~dp0Multimedia\
SET py_file=%~dp0System\SO74.py

rem echo archiving 
del "%mlt_dir%RestMenu\*.*?"
rem wscript %~dp0System\Reader\ReaderMenu.vbs --not properly set...
python %py_file% -g restaurant -w %~dp0 -l %mlt_dir%logfile.log

type %~dp0Structure\HTML_Base_Head.txt > %mainHTML%

echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %mainHTML%
type %~dp0Multimedia\text_horni_lista.txt >> %mainHTML%
echo ^</marquee^>^</div^> >> %mainHTML%

echo ^<div id="west"^>0^</div^> >> %mainHTML%
echo ^<div id="east"^>0^</div^> >> %mainHTML%

echo ^<div id="frame"^> >> %mainHTML%
echo    ^<iframe id="Left" src="Multimedia/RestMenu/bla.html"^>^</iframe^> >> %mainHTML%
echo    ^<iframe id="Right" src="Multimedia/RestMenu/bla.html"^>^</iframe^> >> %mainHTML%
echo ^</div^> >> %mainHTML%

REM echo ^<button onclick="loadPages()"^>Click Me^</button^> >> %mainHTML%

echo ^<script^> >> %mainHTML%
echo    window.setInterval(function(){ >> %mainHTML%
echo    /// call your function here >> %mainHTML%
echo    /// var left = "Multimedia/RestMenu/zat.html"; >> %mainHTML%
echo    /// var right = "Multimedia/RestMenu/sad.html"; >> %mainHTML%

echo     var srcs = [ >> %mainHTML%
for %%F in (%~dp0Multimedia\RestMenu\*.htm) do (
    echo    , "Multimedia/RestMenu/%%~nxF"  >> %mainHTML%
)
echo    ] >> %mainHTML%

echo    document.getElementById('Left').setAttribute('src', srcs[Math.floor(Math.random() * srcs.length)); >> %mainHTML%
echo    document.getElementById('Right').setAttribute('src', srcs[Math.floor(Math.random() * srcs.length)); >> %mainHTML%
echo    // document.getElementById('Left').src += document.getElementById('Left').src; >> %mainHTML%
echo    // document.getElementById('Right').src += document.getElementById('Right').src; >> %mainHTML%
echo    document.getElementById('west').innerHTML = document.getElementById("Left").contentDocument.title; >> %mainHTML%
echo    document.getElementById('east').innerHTML = document.getElementById("Right").contentDocument.title; >> %mainHTML%
echo    }, 10000); >> %mainHTML%
echo ^</script^> >> %mainHTML%

rem echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %mainHTML%
echo ^</body^> >> %mainHTML%
echo ^</html^> >> %mainHTML%


REM     function randomFrom(array) {
REM        return array[Math.floor(Math.random() * array.length)];
REM    };