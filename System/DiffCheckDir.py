import os
import argparse

def difference(dir1, dir2):
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
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check difference of two dirs")
    parser.add_argument('-a', help='First directory', type=str, default='')
    parser.add_argument('-b', help='Second directory', type=str, default='')
    args = parser.parse_args()
    
    difference(args.a, args.b)