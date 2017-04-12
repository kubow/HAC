@ECHO off
cls
SET YY=%Date:~10,4%
SET MM=%Date:~4,2%
SET mainHTML=%~dp0index.html
SET data_db=%~dp0Multimedia\Measured\
SET settings_db=%~dp0System\Device\settings.db
SET py_data_file=%~dp0System\Device\DataWrite.py
SET py_forecast_file=%~dp0System\DataWeather.py
SET sqlite=C:\_Run\App\Database\SQLite\
ECHO ============================================
ECHO getting location in format ('city','country')
ECHO ============================================
SET command=%sqlite%sqlite3.exe %settings_db% "select * from place_active"
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
SET command=%sqlite%sqlite3.exe %settings_db%  "select devicename from device_active;"
FOR /F "tokens=* USEBACKQ" %%F IN (`%command%`) DO (
REM ECHO %%F
SET platform=%%F
)
ECHO syntax: %py_data_file% -d %platform% -l location
REM ECHO writing to: %data_db%%YY%%MM%.sqlite 
ECHO ...............
python %py_data_file% -d %platform% -l %data_db%
