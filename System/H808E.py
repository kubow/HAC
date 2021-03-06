#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import argparse

from log import Log
from DB74 import DataBaseObject
from OS74 import FileSystemObject, CurrentPlatformControl as cpc
from TX74 import xml_to_html
from Template import HTML, SQL


class h808e(object):
    def __init__(self, debug=False):
        self.enc = self.create_structure()
        self.set_active_node(800)
        self.dir_active = 'C:\\_Run\\Script'
        self.dir_folders = self.get_main_directories()
        self.db_path = ''
        self.db_tables = self.get_table()
        self.db_query = 'SELECT * FROM enc_nodes;'
        self.toolkit = 'toolkit'  # special upper menu toolkit
        self.area_links = 'will be a list with referrals...'
        # self.db_data = None
        self.debug = debug

    @staticmethod
    def create_structure():
        """constructor of h808e - list of dictionaries
        key code - number code to define area
        key name - names will be filled after matching
        key child - reference all children
        will be a module after.."""
        h808e = []
        a_max = 3  # only nodes from 400 to 700
        lev = 1  # starting from first level
        for a in range(4):
            a_max += 1
            sub_categories = []
            for b in range(a_max):
                lev += 1
                sub_sub_categories = []
                for c in range(9):
                    if (a_max * 100) + ((b + 1) * 10) + (c + 1) > 599:
                        real = False
                    else:
                        real = True
                    lev += 1
                    sub_sub = {'code': (a_max * 100) + ((b + 1) * 10) + (c + 1),
                               'real': real, 'name': '', 'level': lev}
                    sub_sub_categories.append(sub_sub)
                    lev -= 1
                sub = {'code': (a_max * 100) + ((b + 1) * 10), 'real': real,
                       'name': '', 'level': lev, 'child': sub_sub_categories}
                lev -= 1
                sub_categories.append(sub)
            h808e_dict = {'code': a_max * 100, 'real': real, 'name': '',
                          'level': lev, 'child': sub_categories}
            h808e.append(h808e_dict)
        return h808e

    def get_main_directories(self):
        folders = []
        for area in self.enc:
            list_number = self.get_list_number_item(area['code'])
            self.enc[list_number]['directory'] = None
            for node in area['child']:
                sublist_number = self.get_list_number_item(node['code'])
                self.enc[list_number]['child'][sublist_number]['directory'] = int(str(node['code'])[:2])
                folders.append(int(str(node['code'])[:2]))
        # all folders within enc table
        return folders

    def get_sub_directories(self, main_node):
        # sub_folders = []
        for main_folder in self.dir_folders:
            if main_folder == main_node:
                print('get all directories for {0}'.format(main_node))

    def is_registered_directory(self):
        is_registered = FileSystemObject(self.dir_active).is_folder
        if self.debug:
            logger.log_operation('directory ' + self.dir_active + ' exists: ' + str(is_registered))
        return is_registered

    def directory_register(self):
        # load to in memory sqlite database
        self.load_active_directory_memory()
        # transfer to corresponding database
        if self.contain_same_data:
            return True
        else:
            return False

    def load_active_directory_memory(self):
        database = DataBaseObject(":memory:", active=True)
        database.execute(SQL.table_create)
        i = 0
        
        for root, directories, files in os.walk(self.dir_active):
            database.execute(SQL.table_insert.format('"", "", "' + root + '", "", ""'))
            i += 1
            for filename in files:
                database.execute(SQL.table_insert.format(str(i) + ', "' + filename + '", "' + root + '", "date date date", "' +
                                                FileSystemObject(root + '/' + filename).object_size() + '"'))
                print('---file {0} registered, checking size.'.format(filename))
                i += 1
        
        self.db_data = database.return_many('select * from h808e;')
    
    def contain_same_data(self, another_db):
        # flag = False
        db = DataBaseObject(another_db)
        for record in self.db_data:
            print(str(record[0]) + '/' + str(db.obj_list))
            
    def directory_watcher(self):
        flag = True
        if FileSystemObject(self.dir_active).is_folder:
            if not self.is_registered_directory():
                while flag:
                    flag = self.directory_register()

    def iterate_enc_structure(self):
        directory = self.get_root_path(self.dir_active)
        for en in he.enc:
            # 1. level
            print('--' * int(en['level']) + str(en['code']))
            self.set_active_node(en['code'])
            self.set_db_data(self.get_node_content(str(en['code'])))
            FileSystemObject(directory + str(en['code']) + '.html').object_write(self.db_data)

            for esn in en['child']:
                # 2. level
                print('--' * int(esn['level']) + str(esn['code']))
                self.set_active_node(esn['code'])
                self.set_db_data(self.get_node_content(str(esn['code'])))
                FileSystemObject(directory + str(esn['code']) + '.html').object_write(self.db_data)

                for essn in esn['child']:
                    # 3. level
                    print('--' * int(essn['level']) + str(essn['code']))
                    self.set_active_node(essn['code'])
                    self.set_db_data(self.get_node_content(str(essn['code'])))
                    FileSystemObject(directory + str(essn['code']) + '.html').object_write(self.db_data)

    def iterate_enc_db_structure(self):
        db = DataBaseObject(self.db_path)
        fathers = db.return_many(SQL.select_father_nodes)
        main_fathers = [father[0] for father in fathers]
        root_nodes = db.return_many(SQL.selectRootNodes)
        for root_node in root_nodes:
            print(root_node[2] + ' root node / id ' + str(
                root_node[4]) + ' / sqn ' + str(root_node[5]) + ' level 1')

    def get_table(self):
        sql = 'select code, name, query, folder from enc_nodes where length(query) > 0;'
        tables = DataBaseObject(self.db_path).return_many(sql)
        # all tables within enc table - must run sql
        return tables

    def get_node_content(self, node):
        # print('load node content from id: ' + str(node))
        query = SQL.select_node_text.format(node)
        if self.db_path:
            if self.debug:
                print(self.db_path + ' : ' + query)
            return DataBaseObject(self.db_path).return_one(query)
        else:
            print('cannot execute {0} in memory database.'.format(query))

    def get_nth_node(self, nth, parent_node):
        if parent_node.isdigit():
            return self.get_nth_number(nth, parent_node) * 100
        else:
            return 800
            # not defined node, return max

    def get_nth_number(self, nth, node_number):
        return int(str(node_number)[nth - 1:nth])

    def get_list_number_item(self, number):
        return self.get_nth_number(1, number) - 4

    def get_root_path(self, directory):
        separator = FileSystemObject(directory).separator
        path_list = directory.split(separator)
        for item in path_list:
            if str(item).lower() == 'web':
                nth = int(path_list.index(item)) + 1
                break
        return separator.join(path_list[:nth]) + separator

    def set_db_path(self, db_path):
        print('? - ' + db_path)
        if FileSystemObject(db_path).is_file:
            self.db_path = db_path
        else:
            self.db_path = ':memory:'

    def set_db_data(self, text):
        html_content = HTML.pageTemplateBegin.format(self.node, self.toolkit)
        html_content += self.area_links + HTML.pageTemplateMiddle
        html_content += '{0}' + HTML.pageTemplateEnd.format('footer')
        if text:
            html_content = html_content.format(xml_to_html(''.join(text)))
        else:
            html_content = html_content.format('')

        self.db_data = html_content

    def set_dir_active(self, directory):
        self.dir_active = directory

    def set_active_node(self, node):
        self.node = node


