# -*- coding: utf-8 -*-
import pyowm
import argparse
import os

import DB74
import OS74
from TX74 import WebContent
from Template import HTML


class OpenWeatherMap(object):
    def __init__(self, location):
        # syntax = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
        print 'OpenWeatherMap.org - validate API-key disabled'
        self.owm_api = '1050e850fbcc463dd98a726d6af37134'
        self.place_obj = pyowm.OWM(self.owm_api).weather_at_place(location)._location
        self.place_name = self.place_obj._name + ', ' + self.place_obj._country
        self.place_coor = str(self.place_obj._lat) + ', ' + str(self.place_obj._lon)
        self.weather_local = pyowm.OWM(self.owm_api).weather_at_place(location).get_weather()
        self.weather_forecast = pyowm.OWM(self.owm_api).daily_forecast(location).get_forecast()
        self.weather_forecast_days = self.weather_forecast._weathers
        # tomorrow = pyowm.timeutils.tomorrow()
        # self.is_sunny_tomorrow = self.weather_forecast.will_be_sunny_at(tomorrow) # true/false

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

        velocities = (stat, pres, humi, rain, snow, temp, wind)
        text_local = '\n'.join(velocities)
        return HTML.div_tag_id.format('weather_now', text_local)

    def build_text_forecast(self):
        velocities = (self.weather_local._status, str(self.weather_local._pressure['press']),
                      str(self.weather_local._humidity))


'''class WeatherUnderground(object):
    def __init__(self):
        self.actual_data = self.get_actual(location)'''


def browse_internet(match_dir):
    OS74.create_dir_if_neccesary(match_dir + '/Multimedia/RestMenu')
    settings_db = os.path.dirname(os.path.realpath(__file__))+'/Device.db'
    restaurants = DB74.execute_many_not_connected(settings_db, 'SELECT * FROM RestActive;')
    template = HTML.skelet_titled
    for restaurant in restaurants:
        if restaurant[4]:
            wc = WebContent(restaurant[4])
        else:
            wc = WebContent(restaurant[5]) # zomato style
        wc.procces_url()
        html_file_pah = match_dir + '/' + restaurant[2].encode('utf-8') + '.html'
        if wc.div:
            print html_file_pah
        else:
            print html_file_pah + ' ... not creating, cannot fetch source'
        # OS74.file_write(html_file_path, template.format(restaurant[3].encode('utf-8'), wc.div))
        
def write_temperature_text(html_file, title, content):
    OS74.file_write(html_file, HTML.skelet_titled.format(title, content.encode('utf-8')))

def temporary_class_Mapping():
    #from qgis.core import *
    print u'aaa'

if __name__ == '__main__':
    localization = ' location where user wants to read weather'
    destination = ' type of file to write (HTML, SQLite, All)/destination location'
    parser = argparse.ArgumentParser(description="weather@location")
    parser.add_argument('-l', help=localization, type=str, default='')
    parser.add_argument('-g', help='HTML mode', type=str, default='')
    parser.add_argument('-w', help=destination, type=str, default='none')
    args = parser.parse_args()
    if args.g:
        browse_internet(args.w)
    else:
        # check for submitted location
        if args.l:
            loc = args.l
        else:
            # determine setting from database / make default
            loc = 'Horni Pocernice,cz' #'Necin,cz'

        print 'getting weather forecast of location: '+loc
        o = OpenWeatherMap(loc)

        print 'writing content to file: '+args.w
        write_temperature_text(args.w, 'Weather at '+loc, o.build_text_place() + '\n' + o.build_text_local())
