@echo off
REM check if python path in variable PATH (presume python installed)
REM for /f "delims=" %%a in ('REG QUERY "HKLM\SOFTWARE\Python\PythonCore" /s ^| findstr InstallPath') do  (
REM   set key=%%a
REM   goto :endfor
REM )
REM :endfor
REM for /f "tokens=2*" %%a in ('REG QUERY %key% /ve') do set "CHESSPYTHONPATHv1=%%~bpython.exe"
REM echo %CHESSPYTHONPATHv1%
REM check if pip path in variables
SET /p args=<%~dp0py_packages.txt
echo checking if installed: %args%
python installer.py %args% > %~dp0py_install.log