def build_text_menu(he):
    keep_alive = True
    while keep_alive:
        print("""       ============= -H_808_E- =============
        -------------------------------------
        1.  Open encyklopedia cherrytree
        2.  Open encyklopedia sqlite browser
        3.  Directory synchronizer
        4.  Generate structure from db
        5.  Register directory
        -------------------------------------
        6.  Kivy interface
        7.  AppJar python project
        8.  Universal python project
        -------------------------------------
        9.  Browse pages in (FF/CH/IE)
        -------------------------------------
        ==========PRESS 'Q' TO QUIT==========""")
        keep_alive = input("Please run:")  # python 3
        file_name = FileSystemObject(he.db_path).last_part()
        active_directory = args.c.replace(file_name, '')
        if keep_alive == '1':
            print("\n    Opening cherrytree ...\n")
            cherry = cpc('cherrytree')
            cherry.run_with_argument(arg_1=args.c)
            print("\n    Cherrytree closed ...\n")
        elif keep_alive == '2':
            print("\n    Opening sqlite browser\n")
            sqlitedb = cpc('sqlitedb')
            sqlitedb.run_with_argument(arg_1=str(args.c).replace('.ctb', '_tab.db'))
            print("\n    Closing sqlite browser\n")
        elif keep_alive == '3':
            # dropbox synchronizer
            print("\n    Synchronize directories\n")
            dropbox_dir = FileSystemObject(cpc().homepath).append_objects(dir='Dropbox')
            
            db = args.c.replace('.ctb', '_tab.db')
            file_name_db = file_name.replace('.ctb', '_tab.db')
            dropbox_he = FileSystemObject(dropbox_dir).append_objects(file=file_name)
            dropbox_db = dropbox_he.replace('.ctb', '_tab.db')
            
            local_he_mod = FileSystemObject(args.c).object_mod_date()
            local_db_mod = FileSystemObject(db).object_mod_date()
            dropbox_he_mod = FileSystemObject(dropbox_he).object_mod_date()
            dropbox_db_mod = FileSystemObject(dropbox_db).object_mod_date()
            
            row_he = file_name + '     | ' + local_he_mod + ' {0} ' + dropbox_he_mod
            row_db = file_name_db + '  | ' + local_db_mod + ' {0} ' + dropbox_db_mod
            
            print('file          | ' + active_directory + '              | ' + dropbox_dir)
            print('='*60)
            if local_he_mod > dropbox_he_mod:
                print(row_he.format('>'))
                FileSystemObject(args.c).copy_file_to(dropbox_dir)
            elif local_he_mod < dropbox_he_mod:
                print(row_he.format('<'))
                FileSystemObject(dropbox_he).copy_file_to(active_directory)
            else:
                print(row_he.format('='))
            
            if local_db_mod > dropbox_db_mod:
                print(row_db.format('>'))
                FileSystemObject(db).copy_file_to(dropbox_dir)
            elif local_db_mod < dropbox_db_mod:
                print(row_db.format('<'))
                FileSystemObject(dropbox_db).copy_file_to(active_directory)
            else:
                print(row_db.format('='))
            print('\n')
        elif keep_alive == '4':
            print('generate structure')
            he.iterate_enc_structure()
        elif keep_alive == '5':
            print("\n    Register directories\n")
            he.directory_watcher()
        elif keep_alive == '6':
            print("\n    Kivy interface starting...\n")
            import UI74KW
            UI74KW.MainApp().run()
        elif keep_alive == '7':
            db_file = he.db_path.replace('.ctb', '_tab.db')
            logger.log_operation('universal python for ' + db_file)
            cpc(FileSystemObject().append_objects(file='UI74AJ.py')).external_call()
        elif keep_alive == '8':
            import UI74
            # running Tkinter GUI
            logger.log_operation('universal python in ' + args.d)
            UI74.h808e_browser(args.d)
        elif keep_alive == '9':
            print("\n    Opening web browser\n")
            browser = cpc('web')
            browser.run_with_argument(arg_1=args.c)
            print("\n    Closing web browser\n")
        elif str(keep_alive).lower() == "q":
            print("\n Goodbye")
            keep_alive = False
        elif keep_alive != "":
            print("\n {0} (type {1}) Not Valid Choice Try again".format(keep_alive, type(keep_alive)))


def build_structure_numbers():
    """constructor of h808e - list of dictionaries
    will be a module after.."""
    return [x for x in range(400, 800) if str(x)[1:2] <= str(x)[:1] and str(x)[2:] <= str(x)[:1]]
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="construct h808e")
    parser.add_argument('-c', help='ctb file', type=str, default='')
    parser.add_argument('-d', help='directory', type=str, default='')
    parser.add_argument('-l', help='log file', type=str, default='')
    args = parser.parse_args()
    
    logger = Log(args.l, 'main', 'h808e', True)
    
    he = h808e()
    he.set_dir_active(args.d)
    he.set_db_path(args.c)

    # prepare the insert query
    # insert = 'INSERT INTO veci (hmotne, oblast, uroven) VALUES ({0}, "{1}", {2});'
    # browse encyklopedia node (en) + subnode (esn), subsubnode (essn)

    build_text_menu(he)
