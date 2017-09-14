@echo off
REM SET sqlite=C:\_Run\App\Database\SQLite\sqlite3.exe

SET log_dir=%~dp0Multimedia\
SET script_dir=%~dp0System\
SET py_data_file=%script_dir%DV72.py

ECHO ==========================
ECHO serial read data
ECHO ==========================
ECHO syntax: %py_data_file% -d %platform% -l %log_dir% -m mode(read/aggregate)
python %py_data_file% -d "%platform%" -l %log_dir% -m read
