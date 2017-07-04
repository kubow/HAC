# -*- coding: utf-8 -*-
import os
import argparse
import sqlite3
# sys.setdefaultencoding('utf-8')
# H808E modules
import DB74
import OS74
import UI74
import TX74


class h808e(object):
    def __init__(self):
        self.enc = self.create_structure()
        self.folders = self.get_main_directories()
        self.tables = self.get_table()
        self.dir_active = OS74.get_current_dir()
        self.db_path = ''
        self.db_query = 'SELECT * FROM enc_nodes;'
        # self.db_data = None

    def create_structure(self):
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
        for main_folder in self.folders:
            if main_folder == main_node:
                print 'get all directories for {0}'.format(main_node)

    def iterate_enc_structure(self):
        directory = self.get_root_path(self.dir_active)
        for en in he.enc:
            # 1. level
            print '--' * int(en['level']) + str(en['code'])
            refresh_file(directory + str(en['code']) + '.html', self.get_node_content(str(en['code'])))

            for esn in en['child']:
                # 2. level
                print '--' * int(esn['level']) + str(esn['code'])
                refresh_file(directory + str(esn['code']) + '.html', self.get_node_content(str(esn['code'])))

                for essn in esn['child']:
                    # 3. level
                    print '--' * int(essn['level']) + str(essn['code'])
                    refresh_file(directory + str(essn['code']) + '.html', self.get_node_content(str(essn['code'])))

    def iterate_enc_db_structure():
        conn.execute(q.select_father_nodes()).fetchall()
        main_fathers = [father[0] for father in fathers]
        root_nodes = conn.execute(c.select_root_nodes).fetchall()
        for root_node in root_nodes:
            print root_node[2].encode('utf8') + ' root node / id ' + str(
                root_node[4]) + ' / sqn ' + str(root_node[5]) + ' level 1'

    def get_table(self):
        tables = (None, '')
        # all tables within enc table - must run sql
        return tables

    def get_node_content(self, node):
        # print 'load node content from id: ' + str(node)
        query = q.select_node_text
        #query = q.select_node_text.format(node)
        print self.db_path + ' : ' + query
        return DB74.execute_not_connected(self.db_path,query)

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
        separator = OS74.get_separator_from(directory)
        path_list = directory.split(separator)
        for item in path_list:
            if str(item).lower() == 'web':
                nth = int(path_list.index(item)) + 1
                break
        return separator.join(path_list[:nth]) + separator

    def set_db_path(self, db_path):
        print '? - ' + db_path
        if os.path.isfile(db_path):
            self.db_path = db_path
        else:
            self.db_path = ':memory:'

    def set_dir_active(self, directory):
        self.dir_active = directory


class SQL(object):
    select_father_nodes = """SELECT children.father_id, COUNT(node.node_id)
    FROM node
    INNER JOIN children ON node.node_id = children.node_id
    GROUP BY father_id"""
    select_root_nodes = """SELECT children.father_id, node.level, node.name,
    node.txt, node.node_id, children.sequence, enc.code FROM children
    INNER JOIN node ON children.node_id = node.node_id
    INNER JOIN enc ON enc.node_id = node.node_id
    WHERE (children.father_id = 0 )
    ORDER BY children.sequence"""
    select_sub_nodes = """SELECT node.node_id, node.name, node.txt,
    children.sequence, enc.code
    FROM children
    INNER JOIN node ON children.node_id = node.node_id
    INNER JOIN enc ON children.node_id = enc.node_id
    WHERE children.father_id =:father
    ORDER BY children.sequence"""
    select_node_text = """select * from node;"""
    select_node_text3 = """SELECT test FROM "enc" WHERE code = {0};"""
    select_node_text2 = """SELECT txt FROM "enc_nodes" WHERE code = {0};"""


def build_text_menu(directory):
    keep_alive = True
    while keep_alive:
        print("""       ============= -H_808_E- =============
        -------------------------------------
        1.  Open encyklopedia cherrytree
        2.  Open encyklopedia sqlite browser
        3.  Directory synchronizer
        4.  Generate structure from db
        5.  A
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
        elif keep_alive == "2":
            print("\n Opening sqlite browser\n")

        elif keep_alive == "3":
            print("\n Synchronize directories")
            # dropbox synchronizer
        elif keep_alive == "4":
            print 'generate structure'
            he.iterate_enc_structure()

        elif keep_alive == "8":
            # running Tkinter GUI
            print 'universal python in ' + args.d
            GUI.build_window(args.d)

        elif str(keep_alive).lower() == "q":
            print("\n Goodbye")
            keep_alive = False
        elif keep_alive != "":
            print("\n Not Valid Choice Try again")


def refresh_file(filename, text):
    # print 'refreshing filename: ' + filename + ' with text: ' + text
    if os.path.isfile(filename):
        print 'can do..'
    else:
        print 'file {0} not exist, must create'.format(filename)


def register_dir(directory, he):
    # register directory within sqlite database
    conn_mem = sqlite3.connect(":memory:")
    curs_mem = conn_mem.cursor()
    curs_mem.execute("""CREATE TABLE h808e (
        ID int,
        reg_name text,
        file_dir int, --boolean
        last_change text, --date
        size int
        ); """)
    i = 1
    tab_ins = """INSERT INTO h808e
        (reg_name, file_dir)
        VALUES ({0});"""
    col = ('reg_name', 'file_dir')
    for root, directories, files in os.walk(directory):
        curs_mem.execute(tab_ins.format('"", ' + root))
        i += 1
        # iterate files in directory
        for filename in files:
            fln_val = dw.ins_val.format(i, filename, root, 'date date date',
                                        get_file_size(root + '/' + filename))
            v = (filename, root)
            # print v
            if val_exist(v, col, 'dirlist', c):
                msg = '---file {0} registered, checking size.'.format(filename)
            else:
                msg = '---file {0} registering.'.format(filename)
            # c.execute(dw.tab_ins.format(fln_val))
            i += 1
            # print filename
    return c

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="construct h808e")
    parser.add_argument('-c', help='ctb file', type=str, default='')
    parser.add_argument('-d', help='directory', type=str, default='')
    args = parser.parse_args()
    # he class
    he = h808e()
    he.set_dir_active(args.d)
    he.set_db_path(args.c)
    # SQL queries class
    q = SQL()

    # prepare the insert query
    # insert = 'INSERT INTO veci (hmotne, oblast, uroven) VALUES ({0}, "{1}", {2});'
    # browse encyklopedia node (en) + subnode (esn), subsubnode (essn)

    build_text_menu(he)

