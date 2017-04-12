import os
import sys
import pyowm

class OpenWeatherMap(key, loc):
    """observe weather function
    API-key required for owm
    second parameter location"""
    print 'validate API-key disabled'
    print 'getting location ' + loc
    def obs_weather(key):
        owm = pyowm.OWM(key)
        wap = owm.weather_at_place(loc)
        frc = owm.daily_forecast(loc)
        # wbs = will_be_sunny()
        # wac = owm.weather_around_coords(-22.57, -43.12)
        observed = {'actual':wap.get_weather(), 'forecast':frc}
        return observed
        
    def will_be_sunny():
        tomorrow = pyowm.timeutils.tomorrow()
        return forecast.will_be_sunny_at(tomorrow)  # true/false
    

""" Passing space-separated command line arguments
1. location where user wants to read weather
2. type of file to write (HTML, SQLite, All)
"""
parser = argparse.ArgumentParser(description="weather@location")
parser.add_argument('-l', help='Location', type=str, default='')
parser.add_argument('-w', help='Write path', type=str, default='none')
args = parser.parse_args()
# Determine if passed parguments for running over a directory
if len(sys.argv)>2:
    # print sys.argv
    # write_file_path=os.path.dirname(os.path.realpath(__file__))+'/weather.htm'
    write_file_path=sys.argv[1]
    # print write_file_path
    # print sys.argv[2]
    loc = sys.argv[2]
else:
    loc = 'Horni Pocernice,cz' #'Necin,cz'

print 'weather forecast in '+loc

# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
owm = pyowm.OWM('1050e850fbcc463dd98a726d6af37134')  # You MUST provide a valid API key

obs = owm.weather_at_place(loc)
w = obs.get_weather()
# Weather details
# w.get_wind()                  # {'speed': 4.6, 'deg': 330}
#w.get_humidity()              # 87
#w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

htm=open(args.l, 'w+')
print 'file '+args.l+' created...'
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

