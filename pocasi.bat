@echo off

SET YY=%Date:~10,4%
SET MM=%Date:~4,2%
SET mainHTML=%~dp0index.html
SET data_db=%~dp0Multimedia\Weather\
SET settings_db=%~dp0System\Device\settings.db
SET py_data_file=%~dp0System\Device\DataWrite.py
SET py_forecast_file=%~dp0System\Data\Weather\WriteWeatherActual.py

SET sqlite=C:\_Run\App\Textoviny\SQL\SQLite\

REM echo location = 'city,country'
SET /P result= < %sqlite%sqlite3.exe %settings_db% "select * from place_active" 
echo %result%
FOR /F %%a in (%result%) do SET loc=%%a
FOR /F %%a in (%result%) do SET cnt=%%b
SET location=%loc%,%cnt%
echo %location%

REM echo python read forecast
REM echo ====================
REM echo syntax: py_forecast_file file_to_write location
echo %py_forecast_file%
REM python %py_forecast_file% %mainHTML% %location%

REM echo python read forecast
REM echo ====================
echo %data_db%%YY%%MM%.sqlite 
python %py_data_file% -d %data_db%%YY%%MM%.sqlite 
