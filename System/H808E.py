# -*- coding: utf-8 -*-
import os
import sqlite3
#sys.setdefaultencoding('utf-8')

def conh808e():
    """constructor of h808e
    in dictionary..main structure:
    key code - number code to define area
    key name - names will be filled after matching
    key child - reference all children
    will be a module after.."""
    h808e = []
    # only nodes from 400 to 700
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
    
he = conh808e()
print he
print '---------------------------------'
# connect to database
conn = sqlite3.connect('/home/kubow/Dokumenty/H808E.ctb')
# prepare the insert query
insert = 'INSERT INTO veci (hmotne, oblast, uroven) VALUES ({0}, "{1}", {2});'
# browse encyklopedia node (en) + subnode (esn), subsubnode (essn)
for en in he:
    # 1 
    print str(en['code']) + '/' + str(en['level'])
    print insert.format(en['code'], en['real'], en['level'])
    conn.execute(insert.format(en['real'], en['code'], en['level']))
    for esn in en['child']:
        print str(esn['code']) + '/' + str(esn['level'])
        for essn in esn['child']:
            print str(essn['code']) + '/' + str(essn['level'])
    break

tbl = conn.execute('SELECT * FROM veci;')
