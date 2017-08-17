#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

echo "$parent_path"
# calling batch menu (platform independent)
python ./System/H808E.py -d ../Web/64/Astrologie/ -c ../H808E.ctb -l ./Multimedia/logfile.log
