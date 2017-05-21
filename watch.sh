#!/bin/bash
#!/usr/bin python
bbb='/home/kubow/Dokumenty/Script'
h808e='/home/kubow/Dokumenty/H808E.ctb'
python ${bbb}/System/H808E.py -d "/home/kubow/Dokumenty/Web/"
echo "run in ${bbb}"
#python ${PWD}/System/DirWatch.py -l ${PWD}/Multimedia/logfile.log -w "/home/kubow/Dokumenty/Web/" -d ${PWD}/Multimedia/logfile.sqlite
python ${bbb}/System/DirWatch.py -l ${bbb}/Multimedia/logfile.log -w "/home/kubow/Dokumenty/Web/" -d ${bbb}/Multimedia/logfile.sqlite
echo "done run"
