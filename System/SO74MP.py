try:
    import pyowm
    weather_wrapper = False
except ImportError:
    print('using weather simple web requesting')
    weather_wrapper = False
from osmapi import OsmApi

from OS74 import DateTimeObject
from SO74TX import WebContent, JsonContent
from Template import HTML, SQL


class OpenWeatherMap(object):
    def __init__(self, location=None, owm_api='442f089290ae64104a202bfb8d52e0cb'):
        print('OpenWeatherMap.org - validate API-key disabled - location: ' + location)
        if not location:
            location = 'Horni Pocernice,cz'  # 'Necin,cz'
        if weather_wrapper:
            # syntax = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
            owm = pyowm.OWM(owm_api)        
            self.place_obj = owm.weather_at_place(location)._location
            self.place_name = self.place_obj._name + ', ' + self.place_obj._country
            self.place_coor = str(self.place_obj._lat) + ', ' + str(self.place_obj._lon)
            self.weather_local = owm.weather_at_place(location).get_weather()
            self.weather_forecast = owm.daily_forecast(location).get_forecast()
            self.weather_forecast_days = self.weather_forecast._weathers
            self.heading = 'Weather at ' + location, self.build_text_place() + '\n' + self.build_text_local()
            # tomorrow = pyowm.timeutils.tomorrow()
            # self.is_sunny_tomorrow = self.weather_forecast.will_be_sunny_at(tomorrow) # true/false
        else:
            q_address = 'api.openweathermap.org/data/2.5/weather?q='
            owm = WebContent(q_address + location + '&APPID=' + owm_api)
            owm.process_url()
            json_data = JsonContent(owm.html_text, direct=True).content
            self.place_obj = ''
            self.place_name = ''
            self.place_coor = json_data['coord']
            self.weather_local = json_data['weather']
            self.weather_forecast = json_data['main']
            self.weather_forecast_days = ''
            self.heading = ''

    def build_text_place(self):
        text = self.place_name + ' (' + self.place_coor + ')'
        return HTML.heading.format('1', text)

    def build_text_local(self):
        stat = HTML.paragraph.format('Status: ' + self.weather_local._status)
        pres = HTML.paragraph.format('Pressure: ' + str(self.weather_local._pressure['press']) + ' kPa')
        humi = HTML.paragraph.format('Humidity: ' + str(self.weather_local._humidity) + ' %')
        rain = HTML.paragraph.format('Raining: ' + str(self.weather_local._rain) + ' mm')
        snow = HTML.paragraph.format('Snowing: ' + str(self.weather_local._snow) + ' mm')
        temp = HTML.paragraph.format('Temperature: ' + str(self.weather_local.get_temperature('celsius')))
        wind = HTML.paragraph.format('Wind: ' + str(self.weather_local.get_wind()) + ' m/s')
        time = HTML.paragraph.format('last proccess: ' + DateTimeObject().date.strftime('%d.%m.%Y %H:%M:%S'))

        velocities = (stat, pres, humi, rain, snow, temp, wind, time)
        text_local = '\n'.join(velocities)
        return HTML.div_tag_id.format('weather_now', text_local)

    def build_text_forecast(self):
        velocities = (self.weather_local._status, str(self.weather_local._pressure['press']),
                      str(self.weather_local._humidity))


class OpenStreetMap(object):
    def __init__(self, url):
        self.url = url
        self.osm_api = 'AIzaSyDkEnsboDEPpmq98svR1ORv-zACEy2TSjQ'
        print('OpenStreetrMap.org - validate API-key disabled')
        osm = OsmApi()


'''class WeatherUnderground(object):
    def __init__(self):
        self.actual_data = self.get_actual(location)

class Mapping(object):
    #from qgis.core import *
    print(u'aaa')
    '''


if __name__ == '__main__':

    from log import Log
