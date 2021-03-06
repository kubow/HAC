@echo off

Set presDir=%~dp0Multimedia\
Set tempDir=%~dp0Structure\
Set sysDir=%~dp0System\
Set mainHTML=%~dp0index.html
Set subHTML=%presDir%presenting.html

python %sysDir%log.py -l %presDir%logfile.log -t "Image presentation" -m Presenter
echo ^<html^> > %mainHTML%
echo ^<head^> >> %mainHTML%
echo ^<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" /^> >> %mainHTML%
echo ^<title^>Prezentace^</title^> >> %mainHTML%
echo ^<link rel="stylesheet" type="text/css" href="%tempName%/style.css"^> >> %mainHTML%
echo ^</head^> >> %mainHTML%
echo ^<body^> >> %mainHTML%
echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %mainHTML%
rem echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %mainHTML%
type  %presDir%text_horni_lista.txt >> %mainHTML%
echo ^</marquee^>^</div^> >> %mainHTML%
echo ^<div id="frame"^>^<iframe src="Multimedia/presenting.html" width="100%%" height="100%%"^>^</iframe^>^</div^> >> %mainHTML%
echo ^</body^> >> %mainHTML%
echo ^</html^> >> %mainHTML%
rem http://stackoverflow.com/questions/5642021/batch-process-all-files-in-directory
type %tempDir%HTML_Presenter_head.txt > %subHTML%
for %%F in (%presDir%image\*.jpg) do (
    echo %presDir%image\%%~nxF
    echo ^<li^> >> %subHTML%
    echo ^<span class="Centerer"^>^</span^> >> %subHTML%
    echo ^<img class="Centered" src="image\%%~nxF" alt="X"/^> >> %subHTML%
    echo ^</li^> >> %subHTML%   
)
type %tempDir%HTML_Presenter_tail.txt >> %subHTML%