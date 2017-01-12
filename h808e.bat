@ECHO OFF

:MENU
CLS

ECHO ============= -H_808_E- =============
ECHO -------------------------------------
ECHO 1.  Open encyklopedia cherrytree
ECHO 2.  Open encyklopedia sqlite browser
ECHO 3.  Directory synchronizer
ECHO 4.  A
ECHO 5.  E
ECHO 6.  B
ECHO 7.  C
ECHO -------------------------------------
ECHO 8.  D
ECHO -------------------------------------
ECHO 9.  Browse pages in (FF/CH/IE)
ECHO -------------------------------------
ECHO ==========PRESS 'Q' TO QUIT==========
ECHO.

SET INPUT=
SET /P INPUT=Please select a number:

IF /I '%INPUT%'=='1' GOTO CherryTree
IF /I '%INPUT%'=='2' GOTO SQLite
IF /I '%INPUT%'=='3' GOTO DirSync
IF /I '%INPUT%'=='4' GOTO A
IF /I '%INPUT%'=='5' GOTO E
IF /I '%INPUT%'=='6' GOTO B
IF /I '%INPUT%'=='7' GOTO C
IF /I '%INPUT%'=='8' GOTO D
IF /I '%INPUT%'=='9' GOTO BrowsePages
IF /I '%INPUT%'=='Q' GOTO Quit

CLS

ECHO ============INVALID INPUT============
ECHO -------------------------------------
ECHO Please select a number from the Main
echo Menu [1-9] or select 'Q' to quit.
ECHO -------------------------------------
ECHO ======PRESS ANY KEY TO CONTINUE======

PAUSE > NUL
GOTO MENU

:CherryTree
call C:\_Run\Shortcut\Batch\CherryTree.bat
goto MENU

:SQLite
call C:\_Run\Shortcut\Batch\SQLite.bat
goto MENU

:DirSync
SET enc_path=C:_Run\Web\ENC\
SET python_script=C:\_Run\Script\System\FileWatcher\FileWatcherRegistry.py
for /d %%a in ("%enc_path%*") do (
  for %%* in ("%%a\.") do echo %%a
  reom python %python_script% %%a 
  rem C:\_Run\Web\ENC\41
)
rem will be a loop over all encyklopedia folders
pause
goto MENU

:BrowsePages
call C:\_Run\Shortcut\Batch\www.bat
goto MENU

:Quit
CLS

ECHO ==============THANKYOU===============
ECHO -------------------------------------
ECHO ======PRESS ANY KEY TO CONTINUE======

PAUSE>NUL
EXIT