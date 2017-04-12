@echo off
chcp 1250
SET BinDirectory=c:\_Run\App\Mapoaplikace\EpaNET\WD\
SET WorkingDirectory=c:\_Model\
for /f "tokens=1,2,3,4,5,6* delims=," %%i in ('C:\_Run\App\Uzitecne\UnixUtils\usr\local\wbin\date.exe +"%%y,%%m,%%d,%%H,%%M,%%S"') do set yy=%%i& set mo=%%j& set dd=%%k& set hh=%%l& set mm=%%m& set ss=%%n
rem C:\_Run\App\Uzitecne\UnixUtils\usr\local\wbin\date.exe +"%%d/%%m/%%Y %%r" > %WorkingDirectory%date.txt
C:\_Run\App\Uzitecne\UnixUtils\usr\local\wbin\date.exe +"%%d/%%m/%%Y 12:00:00 PM" > %WorkingDirectory%date.txt
SET /p RunDate= < %WorkingDirectory%date.txt
rem del %WorkingDirectory%date.txt

"%BinDirectory%EPANET.exe" "inpfilename:%WorkingDirectory%Model-Base.inp" "now:%RunDate%" hydraulicrun:SS_Qd commaseparator:. csvseparator:; saveres:True min:10 max:90
rem the parameter now could be "now:01/01/2014 12:00:00 PM" or "now:Now" or %RunDate%