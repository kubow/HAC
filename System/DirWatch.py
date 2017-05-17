""" Determine new files in directory (not logged to h808e)
1st argument - path to directory (name of dir = key)
2nd argument - table to hold list information
"""
import os
import time
import argparse
import sqlite3
# from local project
import log


class dirWatch(object):
    """SQL to command directory warcher"""
    exist = """SELECT EXISTS(
        SELECT 1 FROM {0}
        WHERE {1}
    );"""
    table_exist = exist.format('sqlite_master', 
    'type="table" AND name = "{0}"')
    tab_ddl = 'CREATE TABLE {0} ({1});'
    tab_fld = """ ID int,
    reg_name text,
    file_dir int, --boolean
    last_change text, --date
    size int
    """
    table_create = tab_ddl.format('dirlist', tab_fld)
    tab_ins = 'INSERT INTO dirlist VALUES ({0});'
    ins_val = '"{0}", "{1}", "{2}", "{3}", {4}'
    
def get_file_size(_file):
    # return file size in kilobytes
    return '{0:.2f}'.format(os.path.getsize(_file)/1024)
    
def touch_file(path):
    with open(path, 'a'):
        os.utime(path, None)

def tab_exist(t, c):
    if not c.execute(dw.table_exist.format(t)).fetchone()[0]:
        return False
    else:
        return True
        
def val_exist(v, col, t, c):
    # 1 build where condition
    where = ''
    if isinstance(v, str) and isinstance(col, str):
        where = col + ' = "' + v + '"'
    elif isinstance(v, tuple) and isinstance(col, tuple):
        for i in range(len(col)):
            where += col[i] + ' = "' + v[i] + '" AND '
        where = where[:-5]
        print where
    # 2 build whole sql & execute
    row_exist = dw.exist.format(t, where)
    if not c.execute(row_exist).fetchone()[0]:
        return False
    else:
        return True
    
def walk_dir(directory):
    for root, directories, files in os.walk(directory):
        print root
        for filename in files:
            print filename

def reg_dir(directory, c):
    # register directory within sqlite database
    
    if not tab_exist('dirlist', c):
        c.execute(dw.table_create)
    i = 1
    col =  ('reg_name', 'file_dir')
    for root, directories, files in os.walk(directory):
        # print root
        fld_val = dw.ins_val.format(i, root, '', 'date date date', 0)
        # print fld_val
        # print dw.tab_ins #.format(fld_val)
        if val_exist(root, 'reg_name', 'dirlist', c):
            print 'value already exist...'
        else:
            c.execute(dw.tab_ins.format(fld_val))
        i += 1
        # iterate files in directory
        for filename in files:
            fln_val = dw.ins_val.format(i, filename, root, 'date date date',
            get_file_size(root+'/'+filename))
            v = (filename, root)
            print v
            if val_exist(v, col, 'dirlist', c):
                print 'file exist, check size...'
            else:
                c.execute(dw.tab_ins.format(fln_val))
            i += 1
            #print filename
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Watch dirs/files")
    parser.add_argument('-w', help='Watch directory', type=str, default='')
    parser.add_argument('-l', help='log file', type=str, default='')
    parser.add_argument('-d', help='database file', type=str, default='')
    args = parser.parse_args()
    dw = dirWatch()
    if os.path.isfile(args.l):
        # found log file, need to check for database file
        print '-----------------'
        if os.path.isdir(args.w):
            flag = True
            conn = sqlite3.connect(args.d)
            c = conn.cursor()
            while flag:
                log.file_write(args.l, "watch", 
                "Searching for new files... in {0}".format(args.w))
                start_time = time.clock()
                # walk_dir(args.w)
                flag = reg_dir(args.w, c)
                conn.commit()
                flag = False
                elapsed_time = time.clock() - start_time
                print "Time elapsed: {} seconds".format(elapsed_time)
        else:
            log.file_write(args.l, "watch",
            'please submit proper directory - {0}'.format(args.w))
            flag = False
    else:
        # cannot log because of missing log file
        basedir = os.path.dirname(args.l)
        if not os.path.exists(os.path.dirname(basedir)):
            print 'creating ' + basedir
            os.makedirs(basedir)
        touch_file(args.l)
        print "cannot find log file, please run once more..."
        flag = False

    
