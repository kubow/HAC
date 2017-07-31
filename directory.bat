@echo off
SET log_file=%~dp0Multimedia\logfile.log
SET mlt_dir='C:\_Run\Web'
SET py_for_file=%~dp0System\OS74.py

REM echo '-b', help='browse dir', type=str, default='')
REM echo '-l', help='list dir', type=str, default='')
REM echo '-f', help='file output', type=str, default='')
echo python %py_for_file% -b %mlt_dir% -f %log_file%
python %py_for_file% -b %mlt_dir% -f %log_file%

REM echo pure DOS version
REM dir /s/b *.mp3 > dir.txt
