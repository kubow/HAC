import argparse
import difflib

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check difference of two files")
    parser.add_argument('-a', help='First file', type=str, default='')
    parser.add_argument('-b', help='Second file', type=str, default='')
    args = parser.parse_args()
    
    print 'a'
    with open(args.a, 'r') as f: lines1 = f.read()
    with open(args.b, 'r') as f: lines2 = f.read()

    diff = difflib.unified_diff(lines1, lines2, fromfile=args.a, tofile=args.b, lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    removed = [line[1:] for line in lines if line[0] == '-']

    print 'additions:'
    for line in added:
        print line
    print 'additions, ignoring position'
    for line in added:
        if line not in removed:
            print line