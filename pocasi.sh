#!/bin/bash
#!/usr/bin python

YY=$(date +%Y)
MM=$(date +%m)
last_run_file=${PWD}/Multimedia/Weather/last.run
mainHTML=${PWD}/index.html
settings_db=${PWD}/System/Device/settings.db
py_dev_file=${PWD}/System/Device/DataWrite.py
py_for_file=${PWD}/System/DataWeather/WriteWeatherActual.py

#location='city,country'
IFS='|' read -r loc cnt <<< $(sqlite3 ${settings_db} 'select * from place_active')
location=${loc},${cnt}

#python read forecast
#====================
#syntax: py_for_file file_to_write location
#forecast temporarily diabled
#python ${py_for_file} ${mainHTML} ${location}

#python read actual weather data
#===============================
weather_db=${PWD}/Multimedia/Weather/${loc}_${YY}${MM}.db
platform=$(sqlite3 ${settings_db} 'select devicename from device where active=1')
echo ${platform} - writing ${loc}_${YY}${MM}.db
python ${py_dev_file} -d ${weather_db} -p ${platform}
touch ${last_run_file}
