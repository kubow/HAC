# -*- coding: utf-8 -*-
import os
import argparse
import sqlite3
#sys.setdefaultencoding('utf-8')

class h808e(object):
    
    # folders = property(self.get_folder)
    # print 'aaaaaaaaaaaaaaaaaaaaaaa'
    # tables = property(self.get_table)
    
    def construct(self):
        """constructor of h808e
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
        folders = (Null, )
        # all folders within enc table
        return folders
        
    def get_table(self):
        tables = (Null, )
        # all tables within enc table
        return tables
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="construct h808e")
    parser.add_argument('-c', help='ctb file', type=str, default='')
    parser.add_argument('-d', help='directory', type=str, default='')
    args = parser.parse_args()
    h_e = h808e()
    print '------------------------'
    he = h_e.construct()
    print he
    print '---------------------------------'
    # connect to database
    try:
        conn = sqlite3.connect('/home/kubow/Dokumenty/H808E.ctb')
    except:
        conn = sqlite3.connect('c:/_Run/H808E.ctb')
    # prepare the insert query
    # insert = 'INSERT INTO veci (hmotne, oblast, uroven) VALUES ({0}, "{1}", {2});'
    # browse encyklopedia node (en) + subnode (esn), subsubnode (essn)

    for root, directories, files in os.walk(args.d):
        print '**********'
        print he.folders
        print '**********'
        if not root in he.folders:
            print 'no corresponding directory found...'
            continue
        for filename in files:
            # locate table CTB
            print 'table read!, chcek if registered'

    for en in he:
        # 1 
        print str(en['code']) + '/' + str(en['level'])
        print insert.format(en['code'], en['real'], en['level'])
        # conn.execute(insert.format(en['real'], en['code'], en['level']))
        for esn in en['child']:
            print str(esn['code']) + '/' + str(esn['level'])
            for essn in esn['child']:
                print str(essn['code']) + '/' + str(essn['level'])
        break

    tbl = conn.execute('SELECT * FROM veci;')
