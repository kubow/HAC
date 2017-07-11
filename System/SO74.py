import os
import sys
import pyowm
import argparse

class OpenWeatherMap(object):
    """observe weather function
    API-key required for owm
    second parameter location"""
    def __init__(self):
        print 'validate API-key disabled'
        self.api_key = '1050e850fbcc463dd98a726d6af37134'
        self.owm = pyowm.OWM(self.api_key)
        print 'getting location '
        
        
    def obs_weather(self, loc):
        wap = self.owm.weather_at_place(loc)
        frc = self.owm.daily_forecast(loc)
        # wbs = will_be_sunny()
        # wac = self.owm.weather_around_coords(-22.57, -43.12)
        observed = {'actual':wap.get_weather(), 'forecast':frc}
        return observed
        
    def will_be_sunny():
        tomorrow = pyowm.timeutils.tomorrow()
        return forecast.will_be_sunny_at(tomorrow)  # true/false

'''class WeatherUnderground(object):
    def __init__(self):
        self.actual_data = self.get_actual(location)'''
        

""" Passing space-separated command line arguments
1. location where user wants to read weather
2. type of file to write (HTML, SQLite, All)
"""
parser = argparse.ArgumentParser(description="weather@location")
parser.add_argument('-l', help='Location', type=str, default='')
parser.add_argument('-w', help='Write path', type=str, default='none')
args = parser.parse_args()
if args.l:
    loc = args.l
else:
    # determine setting from database
    loc = 'Horni Pocernice,cz' #'Necin,cz'
print 'weather forecast in '+loc

# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
o = OpenWeatherMap()

obs = o.owm.weather_at_place(loc)
w = obs.get_weather()
# Weather details
# w.get_wind()                  # {'speed': 4.6, 'deg': 330}
# w.get_humidity()              # 87
# w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

htm=open(args.w, 'w+')
print 'file '+args.w+' created...'
htm.write('<HTML>\n<HEAD>\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">\n')
htm.write('<TITLE>Weather at '+loc+'</TITLE>\n</HEAD>\n<BODY>\n<H1>')
htm.write('Weather at '+loc+'</H1>\n<P>')
#htm.write(w = str(obs.get_weather()))
htm.write('Nearest station: '+obs._location._name+' ('+obs._location._country+')\n</BR>')
htm.write('Temperature: '+str(w.get_temperature('celsius'))+'\n</BR>')
htm.write('Wind: '+str(w.get_wind())+'\n</BR>')
htm.write('Humidity: '+str(w.get_humidity())+'\n</BR></P>')
htm.write('</BODY>\n</HTML>')

htm.close

