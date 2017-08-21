@echo off
cls
SET py_file=%~dp0System\SO74DB.py
echo python %py_file% -m compare -l %1 -r %2
python %py_file% -m compare -l %1 -r %2
pause