@echo off
SET log_file=%~dp0Multimedia\logfile.log


IF /I '%1%'=='h' GOTO HANA
IF /I '%1%'=='s' GOTO SQLite

GOTO MENU

:MENU
echo h - HANA 
echo s - SQLite
GOTO QUIT


:HANA
SET py_file="C:\Program Files\sap\hdbclient\hdbalm.py"
python %py_file%
GOTO MENU


SET mlt_dir='C:\_Run\Web'
SET py_file=%~dp0System\OS74.py

REM echo '-b', help='browse dir', type=str, default='')
REM echo '-l', help='list dir', type=str, default='')
REM echo '-f', help='file output', type=str, default='')
echo python %py_file% -b %mlt_dir% -f %log_file%
python %py_file% -b %mlt_dir% -f %log_file%

REM echo pure DOS version
REM dir /s/b *.mp3 > dir.txt

:SQLite
SET py_file=%~dp0System\SO74DB.py

:QUIT
REM EXIT