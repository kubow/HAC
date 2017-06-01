# -*- coding: utf-8 -*-
import os
import argparse
import sqlite3
#sys.setdefaultencoding('utf-8')
# H808E modules
import GUI

class h808e(object):
    """
    # folders = property(self.get_folder)
    # print 'aaaaaaaaaaaaaaaaaaaaaaa'
    # tables = property(self.get_table)
    """
    def __init__(self):
        self.folders = self.get_folder()
        self.tables = self.get_table()
    
    def construct(self):
        """constructor of h808e - list of dictionaries
        in dictionary..main structure:
        key code - number code to define area
        key name - names will be filled after matching
        key child - reference all children
        will be a module after.."""
        h808e = []
        # only nodes from 400 to 700
        # todo: match names
        a_max = 3
        # starting from first level
        lev = 1
        for a in range(4):
            a_max += 1
            print 'main row: ' + str(a_max) + 'xx'
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
        
    def get_folder(self):
        folders = (None, '')
        # all folders within enc table
        return folders
        
    def get_table(self):
        tables = (None, '')
        # all tables within enc table
        return tables

def build_text_menu():
    #find how to build python menu, will be platform independent
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
        keep_alive=raw_input("Please run:")
        if keep_alive=="1": 
            print("\n Opening cherrytree ...") 
        elif keep_alive=="2":
            print("\n Opening sqlite browser") 
        elif keep_alive=="3":
            print("\n Synchronize directories")
            # dropbox synchronizer
        elif keep_alive=="4":
            print 'generate structure'
        elif keep_alive=="8":
            # running Tkinter GUI
            print 'universal python in ' + args.d
            GUI.build_window(args.d)
        elif str(keep_alive).lower()=="q":
            print("\n Goodbye") 
            keep_alive = False
        elif keep_alive !="":
            print("\n Not Valid Choice Try again") 

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
    col =  ('reg_name', 'file_dir')
    for root, directories, files in os.walk(directory):
        curs_mem.execute(tab_ins.format('"", ' + root))
        i += 1
        # iterate files in directory
        for filename in files:
            fln_val = dw.ins_val.format(i, filename, root, 'date date date',
            get_file_size(root+'/'+filename))
            v = (filename, root)
            # print v
            if val_exist(v, col, 'dirlist', c):
                msg = '---file {0} registered, checking size.'.format(filename)
            else:
                msg = '---file {0} registering.'.format(filename)
            #    c.execute(dw.tab_ins.format(fln_val))
            i += 1
            #print filename
    return c
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="construct h808e")
    parser.add_argument('-c', help='ctb file', type=str, default='')
    parser.add_argument('-d', help='directory', type=str, default='')
    args = parser.parse_args()
    h_e = h808e()
    he = h_e.construct()
    # connect to database
    try:
        conn = sqlite3.connect(args.c)
    except:
        print 'cannot find main db file! > ' + args.c + ' ?'
        # make connection to a temporary database?
        #conn = sqlite3.connect(args.d + 'H808E.ctb')
    # show the text menu
    build_text_menu()
    
    # prepare the insert query
    # insert = 'INSERT INTO veci (hmotne, oblast, uroven) VALUES ({0}, "{1}", {2});'
    # browse encyklopedia node (en) + subnode (esn), subsubnode (essn)
    
    # for root, directories, files in os.walk(args.d):
        # print '**********'
        # print he.folders
        # print '**********'
        # if not root in he.folders:
            # print 'no corresponding directory found...'
            # continue
        # for filename in files:
            # locate table CTB
            # print 'table read!, chcek if registered'

    for en in he:
        # 1 
        print str(en['code']) + '/' + str(en['level'])
       # print insert.format(en['code'], en['real'], en['level'])
        # conn.execute(insert.format(en['real'], en['code'], en['level']))
        for esn in en['child']:
            print str(esn['code']) + '/' + str(esn['level'])
            for essn in esn['child']:
                print str(essn['code']) + '/' + str(essn['level'])
        break

    # tbl = conn.execute('SELECT * FROM veci;')
