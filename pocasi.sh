#!/bin/bash
#!/usr/bin python

YY=$(date +%Y)
MM=$(date +%m)
last_run_file=${PWD}/Multimedia/Weather/last.run
mainHTML=${PWD}/index.html
settings_db=${PWD}/System/Device/settings.db
py_dev_file=${PWD}/System/Device/DataWrite.py
py_for_file=${PWD}/System/DataWeather/WriteWeatherActual.py

echo ============================================
echo "getting location in format ('city','country')"
echo ============================================
command=$(sqlite3 ${settings_db} 'select * from place_active')
IFS='|' read -r loc cnt <<< ${command}
location=${loc},${cnt}
echo got: ${location} : 'select * from place_active'
echo ====================
echo python read forecast 
echo ====================
echo syntax: ${py_for_file} file_to_write location (now disabled)
#syntax: py_for_file file_to_write location
#forecast temporarily diabled
#python ${py_for_file} ${mainHTML} ${location}

echo ==========================
echo python read weather actual
echo ==========================
weather_db=${PWD}/Multimedia/Weather/${loc}_${YY}${MM}.db
platform=$(sqlite3 ${settings_db} 'select devicename from device where active=1')
echo ${platform} - writing ${loc}_${YY}${MM}.db
python ${py_dev_file} -d ${weather_db} -p ${platform}
touch ${last_run_file}
