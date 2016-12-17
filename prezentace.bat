echo on
Set index=%~dp0iisstart.htm
Set HTMLChange=%~dp0Multimedia\presenting.html
echo ^<html^> > %index%
echo ^<head^> >> %index%
echo ^<meta http-equiv="Content-Type" content="text/html; charset=windows-1250" /^> >> %index%
echo ^<title^>Prezentace^</title^> >> %index%
echo ^<link rel="stylesheet" type="text/css" href="Reader/style.css"^> >> %index%
echo ^</head^> >> %index%
echo ^<body^> >> %index%
echo ^<div id="frame"^>^<iframe src="Presenter/index.html" width="100%%" height="100%%"^>^</iframe^>^</div^> >> %index%
echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100"^> >> %index%
rem echo ^<div id="top"^>^<marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3"^> >> %index%
type  %~dp0Multimedia\text_horni_lista.txt >> %index%
echo ^</marquee^>^</div^> >> %index%
echo ^</body^> >> %index%
echo ^</html^> >> %index%
rem http://stackoverflow.com/questions/5642021/batch-process-all-files-in-directory
type %~dp0Presenter\HTML_head.txt > %HTMLChange%
for %%F in (%~dp0\Multimedia\image\*.jpg) do (
   echo ^<li^> >> %HTMLChange%
   echo ^<span class="Centerer"^>^</span^> >> %HTMLChange%
   echo ^<img class="Centered" src="image\%%~nxF" alt="X"/^> >> %HTMLChange%
   echo ^</li^> >> %HTMLChange%   
)
type %~dp0Presenter\HTML_tail.txt >> %HTMLChange%