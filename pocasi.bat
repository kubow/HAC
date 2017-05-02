@ECHO off
cls
SET YY=%Date:~10,4%
SET MM=%Date:~4,2%
SET mainHTML=%~dp0index.html
SET log_dir=%~dp0Multimedia\
SET data_dir=%log_dir%Measured\
SET device_dir=%~dp0System\Device\
SET py_data_file=%device_dir%DataWrite.py
SET py_forecast_file=%~dp0System\DataWeather.py
SET py_log_file=%~dp0System\log.py
SET sqlite=C:\_Run\App\Database\SQLite\sqlite3.exe
ECHO ============================================
ECHO getting location in format ('city','country')
ECHO ============================================
SET command=%sqlite% %device_dir%settings.db "select * from place_active"
FOR /F "tokens=* USEBACKQ" %%F IN (`%command%`) DO (
REM ECHO %%F
SET result=%%F
)
ECHO got: "%result%" : %command%
ECHO ====================
ECHO python read forecast 
ECHO ====================
ECHO syntax: %py_forecast_file% file_to_write location (now disabled)
REM python %py_forecast_file% %mainHTML% %location%
ECHO ==========================
ECHO python write proccessed data
ECHO ==========================
SET command=%sqlite% %device_dir%settings.db  "select devicename from device_active;"
FOR /F "tokens=* USEBACKQ" %%F IN (`%command%`) DO (
REM ECHO %%F
SET platform=%%F
)
ECHO syntax: %py_data_file% -d %platform% -l location
REM ECHO writing to: %data_dir%%YY%%MM%.sqlite 
ECHO ...............
REM python %py_data_file% -d %platform% -l %data_dir% >> %log_dir%logfile.log
python %py_data_file% -d %platform% -l %data_dir%
python %py_log_file% -l %log_dir%logfile.log -m "weather" -t "weather read and data aggregated"