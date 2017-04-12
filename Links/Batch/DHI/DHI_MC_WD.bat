@echo off
cls
SET MC_PATH1=C:\Program Files (x86)\DHI\MIKE CUSTOMISED\Platform\
SET MC_PATH2=C:\_Temp\QGC\
SET MC_PATH3=C:\_Run\App\Mapoaplikace\EPANET\UWOP_R2.1\
echo.
echo  Program directory 1 %MC_PATH1%
echo  Program directory 2 %MC_PATH2%
echo  Program directory 3 %MC_PATH3%
echo.
echo - - - - MIKE CUSTOMIZED in %MC_PATH1% - - - -
echo.
echo  1 ) - MC Shell 64-bit 
echo  2 ) - MC Shell 32-bit
echo  3 ) - MC Database Manager Utility - 64-bit
echo  4 ) - MC Database Manager Utility - 32-bit
echo.
echo - - - - MIKE CUSTOMIZED in %MC_PATH2% - (for netowrk use) -
echo.
echo  5 ) - MC Shell 64-bit 
echo  6 ) - MC Shell 32-bit 
echo.
echo - - - - MIKE CUSTOMIZED in %MC_PATH3% - (for local use) -
echo.
echo  7 ) - MC Shell 64-bit 
echo  8 ) - MC Shell 32-bit 
echo.
echo  9 ) - Exit this batch - - - - - - - 
echo.
choice /c:123456789 
if errorlevel 9 goto End
if errorlevel 8 goto MC_BU_32
if errorlevel 7 goto MC_BU_64
if errorlevel 6 goto MC_LF_32
if errorlevel 5 goto MC_LF_64
if errorlevel 4 goto MC_PF_DB_32
if errorlevel 3 goto MC_PF_DB_64
if errorlevel 2 goto MC_PF_32
if errorlevel 1 goto MC_PF_64

:MC_PF_64
echo Starting MIKE CUSTOMIZED Platform in %MC_PATH1% ...
cd %MC_PATH1%
start DHI.Solutions.Shell.exe
cd\
goto End

:MC_PF_32
echo Starting MIKE CUSTOMIZED Platform in %MC_PATH1% ...
cd %MC_PATH1%
start DHI.Solutions.Shell32.exe
cd\
goto End

:MC_PF_DB_64
echo Starting MIKE CUSTOMIZED Database utility in %MC_PATH1% ...
cd %MC_PATH1%
start DHI.Solutions.Shell.exe --app DHI.Solutions.DatabaseUtility
cd\
goto End

:MC_PF_DB_32
echo Starting MIKE CUSTOMIZED Database utility in %MC_PATH1% ...
cd %MC_PATH1%
start DHI.Solutions.Shell32.exe --app DHI.Solutions.DatabaseUtility
cd\
goto End 

:MC_LF_64
echo Starting MIKE CUSTOMIZED Platform in %MC_PATH2% ...
cd %MC_PATH2%
start DHI.Solutions.Shell.exe
cd\
goto End

:MC_LF_32
echo Starting MIKE CUSTOMIZED Platform in %MC_PATH2% ...
cd %MC_PATH2%
start DHI.Solutions.Shell32.exe
cd\
goto End

:MC_BU_64
echo Starting MIKE CUSTOMIZED Platform in %MC_PATH3% ...
cd %MC_PATH3%
start DHI.Solutions.Shell.exe
cd\
goto End

:MC_BU_32
echo Starting MIKE CUSTOMIZED Platform in %MC_PATH3% ...
cd %MC_PATH3%
start DHI.Solutions.Shell32.exe
cd\
goto End

:End
echo Quitting ....
rem pause