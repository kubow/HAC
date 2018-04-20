@echo off
SET py_file=%~dp0System\SO74.py
SET log_file=%~dp0Multimedia\logfile.log

IF /I '%1%'=='h' GOTO HANA
IF /I '%1%'=='s' GOTO SQLite
IF /I '%1%'=='b' GOTO FolderBrowse
IF /I '%1%'=='f' GOTO FolderList
IF /I '%1%'=='l' GOTO FileList
IF /I '%1%'=='t' GOTO Text

GOTO MENU

:MENU
echo 1st parameter:
echo - - - DATABASE MODE - - - 
echo   h - HANA 
echo   s - SQLite
echo - - - FILE MODE - - - 
echo   t - pure text file
echo - - - FOLDER MODE - - -
echo   b - browse folders
echo   f - list folders
echo   l - list folder files
echo 2nd parameter: object location
GOTO QUIT

:HANA
SET py_file="C:\Program Files\sap\hdbclient\hdbalm.py"
python %py_file%
GOTO QUIT

:SQLite
SET mode_name=browser
SET extra_name=database
SET in_object=%2
goto execute_py

:FolderBrowse
SET mode_name=browser
SET extra_name=folder
SET in_object=%2
if [%2]==[] SET in_object='C:\_Run\Web'
goto execute_py

:FolderList
SET mode_name=list
SET extra_name=folder
SET in_object=%2
if [%2]==[] SET in_object='C:\_Run\Web'
goto execute_py

:FileList
SET mode_name=list
SET extra_name=files
SET in_object=%2
if [%2]==[] SET in_object='C:\_Run\Web'
goto execute_py
REM ECHO report files DOS way:
REM DIR /s/b *.mp3 > %out_object%

:Text
SET mode_name=browser
SET extra_name=text
SET in_object=%2
goto execute_py

:execute_py
ECHO python %py_file% -m %mode_name% -i %in_object% -e %extra_name% -l %log_file%
python %py_file% -m %mode_name% -i %in_object% -e %extra_name% -l %log_file%
GOTO quit

:problem
echo MODE:%mode_name%
echo EXTRA_MODE: %extra_name%
echo INPUT:%in_object%
echo OUTPUT:%out_object%

:QUIT
REM EXIT
