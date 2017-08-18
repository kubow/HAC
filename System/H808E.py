# -*- coding: utf-8 -*-
import os
import argparse
# sys.setdefaultencoding('utf-8')


class h808e(object):
    def __init__(self):
        self.enc = self.create_structure()
        self.set_active_node(800)
        self.dir_active = 'C:\\_Run\\Script'
        self.dir_folders = self.get_main_directories()
        self.db_path = ''
        self.db_tables = self.get_table()
        self.db_query = 'SELECT * FROM enc_nodes;'
        # self.db_data = None

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
        sub_folders = []
        for main_folder in self.dir_folders:
            if main_folder == main_node:
                print 'get all directories for {0}'.format(main_node)

    def is_registered_directory(self):
        print 'just check if table exists'
        if os.path.isdir(self.dir_active):
            print 'table do not exist'
            return False
        else:
            return True

    def directory_register(self):
        # load to in memory sqlite database
        self.load_active_directory_memory()
        # transfer to corresponding database
        
        return True

    def load_active_directory_memory(self):
        conn_mem = SO74DB.open_db_connection(":memory:")
        curs_mem = conn_mem.cursor()
        curs_mem.execute(SQL.table_create)
        i = 0
        
        tab_ins = SQL.insert.format('h808e (reg_name, file_dir)')
        
        for root, directories, files in os.walk(self.dir_active):
            curs_mem.execute(tab_ins.format('"", ' + root))
            i += 1
            for filename in files:
                curs_mem.execute(tab_ins.format(i, filename, root, 'date date date',
                                                FileSystemObject(root + '/' + filename).object_size()))
                print '---file {0} registered, checking size.'.format(filename)
                i += 1
        
        self.db_data = curs_mem.execute('select * from h808e;')
        
    def directory_watcher(self):
        flag = True
        if os.path.isdir(self.dir_active):
            if not self.is_registered_directory():
                while flag:
                    flag = self.directory_register()

    def iterate_enc_structure(self):
        directory = self.get_root_path(self.dir_active)
        for en in he.enc:
            # 1. level
            print '--' * int(en['level']) + str(en['code'])
            self.set_active_node(en['code'])
            self.set_db_data(self.get_node_content(str(en['code'])))
            FileSystemObject(directory + str(en['code']) + '.html').refresh_file(self.db_data)

            for esn in en['child']:
                # 2. level
                print '--' * int(esn['level']) + str(esn['code'])
                self.set_active_node(esn['code'])
                self.set_db_data(self.get_node_content(str(esn['code'])))
                FileSystemObject(directory + str(esn['code']) + '.html').refresh_file(self.db_data)

                for essn in esn['child']:
                    # 3. level
                    print '--' * int(essn['level']) + str(essn['code'])
                    self.set_active_node(essn['code'])
                    self.set_db_data(self.get_node_content(str(essn['code'])))
                    FileSystemObject(directory + str(essn['code']) + '.html').refresh_file(self.db_data)

    def iterate_enc_db_structure(self):
        conn = SO74DB.open_db_connection(self.db_path)
        fathers = conn.execute(SQL.select_father_nodes).fetchall()
        main_fathers = [father[0] for father in fathers]
        root_nodes = conn.execute(SQL.select_root_nodes).fetchall()
        for root_node in root_nodes:
            print root_node[2].encode('utf8') + ' root node / id ' + str(
                root_node[4]) + ' / sqn ' + str(root_node[5]) + ' level 1'
        SO74DB.close_db_connection(conn)

    def get_table(self):
        tables = (None, '')
        # all tables within enc table - must run sql
        return tables

    def get_node_content(self, node):
        # print 'load node content from id: ' + str(node)
        query = q.select_node_text.format(node)
        if self.db_path:
            print self.db_path + ' : ' + query
            return SO74DB.execute_not_connected(self.db_path, query)
        else:
            print 'cannot execute {0} in memory database.'.format(query)

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
        # print '? - ' + db_path
        if os.path.isfile(db_path):
            self.db_path = db_path
        else:
            self.db_path = ':memory:'

    def set_db_data(self, text):
        html_content = HTML.pageTemplateBegin.format(self.node, 'toolkit')
        html_content += '{0}' + HTML.pageTemplateMiddle
        html_content += HTML.pageTemplateEnd.format('footer')
        if text:
            html_content = html_content.format(SO74TX.xml_to_html(''.join(text).encode('utf8')))
        else:
            html_content = html_content.format('')

        self.db_data = html_content

    def set_dir_active(self, directory):
        self.dir_active = directory

    def set_active_node(self, node):
        self.node = node


def build_text_menu(directory):
    keep_alive = True
    while keep_alive:
        print("""       ============= -H_808_E- =============
        -------------------------------------
        1.  Open encyklopedia cherrytree
        2.  Open encyklopedia sqlite browser
        3.  Directory synchronizer
        4.  Generate structure from db
        5.  Register directory
        6.  B
        7.  C
        -------------------------------------
        8.  Universal python project
        -------------------------------------
        9.  Browse pages in (FF/CH/IE)
        -------------------------------------
        ==========PRESS 'Q' TO QUIT==========""")
        keep_alive = raw_input("Please run:")
        if keep_alive == "1":
            print("\n Opening cherrytree ...")
            # OS74.run_command_line('cherrytree %s' % args.c)
        elif keep_alive == "2":
            print("\n Opening sqlite browser\n")

        elif keep_alive == "3":
            print("\n Synchronize directories")
            # dropbox synchronizer
        elif keep_alive == "4":
            print 'generate structure'
            he.iterate_enc_structure()

        elif keep_alive == "5":
            print 'register direcotry'
            he.directory_watcher()

        elif keep_alive == "8":
            # running Tkinter GUI
            logger.log_operation('universal python in ' + args.d)
            UI74.build_window(args.d)

        elif str(keep_alive).lower() == "q":
            print("\n Goodbye")
            keep_alive = False
        elif keep_alive != "":
            print("\n Not Valid Choice Try again")


if __name__ == '__main__':

    from log import Log
    import SO74DB
    from OS74 import FileSystemObject
    import UI74
    import SO74TX
    from Template import HTML, SQL

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
