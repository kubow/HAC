@echo off
Set mainHTML=%~dp0index.html
Set settings_db=%~dp0System/Device/settings.db
Set py_rain_file=%~dp0System/Device/Rain.py
Set py_temp_file=%~dp0System/Device/Temperature.py
Set py_wind_file=%~dp0System/Device/Wind.py
Set py_forecast_file=%~dp0System/DataWeather/WriteWeatherActual.py

Set sqlite=C:\_Run\App\Textoviny\SQL\SQLite\

REM echo location setting
SET /P result= < %sqlite%sqlite3.exe %settings_db% "select * from place_active"
echo %result%
FOR /F %%a in (%result%) do set loc=%%a
FOR /F %%a in (%result%) do set cnt=%%b
SET location=%loc%,%cnt%
echo %location%

REM echo python generate htm's
echo %py_forecast_file%
REM python %py_forecast_file% %mainHTML%
REM python %py_forecast_file% %mainHTML% %location%