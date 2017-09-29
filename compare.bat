@ECHO off
SET log_file=%~dp0Multimedia\logfile.log
IF /I '%1%'=='b' GOTO database
IF /I '%1%'=='d' GOTO directory
IF /I '%1%'=='t' GOTO text
GOTO menu

:menu
CLS
ECHO 1st argument - compare type
ECHO     b - dataBase
ECHO     d - Direcotry
ECHO     t - Text version
ECHO 2nd argument - source file/folder
ECHO 3rd argument - destination file/folder
GOTO quit

:database
SET py_file=%~dp0System\SO74DB.py
ECHO python %py_file% -m compare -a %2 -b %3 -f table_name -l logfile
python %py_file% -m compare -a %2 -b %3 -l %log_file%
GOTO quit

:directory
SET mlt_dir=%2
REM SET mlt_dir='C:\_Run\Web'
SET py_file=%~dp0System\OS74.py

REM echo '-b', help='browse dir', type=str, default='')
REM echo '-l', help='list dir', type=str, default='')
REM echo '-f', help='file output', type=str, default='')
ECHO python %py_file% -i %mlt_dir% -f %log_file% -m True
python %py_file% -i %mlt_dir% -f %log_file%

:text
ECHO pure DOS version
DIR /s/b *.mp3 > dir.txt

:quit
REM EXIT