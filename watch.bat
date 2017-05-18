@echo off
SET bbb=c:\_Run\Script\
SET h808e = "c:\_Run\H808E.ctb"
python %bbb%System\H808E.py
pause
echo run in %bbb%
python %bbb%System\DirWatch.py -l %bbb%Multimedia\logfile.log -w c:\_Run\Web\ -d %bbb%Multimedia\logfile.sqlite
echo "done run"
