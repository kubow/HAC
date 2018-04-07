#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse


def process_web_content(mode='', final_dir='', url=''):
    db = DataBaseObject(FileSystemObject().get_another_directory_file('Settings.sqlite'))
    wc = WebContent(url, log_file=str(args.l), mode=mode)
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
            wc.write_web_content_to_file(html_file_path, w[3])


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

def mode_launcher(mode=None, source=None, additional_par=None, destination=None):
    if not mode:
        print(modes)
        mode = input("Please run:")  # python 3
    while mode:
        if any(str(mode) in s for s in ['1', 'weather', 'wth']):
            if source:
                o = OpenWeatherMap(source.replace('|', ', '))
            else:
                o = OpenWeatherMap('Praha, cz')
            o.write_weather_text(FileSystemObject(args.w).append_objects(file='index.html'))
        elif any(str(mode) in s for s in ['2', '3', 'rest', 'rss', 'restaurants']):
            browse_internet(mode, source)
        elif any(str(mode) in s for s in ['4', 'lister', 'list']):
            if not destination:
                logger.log_operation('cannot export list, missing destination')
                mode = None
            if any(str(additional_par) in s for s in ['dir', 'directory']):
                FileSystemObject(source, destination).directory_lister(list_files=False)
            elif any(str(additional_par) in s for s in ['file', 'files']):
                FileSystemObject(source, destination).directory_lister(list_files=True)
            elif any(str(additional_par) in s for s in ['data', 'database']):
                temp_connect_database(source)
            else:
                logger.log_operation('not known mode: ' + additional_par)
        elif any(str(mode) in s for s in ['5', 'browser', 'browsing']):
            if any(str(additional_par) in s for s in ['dir', 'directory']):
                from UI74 import directory_browser
                directory_browser()
            elif any(str(additional_par) in s for s in ['file', 'files']):
                logger.log_operation('universal file browser still not implemented')
            elif any(str(additional_par) in s for s in ['data', 'database']):
                temp_connect_database(source) # will be a GUI browser in future
            elif any(str(additional_par) in s for s in ['web', 'html']):
                browse_internet(mode='', match_dir='', url=source)
            else:
                logger.log_operation('not known ' + mode + ' mode: ' + additional_par)
        elif any(str(mode) in s for s in ['6', 'convert', 'converter']):
            input_object = FileSystemObject(source)
            if not destination:
                output_object = FileSystemObject(source+'2')
            else:
                output_object = FileSystemObject(destination)
            if input_object.is_file:
                if not additional_par:
                    new_content = TextContent(input_object.object_read()).replace_line_endings()
                # must do a broader logic
                elif 'json' in additional_par:
                    new_content = TextContent(input_object.object_read())
                output_object.object_write(new_content)
            elif input_object.is_folder:
                for file_name in input_object.object_read().items():
                    file_content = TextContent(FileSystemObject(file_name).object_read())
                    if not additional_par:
                        new_content = file_content.replace_crlf_lf()
                    # must do a broader logic
                        
        elif any(str(mode) in s for s in ['7', 'comparison', 'compare']):
            if not destination:
                print('cannot compare, missing destination')
                mode = None
            print("\n  Comparing {0} <-> {1} \n".format(source, destination))
            input_object = FileSystemObject(source)
            output_object = FileSystemObject(destination)
            if input_object.is_folder and output_object.is_folder:
                compare_directories(source, destination)
            elif input_object.is_file and output_object.is_file:
                if input_object.obj_type == 'db':
                    compare_databases(source, destination, additional_par)
                else:
                    logger.log_operation('cannot compare in mode: ' + additional_par)
            else:
                print(TextContent(source).similar_to(destination))
        elif str(mode).lower() == "q":
            print("\n Goodbye")
            mode = False
        elif mode != "":
            print("\n " + mode + "Not Valid Choice Try again")
        mode = None


if __name__ == '__main__':
    from OS74 import FileSystemObject, compare_directories
    from DB74 import DataBaseObject, compare_databases, temp_connect_database
    from TX74 import WebContent, TextContent
    from MP74 import OpenWeatherMap
    from log import Log

    global modes
    modes = ("""       ===-Software_Launcher-currently_implement_modes-===
            -------------------------------------
            1.  Download weather
            2.  Download restaurants menu
            3.  Download rss news
            -------------------------------------
            4.  Lister directory/database
            5.  Browser (directory, database, web, network stream)
            6.  Converter (text_file_line_endings)
            -------------------------------------
            7.  Comparison text / directory / database
            8.  - NA -
            9.  - NA -
            -------------------------------------
            ==========PRESS 'Q' TO QUIT==========""")
    input_loc = (" place/location of original data\n"
                   "     web page, to be read, weather location to find, file to read")
    output_loc = (" type of file to write (HTML, SQLite, All)\n"
                   "or destination location folder")
    extra_par = ('extra parameter for graphic modes ("graphic"), etc...')
    parser = argparse.ArgumentParser(description="weather@location")
    parser.add_argument('-e', help=extra_par, type=str, default=None)
    parser.add_argument('-m', help=modes, type=str, default=None)
    parser.add_argument('-i', help=input_loc, type=str, default='')
    parser.add_argument('-o', help=output_loc, type=str, default=None)
    parser.add_argument('-l', help='logfile', type=str, default='')
    args = parser.parse_args()
    if not args.e:
        extra = __file__
    else:
        extra = args.e
    
    global logger
    logger = Log(args.l, args.m, extra, True)
    logger.log_operation('Run in mode {0}: source / input {1} -> {2}'.format(args.m, args.i, args.o))
    mode_launcher(mode=args.m, source=args.i, additional_par=args.e, destination=args.o)