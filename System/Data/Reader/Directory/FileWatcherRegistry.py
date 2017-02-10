import os
import sys
# Determine if passed parguments for running over a directory
if len(sys.argv) > 1:
    # might chceck for trailing \
    directory = sys.argv[1:2]
    base_dir = sys.argv[2:]
else:
    # os.getcwd() - not applicable if being called from elsewhere
    if 'win' in os.name.lower():
        base_dir = 'C:\_Run'
    elif 'ux' in os.name.lower():
        base_dir = '/home/kubow/Dokumenty'
    directory = os.path.dirname(os.path.realpath(__file__))
print 'exporting for new files in directory :' 
print directory[0]

for root, directories, files in os.walk(directory[0]):
    print root
    for filename in files:
        print filename
