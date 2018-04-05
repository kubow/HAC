#!/bin/bash
if [ "$1" = "b" ]; then
	/usr/bin/qbrowser %F
elif [ "$1" = "d" ]; then
	/usr/bin/qgis %F
else
    echo "argument to run QGIS app"
    echo "    b - QGIS Browser"
    echo "    d - QGIS desktop"
fi
