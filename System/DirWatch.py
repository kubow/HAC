""" Determine new files in directory (not logged to h808e)
1st argument - path to directory (name of dir = key)
2nd argument - table to hold list information
"""
import os
import sys

if sys.argv > 2:
    directory = sys.argv[1]
    table = sys.argv[2]
else:
    print 'missing arguments ...'
    directory = os.path.dirname(os.path.realpath(__file__))
    break

for root, directories, files in os.walk(directory):
    print root
    for filename in files:
        print filename
