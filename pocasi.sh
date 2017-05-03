#!/bin/bash
#!/usr/bin python

YY=$(date +%Y)
MM=$(date +%m)
DD=$(date +%d)
mainHTML=${PWD}/index.html
log_dir=${PWD}/Multimedia/
data_db=${PWD}/Multimedia/Measured/
last_run_file=${data_db}last.run

settings_db=${PWD}/System/Device/settings.db
py_dev_file=${PWD}/System/Device/DataWrite.py
py_for_file=${PWD}/System/DataWeather.py

echo ============================================
echo "getting location in format ('city','country')"
echo ============================================
command=$(sqlite3 ${settings_db} 'select * from place_active;')
IFS='|' read -r loc cnt <<< ${command}
location=${loc},${cnt}
echo got: ${location} : 'select * from place_active'
echo ====================
echo python read forecast 
echo ====================
#syntax: py_for_file file_to_write location
#forecast temporarily diabled
python ${py_for_file} ${mainHTML} ${location}
echo ==========================
echo python write proccessed data
echo ==========================
#weather_mo=${data_db}${YY}${MM}.db
#weather_dy=${data_db}${YY}${MM}${DD}.db
platform=$(sqlite3 ${settings_db} 'select devicename from device_active;')
echo Running on ${platform} - writing ${YY}${MM}"("${DD}").db"
#python ${py_dev_file} -d ${weather_mo} -p ${platform}
python ${py_dev_file} -d ${platform} -l ${data_db}
python ${PWD}/System/log.py -l ${PWD}/Multimedia/logfile.log -m "weather" -t "agregated all data"
touch ${last_run_file}
