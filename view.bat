@echo off
SET log_file=%~dp0Multimedia\logfile.log

IF /I '%1%'=='h' GOTO HANA
IF /I '%1%'=='s' GOTO SQLite
IF /I '%1%'=='b' GOTO FolderBrowse
IF /I '%1%'=='l' GOTO FolderList
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
echo   l - list folder files
echo 2nd parameter: object location
GOTO QUIT

:HANA
SET py_file="C:\Program Files\sap\hdbclient\hdbalm.py"
python %py_file%
GOTO QUIT

:SQLite
SET py_file=%~dp0System\SO74DB.py
echo python %py_file% -l %log_file% -a %2%
python %py_file% -l %log_file% -a %2%
goto QUIT

:FolderBrowse
SET mode=True
if [%2]==[] goto Folder
SET mlt_dir='C:\_Run\Web'
goto Folder

:FolderList
SET mode=""
if [%2]==[] goto Folder
SET mlt_dir='C:\_Run\Web'
goto Folder

:Folder
SET py_file=%~dp0System\OS74.py
echo python %py_file% -i %mlt_dir% -m True/False (%mode%) -l %log_file%
python %py_file% -i %mlt_dir% -m %mode% -l %log_file%
goto QUIT

REM echo pure DOS version
REM dir /s/b *.mp3 > dir.txt

:Text
SET py_file=%~dp0System\SO74TX.py
echo python %py_file% -l %log_file% 
python %py_file% -i %2% -l %log_file% 
goto QUIT

:QUIT
REM EXIT
