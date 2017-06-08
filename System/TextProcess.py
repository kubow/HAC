# -*- coding: utf-8 -*-
""" Proccessing Text (c) Kube Kubow
replace line endings, load/write text to a file
compare text simrality
XML > HTML
"""
import re
import os
import sys
from xml.dom.minidom import parseString
import xml.etree.ElementTree as xml_tree
from bs4 import BeautifulSoup
# sys.setdefaultencoding('utf-8')

def replace_line_endings(block_text):
    # replace double carriage return with tildos
    block_text=re.sub(r'\n\n', r'~~~', block_text)
    # then remove dash followed with carriage return
    block_text=re.sub(r'-\n', r'', block_text)
    # then replace all remaining carriage returns with space
    block_text=re.sub(r'\n', r' ', block_text)
    # and finally put back new line characters
    block_text=re.sub(r'~~~', r'\n\n', block_text)
    return block
    
def filter_lines(textfile, with_filter):
    stream = ''
    for line in textfile:
        if re.search('Dumpfile name', line) or re.search('DUMP is complete', line) or re.search('Dump phase number 1 completed', line):
            stream += line
    return stream

def load_text_from(filename):
    with open(filename, 'rb') as input_file:
        text=input_file.read()
        # for m in re.findall(r'\n\n', whole_data):
            # print m
    return text

def create_file_if_neccesary(file)
    if os.isfile(file):
        print ' -> '+file+' - exists ...'
    else:
        print ' -> '+file+' - creating new file ...'
        with open(file, 'a'):
            os.utime(file, None)
    
def export_text_to(filename, text):
    with open(filename, 'w+') as output_file:
        output_file.write(text)

def xml_to_html(xml_text):
    import Template
    html_text = ''
    c = Template.HTML()
    e = xml_tree.fromstring(xml_text)
    for element in e._children:
        if element.text <> None:
            if len(element.attrib) > 0:
                if element.attrib['scale'] == 'h1':
                    html_text += c.heading.format('1', element.text.encode('utf8'))
                elif element.attrib['scale'] == 'h2':
                    html_text += c.heading.format('2', element.text.encode('utf8'))
                else:
                    html_text += c.paragraph.format('2', element.text.encode('utf8'))
            else:
                for par_text in element.text.split('\n'):
                    html_text += c.paragraph.format(par_text.encode('utf8'))
        else:
            html_text += c.paragraph.format('... no content for this part ...\n')
    return html_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Text proccess")
    parser.add_argument('-i', help='Input file', type=str, default='')
    parser.add_argument('-o', help='Output file', type=str, default='')
    parser.add_argument('-l', help='Logic', type=str, default='')
    args = parser.parse_args()
    
    if os.isfile(args.i):
        create_file_if_neccesary(args.o)
        export_text_to(args.o, replace_line_endings(load_text_from(args.i)))
    else:
        print args.i+' -> input file does not exist ...'
