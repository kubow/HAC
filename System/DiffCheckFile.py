import argparse
import difflib

def difference(text1, text2):
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
    parser = argparse.ArgumentParser(description="Check difference of two files")
    parser.add_argument('-a', help='First file', type=str, default='')
    parser.add_argument('-b', help='Second file', type=str, default='')
    args = parser.parse_args()
    #read content to variable
    print args.a + '-' + args.b
    with open(args.a, 'r') as f: lines1 = f.read()
    f.close()
    with open(args.b, 'r') as f: lines2 = f.read()
    f.close()
    difference(args.a, args.b)
    #difference(lines1, lines2)