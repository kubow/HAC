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
        if not location:
            location = 'Horni Pocernice,cz'  # 'Necin,cz'
        print('OpenWeatherMap.org - validate API-key disabled - location: ' + location)
        if weather_wrapper:
            # syntax = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
            owm = pyowm.OWM(owm_api)
            self.place_name = self.owm.weather_at_place(location)._location._name + ', ' + self.owm.weather_at_place(location)._location._country  # check
            self.place_coor = str(self.owm.weather_at_place(location)._location._lat) + ', ' + str(self.owm.weather_at_place(location)._location._lon)  # check
            self.weather_local = owm.weather_at_place(location).get_weather()
            self.weather_forecast = owm.daily_forecast(location).get_forecast()
            self.weather_forecast_days = self.weather_forecast._weathers
            # tomorrow = pyowm.timeutils.tomorrow()
            # self.is_sunny_tomorrow = self.weather_forecast.will_be_sunny_at(tomorrow) # true/false
        else:
            q_address = 'api.openweathermap.org/data/2.5/{0}?q='
            actual_data = self.owm_data_from_web(q_address.format('weather') + location + '&APPID=' + owm_api)
            self.place_name = actual_data['name'] + ', ' + actual_data['sys']['country']
            self.place_coor = str(actual_data['coord']['lon']) + ', ' + str(actual_data['coord']['lat'])
            self.weather_local = actual_data['main']
            self.weather_local['status'] = actual_data['weather'][0]['main']
            self.weather_local['description'] = actual_data['weather'][0]['description']
            self.weather_local.update(actual_data['wind'])
            weather_forecast = self.owm_data_from_web(q_address.format('forecast') + location + '&APPID=' + owm_api)
            self.weather_forecast = weather_forecast
            self.weather_forecast_days = ''
        self.heading = 'Weather at ' + location, self.build_text_place() + '\n' + self.build_text_local()

    def build_text_place(self):
        text = self.place_name + ' (' + self.place_coor + ')'
        return HTML.heading.format('1', text)

    def build_text_local(self):
        stat = HTML.paragraph.format('Status: ' + self.weather_local['status'] + '(' + self.weather_local['description'] + ')')
        pres = HTML.paragraph.format('Pressure: ' + str(self.weather_local['pressure']) + ' kPa')
        humi = HTML.paragraph.format('Humidity: ' + str(self.weather_local['humidity']) + ' %')
        rain = HTML.paragraph.format('Raining: ' + str(0) + ' mm')
        snow = HTML.paragraph.format('Snowing: ' + str(0) + ' mm')
        temp = HTML.paragraph.format('Temperature: ' + str(self.weather_local['temp'] - 273.15))
        wind = HTML.paragraph.format('Wind: ' + str(self.weather_local['speed']) + ' m/s')
        time = HTML.paragraph.format('last proccess: ' + DateTimeObject().date.strftime('%d.%m.%Y %H:%M:%S'))

        velocities = (stat, pres, humi, rain, snow, temp, wind, time)
        text_local = '\n'.join(velocities)
        return HTML.div_tag_id.format('weather_now', text_local)

    def owm_data_from_web(self, address):
        owm = WebContent(address)
        owm.process_url()
        owm_data = JsonContent(owm.html_text, direct=True).content
        #velocities = (self.weather_local._status, str(self.weather_local._pressure['press']),
        #              str(self.weather_local._humidity))
        return owm_data


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
