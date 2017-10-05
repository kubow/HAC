#!/bin/bash
#!/usr/bin python
dir_main=${PWD}
dir_up=$(dirname $dir_main)
h808e=$dir_up'/H808E.ctb'
python ${dir_main}/System/H808E.py -d $dir_up'/Web/'
echo "run in ${dir_main}"
python ${dir_main}/System/DirWatch.py -l ${bbb}/Multimedia/logfile.log -w "/home/kubow/Dokumenty/Web/" -d ${bbb}/Multimedia/logfile.sqlite
echo "done run"
