# -*- coding: utf-8 -*-
import pyowm
import argparse
import datetime
import os

import DB74
from OS74 import FileSystemObject
from SO74TX import WebContent, RssContent
from Template import HTML, SQL
from osmapi import OsmApi

class OpenWeatherMap(object):
    def __init__(self, location):
        # syntax = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
        owm_api = '1050e850fbcc463dd98a726d6af37134'
        owm = pyowm.OWM(owm_api)
        print 'OpenWeatherMap.org - validate API-key disabled'
        if not location:
            location = 'Horni Pocernice,cz'  # 'Necin,cz'
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


class OpenStreetMap(object):
    def __init__(self, url):
        self.url = url
        self.osm_api = 'AIzaSyDkEnsboDEPpmq98svR1ORv-zACEy2TSjQ'
        print 'OpenStreetrMap.org - validate API-key disabled'
        osm = OsmApi()


'''class WeatherUnderground(object):
    def __init__(self):
        self.actual_data = self.get_actual(location)

class Mapping(object):
    #from qgis.core import *
    print u'aaa'
    '''


def process_web_content(mode, final_dir, url=None):
    path_separator = FileSystemObject(final_dir).separator
    settings_db = os.path.dirname(os.path.realpath(__file__)) + path_separator + 'Settings.sqlite'
    if url:
        wc = WebContent(url)
        print wc
    else:
        if 'rest' in mode:
            web_objects = DB74.execute_many_not_connected(settings_db, 'SELECT * FROM RestActive;')
            for restaurant in web_objects:
                if restaurant[4]:
                    wc = WebContent(restaurant[4])
                    wc.process_url(restaurant[7], restaurant[6])
                else:
                    wc = WebContent(restaurant[5])  # zomato style
                    wc.process_url('id', 'daily-menu-container')
                html_file_path = final_dir + path_separator + restaurant[2].encode('utf-8') + '.html'
                wc.write_web_content_to_file(html_file_path, restaurant[3])
        elif 'rss' in mode:
            web_objects = DB74.execute_many_not_connected(settings_db, 'SELECT * FROM RssActive;')
            for rss in web_objects:
                if rss[3]:
                    wc = RssContent(rss[3])
                else:
                    print 'no address to fetch ...' + str(rss)
                html_file_path = final_dir + path_separator + rss[2].encode('utf-8') + '.html'
                wc.write_rss_content_to_file(html_file_path, rss[3])


def browse_internet(mode, match_dir, url=None):
    path_separator = FileSystemObject(args.l).separator
    if 'rest' in mode:
        final_dir = path_separator.join((match_dir, 'Multimedia', 'RestMenu'))
        url = None
    elif 'rss' in mode:
        final_dir = path_separator.join((match_dir, 'Multimedia', 'NewsFeed'))
        url = None
    else:
        final_dir = path_separator.join((match_dir, 'Multimedia', 'WebsCont'))
    FileSystemObject(final_dir).create_dir_if_neccesary()
    logger.log_operation('proccessing internet content to ' + final_dir)
    process_web_content(mode, final_dir, url)


def write_weather_text(html_file, title, content):
    logger.log_operation('writing content {0} to file: {1}'.format(title, html_file))
    FileSystemObject(html_file).file_write(HTML.skelet_titled.format(title, content.encode('utf-8')))


if __name__ == '__main__':
    from log import Log
    localization = (" place/location where user wants to read weather\n"
                    "     or a link to a web page, which will be read")
    destination = (" type of file to write (HTML, SQLite, All)\n"
                    "or destination location")
    parser = argparse.ArgumentParser(description="weather@location")
    parser.add_argument('-g', help='mode', type=str, default='weather')
    parser.add_argument('-w', help=destination, type=str, default='none')
    parser.add_argument('-p', help=localization, type=str, default='none')
    parser.add_argument('-l', help='logfile', type=str, default='none')
    args = parser.parse_args()
    logger = Log(args.l, args.g, __file__, True)
    if 'weather' in args.g:
        if args.p:
            if '|' in args.p:
                def_loc = args.p.replace('|', ', ')
            else:
                def_loc = args.p
        else:
            def_loc = 'Praha, cz'
        o = OpenWeatherMap(def_loc)
        print 'writing content to file: ' + args.w
        path_separator = FileSystemObject(args.l).separator
        write_weather_text(args.w + path_separator + 'index.html', o.heading[0], o.heading[1])
    else:
        browse_internet(args.g, args.w, args.p)
