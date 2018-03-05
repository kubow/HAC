# -*- coding: utf-8 -*-


def process_web_content(mode='', final_dir='', url=''):
    db = DataBaseObject(FileSystemObject().get_another_directory_file('Settings.sqlite'))
    log_file = str(args.l)
    wc = WebContent(url, mode=mode)
    final_dir_obj = FileSystemObject(final_dir)
    if url:
        print(wc.process_url())
    else:
        if 'rest' in mode:
            web_objects = db.return_many('SELECT * FROM src_restaurant;')
        elif 'rss' in mode:
            web_objects = db.return_many('SELECT * FROM src_rss;')
        else:
            web_objects = None  # must implement other browsing mode types
        for w in web_objects:
            if w[5]:
                wc.url = w[5]
                wc.process_url(w[6], w[7])
            elif w[8]:
                wc.url = w[8]  # zomato style
                wc.process_url('id', 'daily-menu-container')
            else:
                print('cannot proceed with address:' + str(w))
            html_file_path = final_dir_obj.append_objects(file=w[4] + '.html')
            wc.write_web_content_to_file(html_file_path, w[3], log_file)


def browse_internet(mode='', match_dir='', url=''):
    if 'rest' in mode:
        sub_directory_name = 'RestMenu'
    elif 'rss' in mode:
        sub_directory_name = 'NewsFeed'
    else:
        sub_directory_name = 'WebsCont'
    if not match_dir:
        match_dir = FileSystemObject().dir_up()
    final_dir = FileSystemObject(match_dir).append_objects(dir1='Multimedia', dir2=sub_directory_name)
    FileSystemObject(final_dir).object_create_neccesary()
    logger.log_operation('proccessing internet content to ' + final_dir)
    process_web_content(mode, final_dir, url)


if __name__ == '__main__':
    import argparse
    from OS74 import FileSystemObject
    from DB74 import DataBaseObject
    from TX74 import WebContent
    from MP74 import OpenWeatherMap
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
