@ECHO off
SET log_file=%~dp0Multimedia\logfile.log
SET py_file=%~dp0System\SO74.py
SET mode_name=compare
IF /I '%1%'=='b' GOTO database
IF /I '%1%'=='d' GOTO dir_file
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
SET extra_name=database
in_object=%2
out_object=%3
GOTO execute_py

:dir_file
SET extra_name=directory
in_object=%2
out_object=%3
GOTO execute_py

:text
SET extra_name=text
in_object=%2
out_object=%3
GOTO execute_py

:execute_py
ECHO python %py_file% -m %mode_name% -i %in_object% -o %out_object% -e %extra_name% -l logfile
python %py_file% -m %mode_name% -i %in_object% -o %out_object% -e %extra_name% -l %log_file%
GOTO quit

:quit
REM EXIT
