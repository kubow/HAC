@ECHO off
cls
SET YY=%Date:~10,4%
SET MM=%Date:~4,2%
SET mainHTML=%~dp0index.html
SET data_db=%~dp0Multimedia\Measured\
SET settings_db=%~dp0System\Device\settings.db
SET py_data_file=%~dp0System\Device\DataWrite.py
SET py_forecast_file=%~dp0System\Data\Weather\WriteWeatherActual.py
SET sqlite=C:\_Run\App\Textoviny\SQL\SQLite\
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
ECHO python read weather actual
ECHO ==========================
ECHO syntax: %py_data_file% -d database.sqlite -p device.name
ECHO writing to: %data_db%%YY%%MM%.sqlite 
python %py_data_file% -d %data_db%%YY%%MM%.sqlite -p RPi
