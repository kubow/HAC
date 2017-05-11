echo off
cls
powershell.exe -ExecutionPolicy Bypass -Command "c:\_Run\Script\System\Installer\GetSoftwareList.ps1" /conf "C:\..." /res "C:\.."

pause