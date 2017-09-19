@ECHO OFF

REM IF PARAMETER = F
SET F_BROWSER="C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
SET F_DIR="C:\Users\%USERNAME%\AppData\Local\Mozilla\Firefox\Profiles"
REM IF PARAMETER = E
SET E_BROWSER="C:\Program Files\Internet Explorer\iexplore.exe"
SET E_DIR="C:\Users\%USERNAME%\AppData\Local\Microsoft\Internet Explorer\Profiles"
REM IF PARAMETER = C
SET C_BROWSER="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
SET C_DIR="C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Profiles"

SET B_NAME=Chrome

REM IF SECOND_PARAMETER = 0
SET HTML="C:\_Run\Web\400.html"

ECHO Using browser - %B_NAME%
SET BROWSER=%C_BROWSER% 
%BROWSER% %HTML%

goto end

:cookie
ECHO "Clearing cookies"
REM del /q /s /f "%DataDir%"
REM rd /s /q "%DataDir%"
REM for /d %%x in (C:\Users\%USERNAME%\AppData\Roaming\Mozilla\Firefox\Profiles\*) do del /q /s /f %%x\*sqlite

:end
exi