#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'
settings_db=${PWD}/System/Device/settings.db
py_rain_file=${PWD}/System/Device/Rain.py
py_temp_file=${PWD}/System/Device/Temperature.py
py_wind_file=${PWD}/System/Device/Wind.py
py_forecast_file=${PWD}/System/DataWeather/WriteWeatherActual.py

#location='Horni Pocernice,cz'
IFS='|' read -r loc cnt <<< $(sqlite3 ${settings_db} 'select * from place_active')
location=${loc},${cnt}

#python generate htm's
echo ${py_forecast_file}
#python ${py_forecast_file} ${mainHTML} 
python ${py_forecast_file} ${mainHTML} ${location}

#cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $mainHTML
