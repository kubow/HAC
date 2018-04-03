@ECHO OFF

SET JAVA_HOME=C:\SAP\Shared\SAPJRE-8_1_022_64BIT
SET now_dir=%~dp0
SET app_dir=C:\_Run\App\Database\openrefine-2.8

cd %app_dir%
call refine.bat
cd now_dir