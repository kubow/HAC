# -*- coding: utf-8 -*-

def process_web_content(mode, final_dir, url=''):
    db = DataBaseObject(FileSystemObject(__file__).get_another_directory_file('Settings.sqlite'))
    log_file = str(args.l)
    wc = WebContent(url)
    final_dir_obj = FileSystemObject(final_dir)
    if url:
        print(wc)
    else:
        if 'rest' in mode:
            web_objects = db.return_many('SELECT * FROM src_restaurant;')
            for restaurant in web_objects:
                if restaurant[4]:
                    wc.url = restaurant[4]
                    wc.process_url(restaurant[7], restaurant[6])
                else:
                    wc.url = restaurant[5]  # zomato style
                    wc.process_url('id', 'daily-menu-container')

                html_file_path = final_dir_obj.append_objects(file=restaurant[2] + '.html')
                wc.write_web_content_to_file(html_file_path, restaurant[3], log_file)

        elif 'rss' in mode:
            web_objects = db.return_many('SELECT * FROM src_rss;')
            for rss in web_objects:
                if rss[3]:
                    wc = RssContent(rss[3])
                else:
                    print('no address to fetch ...' + str(rss))
                html_file_path = final_dir_obj.append_objects(file=rss[2] + '.html')
                wc.write_rss_content_to_file(html_file_path, rss[3])


def browse_internet(mode, match_dir, url=''):
    if 'rest' in mode:
        sub_directory_name = 'RestMenu'
    elif 'rss' in mode:
        sub_directory_name = 'NewsFeed'
    else:
        sub_directory_name = 'WebsCont'
    final_dir = FileSystemObject(match_dir).append_objects(dir1='Multimedia', dir2=sub_directory_name)
    FileSystemObject(final_dir).object_create_neccesary()
    logger.log_operation('proccessing internet content to ' + final_dir)
    process_web_content(mode, final_dir, url)


if __name__ == '__main__':
    import argparse
    from OS74 import FileSystemObject, DateTimeObject
    from DB74 import DataBaseObject
    from TX74 import WebContent, RssContent
    from MP74 import OpenWeatherMap, OpenStreetMap
    from Template import HTML, SQL
    from log import Log

    localization = (" place/location where user wants to read weather\n"
                    "     or a link to a web page, which will be read")
    destination = (" type of file to write (HTML, SQLite, All)\n"
                   "or destination location")
    parser = argparse.ArgumentParser(description="weather@location")
    parser.add_argument('-g', help='mode', type=str, default='weather')
    parser.add_argument('-w', help=destination, type=str, default='')
    parser.add_argument('-p', help=localization, type=str, default='')
    parser.add_argument('-l', help='logfile', type=str, default='')
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
        logger.log_operation('writing content {0} to file: {1}'.format(o.heading[0], 'index.html'))
        o.write_weather_text(FileSystemObject(args.w).append_objects(file='index.html'))
    else:
        browse_internet(args.g, args.w, args.p)
