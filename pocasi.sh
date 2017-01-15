#!/bin/bash
#!/usr/bin python

#location='Horni Pocernice,cz'
location='Praha,cz'
mainHTML=${PWD}'/index.html'
pythonFILE=${PWD}/System/DataWeather/WriteWeatherActual.py

#python generate htm's
echo ${pythonFILE}
#python ${pythonFILE} ${mainHTML} 
python ${pythonFILE} ${mainHTML} ${location}

#cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $mainHTML
