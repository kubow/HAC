# -*- coding: utf-8 -*-
import pyowm
import argparse
import datetime
import os

import DB74
import OS74
from TX74 import WebContent, RssContent
from Template import HTML, SQL


class OpenWeatherMap(object):
    def __init__(self, location):
        # syntax = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
        owm_api = '1050e850fbcc463dd98a726d6af37134'
        owm = pyowm.OWM(owm_api)
        print 'OpenWeatherMap.org - validate API-key disabled'
        self.place_obj = owm.weather_at_place(location)._location
        self.place_name = self.place_obj._name + ', ' + self.place_obj._country
        self.place_coor = str(self.place_obj._lat) + ', ' + str(self.place_obj._lon)
        self.weather_local = owm.weather_at_place(location).get_weather()
        self.weather_forecast = owm.daily_forecast(location).get_forecast()
        self.weather_forecast_days = self.weather_forecast._weathers
        self.heading = 'Weather at ' + location, self.build_text_place() + '\n' + self.build_text_local()
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
        time = HTML.paragraph.format('last proccess: ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

        velocities = (stat, pres, humi, rain, snow, temp, wind, time)
        text_local = '\n'.join(velocities)
        return HTML.div_tag_id.format('weather_now', text_local)

    def build_text_forecast(self):
        velocities = (self.weather_local._status, str(self.weather_local._pressure['press']),
                      str(self.weather_local._humidity))


'''class WeatherUnderground(object):
    def __init__(self):
        self.actual_data = self.get_actual(location)

class Mapping(object):
    #from qgis.core import *
    print u'aaa'
    '''


def process_web_content(mode, final_dir, url=None):
    settings_db = os.path.dirname(os.path.realpath(__file__)) + '/Settings.sqlite'
    if url:
        wc = WebContent(url)
        print wc
    else:
        if 'rest' in mode:
            web_objects = DB74.execute_many_not_connected(settings_db, 'SELECT * FROM RestActive;')
            for restaurant in web_objects:
                if restaurant[4]:
                    wc = WebContent(restaurant[4])
                    wc.procces_url(restaurant[7], restaurant[6])
                else:
                    wc = WebContent(restaurant[5])  # zomato style
                    wc.procces_url('id', 'daily-menu-container')
                html_file_path = final_dir + '/' + restaurant[2].encode('utf-8') + '.html'
                if wc.div:
                    print 'creating ' + html_file_path + ' from: ' + wc.url
                    OS74.file_write(html_file_path,
                                    HTML.skelet_titled.format(restaurant[3].encode('utf-8'), wc.div))
                else:
                    print 'no content parsed from: ' + wc.url
        elif 'rss' in mode:
            web_objects = DB74.execute_many_not_connected(settings_db, 'SELECT * FROM RssActive;')
            for rss in web_objects:
                if rss[3]:
                    wc = RssContent(rss[3])
                else:
                    print 'no address to fetch ...' + str(rss)
                html_file_path = final_dir + '/' + rss[2].encode('utf-8') + '.html'
                if wc.div:
                    print 'creating ' + html_file_path + ' from: ' + wc.url
                    OS74.file_write(html_file_path,
                                    HTML.skelet_titled.format(rss[3].encode('utf-8'), wc.div.encode('utf-8')))
                else:
                    print 'no content parsed from: ' + wc.url


def browse_internet(mode, match_dir, url=None):
    if 'rest' in mode:
        final_dir = match_dir + '/Multimedia/RestMenu'
        url = None
    elif 'rss' in mode:
        final_dir = match_dir + '/Multimedia/NewsFeed'
        url = None
    else:
        final_dir = match_dir + '/Multimedia/WebsCont'
    OS74.create_dir_if_neccesary(final_dir)
    logger.log_operation('proccessing internet content to ' + final_dir)
    process_web_content(mode, final_dir, url)


def set_default_location(try_this):
    if try_this:
        return try_this
    else:
        # determine setting from database / make default
        return 'Horni Pocernice,cz'  # 'Necin,cz'


def write_weather_text(html_file, title, content):
    logger.log_operation('writing content {0} to file: {1}'.format(title, html_file))
    OS74.file_write(html_file, HTML.skelet_titled.format(title, content.encode('utf-8')))


if __name__ == '__main__':
    from log import Log
    localization = (" place/location where user wants to read weather\n"
                    "     or a link to a web page, which will be read")
    destination = (" type of file to write (HTML, SQLite, All)\n"
                    "or destination location")
    def_loc = 'Praha, cz'
    parser = argparse.ArgumentParser(description="weather@location")
    parser.add_argument('-g', help='mode', type=str, default='weather')
    parser.add_argument('-w', help=destination, type=str, default='none')
    parser.add_argument('-p', help=localization, type=str, default='none')
    parser.add_argument('-l', help='logfile', type=str, default='none')
    args = parser.parse_args()
    loc = set_default_location(args.p)
    logger = Log(args.l, args.g)
    if 'weather' in args.g:
        o = OpenWeatherMap(loc)
        print 'writing content to file: ' + args.w
        write_weather_text(args.w + '/index.html', o.heading[0], o.heading[1])
    else:
        browse_internet(args.g, args.w, args.p)
