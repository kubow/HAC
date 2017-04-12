@echo off
SET WEST_PATH=C:\Users\Public\Documents\DHI\WEST
SET ARC_COM="C:\Program Files (x86)\Common Files\ArcGIS"
SET PY_PATH=C:\%PY_VER%\ArcGIS%ARC_VER%
rem cd %ARC_PATH%

rem decission between arcgis & arccatalog
echo  Program directory %ARC_PATH%
echo.
echo - - - - ArcGIS application ver %ARC_VER% - - - -
echo.
echo  1 ) - ArcMap 
echo  2 ) - ArcCatalog
echo  3 ) - ArcGlobe
echo  4 ) - ArcScene
echo  5 ) - License Administration 
echo.
echo - - - - Tools for ArcGIS (Python) -
echo.
echo  6 ) - IDLE GUI 
echo  7 ) - MXD Doctor 
echo.
echo  8 ) - Exit this batch - - - - - - - 
echo.
choice /c:12345678 
if errorlevel 8 goto End
if errorlevel 7 goto MX_DOC
if errorlevel 6 goto IDLE
if errorlevel 5 goto AR_LIC
if errorlevel 4 goto AR_SCN
if errorlevel 3 goto AR_GLO
if errorlevel 2 goto AR_CAT
if errorlevel 1 goto AR_MAP

:AR_MAP
echo ArcGIS application in %ARC_PATH% ...
call %ARC_PATH%\bin\ArcMap.exe
goto End

:AR_CAT
echo ArcCatalog application in %ARC_PATH% ...
call %ARC_PATH%\bin\ArcCatalog.exe
goto End

:AR_GLO
echo ArcGlobe application in %ARC_PATH% ...
call %ARC_PATH%\bin\ArcGlobe.exe
goto End

:AR_SCN
echo ArcScene application in %ARC_PATH% ...
call %ARC_PATH%\bin\ArcScene.exe
goto End

:AR_LIC
echo ArcGIS Licence Administration application ...
call %ARC_COM%\bin\ArcGISAdmin.exe
goto End

:IDLE
echo Python IDLE application in %PY_PATH% ...
call %PY_PATH%\pythonw.exe "%PY_PATH%\Lib\idlelib\idle.pyw"
goto End

:MX_DOC
echo MXD Doctor application in %ARC_PATH% ...
call %ARC_PATH%\Tools\MXDDoctor.exe
goto End

:End
echo Quitting ....
rem pause
exit

