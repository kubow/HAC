@ECHO off
SET platform=JAV-PC
SET log_dir=%~dp0Multimedia\
SET log_file=%log_dir%logfile.log
SET system_dir=%~dp0System\
SET py_data_file=%system_dir%DV72.py
SET py_forecast_file=%system_dir%SO74.py
SET sqlite=C:\_Run\App\Database\SQLite\sqlite3.exe

IF /I '%1%'=='b' GOTO big
IF /I '%1%'=='s' GOTO small
GOTO menu

:menu
CLS
echo 1st argument - cycle type
echo     b - Big tick / weather + forecast + aggreagte data"
echo     s - Small tick / just aggregate data
GOTO quit

:big
ECHO ============================================
ECHO getting location in format ('city','country')
ECHO ============================================
SET command=%sqlite% %system_dir%Settings.sqlite "select * from place_active"
FOR /F "tokens=* USEBACKQ" %%F IN (`%command%`) DO (
REM ECHO %%F
SET result=%%F
)
ECHO got: "%result%" : %command%

ECHO ====================
ECHO python read forecast 
ECHO ====================
ECHO syntax: %py_forecast_file% -g weather -p location -w destination_to_write_results
rem SET location="Horni Pocernice, cz"
SET location="Zlin, cz"
python %py_forecast_file% -g weather -p %location% -w %~dp0 -l %log_file%

ECHO ====================
ECHO python aggregate data 
ECHO ====================
ECHO syntax: %py_data_file% -d %platform% -l location -m mode(rea/agg)
ECHO ...............
python %py_data_file% -m aggregate -d "%platform%" -l %log_dir%

:small
ECHO ====================
ECHO python aggregate data 
ECHO ====================
ECHO syntax: %py_data_file% -d %platform% -l location -m mode(rea/agg)
ECHO ...............
python %py_data_file% -m aggregate -d "%platform%" -l %log_dir%

:quit
REM EXIT