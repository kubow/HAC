@echo off
SET sqlite=C:\_Run\App\Database\SQLite\sqlite3.exe

SET log_dir=%~dp0Multimedia\
SET data_dir=%log_dir%Measured\
SET py_data_file=%~dp0System\DV72.py

ECHO ==========================
ECHO sqlite setup platform
ECHO ==========================

SET command=%sqlite% %device_dir%settings.db  "select devicename from device_active;"
FOR /F "tokens=* USEBACKQ" %%F IN (`%command%`) DO (
ECHO platform: %%F
SET platform=%%F
)

ECHO ==========================
ECHO serial read data
ECHO ==========================
ECHO syntax: %py_data_file% -d %platform% -l location -m mode(rea/agg)
ECHO writing to: %data_dir%%YY%%MM%.sqlite 
ECHO ...............
REM python %py_data_file% -d %platform% -l %data_dir% >> %log_dir%logfile.log
python %py_data_file% -d "%platform%" -l %data_dir% -m read
