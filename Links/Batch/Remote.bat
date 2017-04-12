@echo off
tasklist /nh /fi "imagename eq mstsc.exe" | find /i "mstsc.exe" > nul || goto pustit
start c:\_Run\Script\Registry\restore_window.vbs

goto konec


:pustit


start %windir%\system32\mstsc.exe

exit



:konec

exit