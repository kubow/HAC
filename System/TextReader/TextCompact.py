""" remove extra line breaks within text file
running with command line arguments:
input_file - with path
output_file - with path
"""
import re
import os
import sys
print 'running in directory: '+os.getcwd()
try:
    filename_in=sys.argv[1]
    filename_out=sys.argv[2]
    print filename_in+' -> '+filename_out 
    # might chceck for trailing \
except:
    raise ValueError('not submited files to read and export')

with open(filename_in, 'rb') as input_file:
	whole_data=input_file.read()
	# for m in re.findall(r'\n\n', whole_data):
		# print m
	# first replace double carriage return with tildos
	output=re.sub(r'\n\n', r'~~~', whole_data)
	# then remove dash followed with carriage return
	output=re.sub(r'-\n', r'', output)
	# then replace all remaining carriage returns with space
	output=re.sub(r'\n', r' ', output)
	# and finally put back new line characters
	output=re.sub(r'~~~', r'\n\n', output)
	
	with open(filename_out, 'w+') as output_file:
		output_file.write(output)
