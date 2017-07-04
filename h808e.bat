@ECHO OFF
SET base_path=C:\_Run\
SET enc_path=%base_path%Web\
SET py_script_path=%base_path%Script\System\

:START
ECHO ************************************
python %py_script_path%H808E.py -d %enc_path%64\Astrologie\ -c %base_path%H808E.ctb
PAUSE
