import os
import argparse
import difflib

def diff_dir(dir1, dir2):
    found = True
    for root, directories, files in os.walk(dir1):
        corr = root.replace(dir1, dir2)
        #print root + ' :x: ' + corr
        if not os.path.isdir(corr):
            print 'not found ' + dir2 + '/' + root
            continue
        for filename in files:
            #print filename
            corr_file = filename.replace(dir1, dir2)
            if not os.path.exists(corr_file):
                #print root + ' :x: ' + corr
                #print 'not found ' + filename
                found = False
        
def diff_file(text1, text2):
    diff = difflib.unified_diff(lines1, lines2,
    fromfile=text1, tofile=text2, lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    removed = [line[1:] for line in lines if line[0] == '-']

    print 'additions:'
    #for line in added:
        #print line
    print 'additions, ignoring position'
    for line in added:
        if line not in removed:
            print line

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check difference dirs/files")
    parser.add_argument('-a', help='Left directory/file', type=str, default='')
    parser.add_argument('-b', help='Right directory/file', type=str, default='')
    args = parser.parse_args()
    if os.path.isfile(args.a) and os.path.isfile(args.b):
        print 'comparing files'
        #with open(args.a, 'r') as f: lines1 = f.read()
        #f.close()
        #with open(args.b, 'r') as f: lines2 = f.read()
        #f.close()
        #difference(lines1, lines2)
        diff_file(args.a, args.b)
    elif os.path.isdir(args.a) and os.path.isdir(args.b):
        print 'comparing directories'
        diff_dir(args.a, args.b)
    else:
        print args.a + '-' + args.b + ' (not a directory/file)!!!'
