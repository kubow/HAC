@ECHO off
SET log_file=%~dp0Multimedia\logfile.log
SET py_file=%~dp0System\UI74KW.py
IF /I '%1%'=='a' GOTO kivy
IF /I '%1%'=='b' GOTO inspector
IF /I '%1%'=='t' GOTO text
GOTO menu

:menu
CLS
ECHO 1st argument - compare type
ECHO     a - Normal run
ECHO     b - Debug
ECHO     t - Text version (not implemented)
GOTO quit

:kivy

ECHO python %py_file%
python %py_file%
GOTO quit

:inspector
ECHO python %py_file% -m inspector
python %py_file% -m inspector
GOTO quit

:text
ECHO pure DOS version not implemented..

:quit
REM EXIT
