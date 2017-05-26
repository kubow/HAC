@ECHO OFF
SET enc_path=C:\_Run\Web\
SET py_script_path=C:\_Run\Script\System\

:MENU
CLS

ECHO ============= -H_808_E- =============
ECHO -------------------------------------
ECHO 1.  Open encyklopedia cherrytree
ECHO 2.  Open encyklopedia sqlite browser
ECHO 3.  Directory synchronizer
ECHO 4.  Generate structure from db
ECHO 5.  A
ECHO 6.  B
ECHO 7.  C
ECHO -------------------------------------
ECHO 8.  Universal python project
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
IF /I '%INPUT%'=='4' GOTO Structure
IF /I '%INPUT%'=='5' GOTO A
IF /I '%INPUT%'=='6' GOTO B
IF /I '%INPUT%'=='7' GOTO C
IF /I '%INPUT%'=='8' GOTO UniPy
IF /I '%INPUT%'=='9' GOTO BrowsePages
IF /I '%INPUT%'=='Q' GOTO Quit

CLS

ECHO ============INVALID INPUT============
ECHO -------------------------------------
ECHO Please select a number from the Main
ECHO Menu [1-9] or select 'Q' to quit.
ECHO -------------------------------------
ECHO ======PRESS ANY KEY TO CONTINUE======

PAUSE > NUL
GOTO MENU

:CherryTree
CALL C:\_Run\Shortcut\Batch\CherryTree.bat
GOTO MENU

:SQLite
CALL C:\_Run\Shortcut\Batch\SQLite.bat
GOTO MENU

:DirSync
SET python_script=%py_script_path%DirWatch.py
FOR /d %%a in ("%enc_path%*") do (
  rem FOR %%* in ("%%a\.") do ECHO %%a
  rem python %python_script% %%a 
  rem C:\_Run\Web\ENC\41
  cd %%a
  echo %%a
  tree /f
  pause
)
rem will be a loop over all encyklopedia folders
PAUSE
GOTO MENU

:Structure
SET python_script=C:/_Run/H808E_gen.py
python %python_script%
ECHO done
PAUSE
GOTO MENU

:UniPy
SET python_script=%py_script_path%GUI.py -d c:\_Run\Web\64\Astrologie\
ECHO will use tkinter and make a system to input data
python %python_script%
PAUSE
GOTO MENU

:BrowsePages
CALL C:\_Run\Shortcut\Batch\www.bat
GOTO MENU

:Quit
CLS

ECHO ==============THANKYOU===============
ECHO -------------------------------------
ECHO ======PRESS ANY KEY TO CONTINUE======

PAUSE>NUL
REM EXIT
