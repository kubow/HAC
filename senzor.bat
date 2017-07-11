@echo off
REM SET py_data_file=%~dp0System\Device\DataRead.py
SET py_data_file=%~dp0System\DV72.py
python %py_data_file% -d X86 -s luxo -l %~dp0Multimedia