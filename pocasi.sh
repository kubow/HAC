#!/bin/bash
#!/usr/bin python

YY=$(date +%Y)
MM=$(date +%m)
DD=$(date +%d)

log_dir=${PWD}/Multimedia/
log_file=${log_dir}logfile.log
settings_db=${PWD}/System/Settings.sqlite
py_dev_file=${PWD}/System/DV72.py
py_for_file=${PWD}/System/SO74.py

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
python ${py_for_file} -g weather -p ${location} -w ${PWD} -l ${log_file}
echo ==========================
echo python write proccessed data
echo ==========================
data_db=${PWD}/Multimedia/Measured/
last_run_file=${data_db}last.run
#weather_mo=${data_db}${YY}${MM}.db
#weather_dy=${data_db}${YY}${MM}${DD}.db
platform=$(sqlite3 ${settings_db} 'select devicename from device_active;')
echo Running on ${platform} - writing ${YY}${MM}"("${DD}").db"
#python ${py_dev_file} -d ${weather_mo} -p ${platform}
python ${py_dev_file} -d ${platform} -s luxo -l ${data_db}
touch ${last_run_file}
