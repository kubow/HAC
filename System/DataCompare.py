import argparse
import sqlite3
import difflib

def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio() #> 0.9

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare two sqlite databases")
    parser.add_argument('-l', help='first file', type=str, default='')
    parser.add_argument('-r', help='second file', type=str, default='')
    args = parser.parse_args()
    
    table_exist = """SELECT EXISTS(
        SELECT 1 FROM sqlite_master 
        WHERE type="table" AND name = "{0}"
    );"""
    
    table_list = """SELECT tbl_name, type 
        FROM sqlite_master 
        WHERE type not LIKE "%index%" 
    ;"""
    list_rows = """SELECT * FROM {0};"""
    fld_content = """SELECT txt FROM node
        WHERE node_id = {0}"""
    
    db_left = sqlite3.connect(args.l)
    l = db_left.cursor()
    db_right = sqlite3.connect(args.r)
    r = db_right.cursor()
    
    for table in l.execute(table_list).fetchall():
        print '/// table {0}'.format(table[0])
        # check if table exist also on the right side
        if not r.execute(table_exist.format(table[0])):
            print 'missing table ' + str(table[0]) + ' (' + args.p + ')'
            # goto next table
            continue
        for row in l.execute(list_rows.format(table[0])):
            print '////// ' + row[1]
            # make mirrored text
            mirror = r.execute(fld_content.format(row[0])).fetchone()
            # compare strings using difflib
            #if row[2] != mirror[0]:
            if similar(row[2], mirror[0]) < 1:
                print similar(row[2], mirror[0])
                # print '--------' + row[1] + '/' + str(similar(row[2], mirror[0])) + '--------'
                print mirror
                print '++++++++++++++++++'
                print row
            # if table == ''
            else:
                print str(similar(row[2], mirror[0]))
        break