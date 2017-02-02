#!/bin/bash
#!/usr/bin python

YY=$(date +%Y)
MM=$(date +%m)
mainHTML=${PWD}/index.html
settings_db=${PWD}/System/Device/settings.db
py_rain_file=${PWD}/System/Device/Rain.py
py_temp_file=${PWD}/System/Device/Temperature.py
py_wind_file=${PWD}/System/Device/Wind.py
py_forecast_file=${PWD}/System/DataWeather/WriteWeatherActual.py

#location='city,country'
IFS='|' read -r loc cnt <<< $(sqlite3 ${settings_db} 'select * from place_active')
location=${loc},${cnt}

#python read forecast
#====================
#syntax: py_forecast_file file_to_write location
python ${py_forecast_file} ${mainHTML} ${location}

#python read actual weather data
#===============================
weather_db=${PWD}/Multimedia/Weather/${loc}_${YY}${MM}.db
echo ${weather_db}
driver=$(sqlite3 ${settings_db} 'select driverloc from device where active=1')
echo ${driver}
#python ${py_rain_file} ${weather_db}
#python ${py_wind_file} ${weather_db}
#python ${py_temp_file} ${weather_db}
