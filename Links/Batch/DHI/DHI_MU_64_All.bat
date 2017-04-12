@echo off
cls
rem echo Closing mu.exe
tskill 7120
taskkill /IM "MU.exe" /T /F > nul
rem /T = kills child process
rem /F = forceful termination of your process
if errorlevel 128 (  echo process MU.exe is not running - no need to close) 
rem echo Closing muiservermanager.exe
taskkill /IM "muiservermanager.exe" /T /F > nul
if errorlevel 128 (  echo process muiservermanager.exe is not running - no need to close
)
SET OF_PATH="C:\Program Files\Microsoft Office\OFFICE\MSACCESS.EXE"
IF EXIST "C:\Program Files (x86)\DHI\2014\bin" SET MU_PATH="C:\Program Files (x86)\DHI\2014\bin"
IF EXIST "C:\Program Files (x86)\DHI\2016\bin" SET MU_PATH="C:\Program Files (x86)\DHI\2016\bin"
SET MO_PATH=C:\_Model
echo.
echo  Program directory %MU_PATH%
echo  Model directory %MO_PATH%
echo.
echo - - - - MIKE URBAN with Licence Administration - - - -
echo.
echo  1 ) - Run Licence Administration and MU - Model.mup 
echo  2 ) - Run Licence Administration and MU - Model.mdb
echo.
echo - - - - MIKE URBAN directly open Model - - - -
echo.
echo  3 ) - Run MIKE URBAN - C:\_Model\Model.mup 
echo  4 ) - Run MIKE URBAN - C:\_Model\Model.mdb
echo.
echo - - - - just MIKE URBAN window - - - -
echo.
echo  5 ) - Open new
echo.
echo  6 ) - Exit this batch - - - - - - - 
echo.
choice /c:123456 
if errorlevel 6 goto End
if errorlevel 5 goto MU
if errorlevel 4 goto Mdb
if errorlevel 3 goto Mup
if errorlevel 2 goto LicMdb
if errorlevel 1 goto LicMup

:LicMup
call %MU_PATH%\LicSvcLocUI.exe
echo Starting MIKE URBAN %MO_PATH%\Model.mup ...
call %MU_PATH%\MU.exe %MO_PATH%\Model.mup 
echo spustil se LicAdmin a pak MUP Model
goto End

:LicMdb
call %MU_PATH%\LicSvcLocUI.exe"
echo Starting MIKE URBAN %MO_PATH%\Model.mdb ...
call %MU_PATH%\MU.exe %MO_PATH%\Model.mdb
echo spustil se LicAdmin a pak MDB Model
goto End

:Mup
echo Starting MIKE URBAN %MO_PATH%\Model.mup ...
call %MU_PATH%\MU.exe %MO_PATH%\Model.mup 
echo spustil se MUP Model
goto End

:Mdb
echo Starting MIKE URBAN %MO_PATH%\Model.mdb ...
call %MU_PATH%\MU.exe %MO_PATH%\Model.mdb 
echo spustil se MDB Model
goto End 

:MU
echo Starting MIKE URBAN window ...
call %MU_PATH%\MU.exe
echo spustilo se ciste okno MU
goto End

:End
echo vypnuti procesu na konci davky je vyple nebot to stejne nedojede na konec
rem compact and repair db
%OF_PATH% %MO_PATH%\Model.mdb /compact
echo Closing mu.exe
rem taskkill /f /im mu.exe > nul
echo Closing muiservermanager.exe
rem taskkill /f /im muiservermanager.exe > nul
rem pause