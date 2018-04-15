#!/bin/bash

get_location()
{
    settings_db=${PWD}/System/Settings.sqlite
    command=$(sqlite3 ${settings_db} 'select * from place_active;')
    IFS='|' read -r loc cnt <<< ${command}
    echo ${loc},${cnt}
}

read_weather()
{
    echo =====================
    echo "python read weather"
    echo =====================
    echo syntax: ${py_forecast_file} -m weather -i location -o destination_to_write_results
    ${py_forecast_file} -m weather -i ${location} -o ${PWD} -l ${log_file}
}

aggregate()
{
    echo =============================
    echo "python write proccessed data"
    echo =============================
    echo 'syntax: '${py_data_file}' -l location -m mode(rea/agg)'
    echo 'Running on linux - writing '${YY}${MM}"("${DD}").db"
    ${py_data_file} -l ${log_dir} -m aggregate
}

log_dir=${PWD}/Multimedia/
log_file=${log_dir}logfile.log
system_dir=${PWD}/System/


py_data_file=${PWD}/System/DV72.py
py_forecast_file=${PWD}/System/SO74.py

if [ "$1" = "b" ] # big tick
then
    echo ============================================
    echo "getting location in format ('city','country')"
    echo ============================================
    location=$(get_location)
    echo got: ${location}
    read_weather
    aggregate
elif [ "$1" = "s" ]
then
    aggregate
else
    echo "1st argument - cycle type"
    echo "    b - Big tick / weather + forecast + aggregate data" 
    echo "    s - Small tick / just aggregate data"
fi

