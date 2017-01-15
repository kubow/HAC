#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'
pythonFILE=${PWD}/System/DataWeather/WriteWeatherActual.py

#python generate htm's
echo ${pythonFILE}
python ${pythonFILE} ${mainHTML} 'Horni Pocernice,cz'

cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $mainHTML
