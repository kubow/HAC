# -*- coding: utf-8 -*-
import argparse
import os


def process_web_content(mode, final_dir, url=None):
    path_separator = FileSystemObject(final_dir).separator
    settings_db = DataBaseObject(os.path.dirname(os.path.realpath(__file__)) + path_separator + 'Settings.sqlite')
    log_db = args.l
    wc = WebContent(url)
    if url:
        print wc
    else:
        if 'rest' in mode:
            web_objects = settings_db.return_many('SELECT * FROM RestActive;')
            for restaurant in web_objects:
                if restaurant[4]:
                    wc.url = restaurant[4]
                    wc.process_url(restaurant[7], restaurant[6])
                else:
                    wc.url = restaurant[5]  # zomato style
                    wc.process_url('id', 'daily-menu-container')

                html_file_path = final_dir + path_separator + restaurant[2].encode('utf-8') + '.html'
                wc.write_web_content_to_file(html_file_path, restaurant[3], log_db)

        elif 'rss' in mode:
            web_objects = settings_db.return_many('SELECT * FROM RssActive;')
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
    FileSystemObject(final_dir).object_create_neccesary()
    logger.log_operation('proccessing internet content to ' + final_dir)
    process_web_content(mode, final_dir, url)


def write_weather_text(html_file, title, content):
    logger.log_operation('writing content {0} to file: {1}'.format(title, html_file))
    FileSystemObject(html_file).object_write(HTML.skelet_titled.format(title, content.encode('utf-8')), 'w+')


if __name__ == '__main__':

    from OS74 import FileSystemObject, DateTimeObject
    from SO74DB import DataBaseObject
    from SO74TX import WebContent, RssContent
    from SO74MP import OpenWeatherMap, OpenStreetMap
    from Template import HTML, SQL
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
        write_weather_text(FileSystemObject(args.w).append_file('index.html'), o.heading[0], o.heading[1])
    else:
        browse_internet(args.g, args.w, args.p)
