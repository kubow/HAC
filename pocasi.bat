@ECHO off
cls
SET YY=%Date:~10,4%
SET MM=%Date:~4,2%
SET mainHTML=index.html
SET log_dir=%~dp0Multimedia\
SET data_dir=%log_dir%Measured\
SET system_dir=%~dp0System\
SET py_data_file=%system_dir%DV72.py
SET py_forecast_file=%system_dir%SO74.py
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
ECHO syntax: %py_forecast_file% -g weather -l location -w destination_to_write_results
SET location="Horni Pocernice, cz"
python %py_forecast_file% -g weather -l %location% -w %~dp0
ECHO ==========================
ECHO python write proccessed data
ECHO ==========================
SET command=%sqlite% %device_dir%settings.db  "select devicename from device_active;"
FOR /F "tokens=* USEBACKQ" %%F IN (`%command%`) DO (
REM ECHO %%F
SET platform=%%F
)
ECHO syntax: %py_data_file% -d %platform% -l location
ECHO writing to: %data_dir%%YY%%MM%.sqlite 
ECHO ...............
REM python %py_data_file% -d %platform% -l %data_dir% >> %log_dir%logfile.log
python %py_data_file% -d %platform% -l %data_dir%
REM python %py_log_file% -l %log_dir%logfile.log -m "weather" -t "weather read and data aggregated"