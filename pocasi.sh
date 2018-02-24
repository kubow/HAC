#!/bin/bash
#!/usr/bin python

log_dir=${PWD}/Multimedia/
log_file=${log_dir}logfile.log
system_dir=${PWD}/System/

settings_db=${PWD}/System/Settings.sqlite
py_data_file=${PWD}/System/DV72.py
py_forecast_file=${PWD}/System/UI74SO.py

if [ "$1" = "b" ] # big tick
then
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
    echo syntax: ${py_forecast_file} -g weather -p location -w destination_to_write_results
    python ${py_forecast_file} -g weather -p ${location} -w ${PWD} -l ${log_file}
    echo ==========================
    echo python write proccessed data
    echo ==========================
    platform='linux'
    echo 'syntax: '${py_data_file}' -l location -m mode(rea/agg)'

    echo Running on ${platform} - writing ${YY}${MM}"("${DD}").db"
    python ${py_data_file} -l ${log_dir} -m aggregate
elif [ "$1" = "s" ]
then
    echo ==========================
    echo python write proccessed data
    echo ==========================
    platform='linux'
    echo 'syntax: '${py_data_file}' -l location -m mode(rea/agg)'

    echo Running on ${platform} - writing ${YY}${MM}"("${DD}").db"
    #python ${py_data_file} -d ${weather_mo} -p ${platform}
    python ${py_data_file} -l ${log_dir} -m aggregate
else
    echo "1st argument - cycle type"
    echo "    b - Big tick / weather + forecast + aggreagte data" 
    echo "    s - Small tick / just aggregate data"
fi

