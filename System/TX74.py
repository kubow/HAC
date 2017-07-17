# -*- coding: utf-8 -*-
""" Proccessing Text (c) Kube Kubow
replace line endings, load/write text to a file
compare text simrality
XML > HTML
"""
import re
import os
import argparse
import difflib
import xml.etree.ElementTree as xml_tree
import lxml.html
import requests
from xml.dom.minidom import parseString
try:
    from bs4 import BeautifulSoup
except:
    print 'using alternative html parser'
import HTMLParser

import DV72
from Template import HTML, SQL
import log
# sys.setdefaultencoding('utf-8')


class WebContent(HTMLParser.HTMLParser):
    """http://stackoverflow.com/questions/3276040/how-can-i-use-the-python-htmlparser-library-to-extract-data-from-a-specific-div """
    def __init__(self, url):
        HTMLParser.HTMLParser.__init__(self)
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        self.recording = 0
        self.data = []
        self.url = url
        self.easier = True # found BS4

    def handle_starttag(self, tag, attributes): #, tag_type, tag_name):
        if tag != 'div':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if name == self.start_tag_type and value == self.start_tag_name:
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)
            
    def procces_url(self, tag_type, tag_name):
        if 'id' in str(tag_type).lower():
            tag_type = 'id'
        else:
            tag_type = 'class'
        try:
            html = requests.get(self.url, timeout=(10, 5))
            if is_html_text(html.content):
                if self.easier:
                    soup = BeautifulSoup(html.content, "lxml")
                    self.div = soup.find('div', {tag_type: tag_name})
                else:
                    p = WebContent()
                    self.div = p.feed(html.content)
                    p.close()

            else:
                print 'cannot parse content of {0} ({1})'.format(self.url, html.content)
        except HTMLParser.HTMLParseError, e:
            print 'cannot fetch address {0}, ({1})'.format(self.url, e)
        except:
            print 'some else error occurred: ' + self.url
            self.div = None
        

def replace_line_endings(block_text):
    # replace double carriage return with tildos
    block_text = re.sub(r'\n\n', r'~~~', block_text)
    # then remove dash followed with carriage return
    block_text = re.sub(r'-\n', r'', block_text)
    # then replace all remaining carriage returns with space
    block_text = re.sub(r'\n', r' ', block_text)
    # and finally put back new line characters
    block_text = re.sub(r'~~~', r'\n\n', block_text)
    return block_text

def trim_line_last_chars(filename):
    new_line = []
    for line in load_text_from(filename):
        new_line.append(line[:-2])
    return new_line

def filter_lines(textfile, with_filter):
    stream = ''
    for line in textfile:
        if re.search('Dumpfile name', line) or re.search('DUMP is complete', line) or re.search(
                'Dump phase number 1 completed', line):
            stream += line
    return stream

def is_html_text(text):
    if lxml.html.fromstring(text).find('.//*') is not None:
        return True
    else:
        return False

def load_text_from(filename):
    with open(filename, 'rb') as input_file:
        text = input_file.read()
        # for m in re.findall(r'\n\n', whole_data):
        # print m
    return text
    
    
def export_text_to(filename, text):
    with open(filename, 'w+') as output_file:
        output_file.write(text)    
    

def writeCSV(file_name, values, timestamp, device):
    """write a CSV file
    values - in dictionary
    timestamp of exact time measured
    device - which perform data read"""
    if os.path.exists(file_name):
        f = open(file_name, "a")
        line = 2
        # TODO: check if header corresponds
    else:
        f = open(file_name, "a+")
        line = 1
    # write time series and header
    for actime, vals in values.iteritems():
        row = ''
        if line == 1:
            for d, v in vals.iteritems():
                row += str(d) + ','
            row = 'datetime, ' + row
            f.write(row + "\n")
        row = str(actime) + ','
        for d, v in vals.iteritems():
            row += str(v) + ','
        f.write(row+"\n")
        line += 1
    f.close()

def readCSV(csvfile):
    """read value from csv file
    return in dictionary"""
    try:
        fileobj = open(csvfile,'r')
        lines = fileobj.readlines()
        timestamp = DV72.get_time_from_file(csvfile)
        fileobj.close()
        # load field names as variables
        val = 0
        timestamps = {}
        flds = []  # field number
        vels = []  # velocities
        values = {}
        velocities = {}
        # load values to dictionary
        for row in lines:
            if not row:
                continue
            hd = row.split(',')
            if val == 0:
                # various columns save
                for i in range(len(hd)):
                    if hd[i] not in ('datetime', None, '\n'):
                        flds.append('val_'+str(i))
                        vels.append(hd[i].strip())
                        values['val_'+str(i)] = 0
                val += 1
            else:
                for fld in flds:
                    idx = int(fld.split('_')[-1])
                    values[fld] = int(values[fld]) + int(hd[idx])
                val += 1
        for field, sum_vals in values.iteritems():
            values[field] = sum_vals/val
            # get index of field - change to proper list
            velocities[vels[flds.index(field)]] = sum_vals/val
        timestamps[timestamp] = velocities
        return timestamps
    except Exception as ex:
        print ex.args[0]
        print 'problem in csv ' + csvfile + ' (line{0})'.format(str(val))
        return None

def readJSON(file):
    print 'file: ' + file
    with open(file, 'r') as fh:
        #first = next(fh).decode()
        first = fh.readline()
        print 'got first line' + first
        print '*****************'
        fh.seek(-512, 2)
        #last = fh.readlines()
        last = fh.readlines()[-1].decode()
    return (first, last)

def writeJSON(location, cols, c):
    # print cols
    columns = cols.split(',')
    for column in columns:
        col = column.split(' ')[0]
        # avoid some column names
        if col in ('timestamp', None) or not col:
            continue
        # determine if column contains data
        loc = c.execute(SQL.group_select.format(col, col, col)).fetchall()
        col_data = '(%s)' % ', '.join(map(str, loc))
        bypass = column + ' : ' + col_data
        if 'None' in col_data:
            print bypass + ' - bypassing, found None data'
            continue
        print bypass
        # prepare JSON file to HTML graphs
        print '-------------------'
        if os.path.isfile(location + col + '.json'):
            print readJSON(location + col + '.json')
        else:
            print location + col + '/.json'
        print '-------------------'
        get_ts = SQL.column_select.format('timestamp, ' + col, 'measured')
        #print get_ts
        json = open(location + col + '.json','w')
        json.write('[')
        # fetch dataset
        for ts in c.execute(get_ts).fetchall():
            # write values
            print ts
            json.write('[' + ts[0] + ',' + str(ts[1]) + '],\n')
        
        # finish JSON file
        json.write(']')


def file_content_difference(file1, file2):
    diff = difflib.unified_diff(fromfile=file1, tofile=file2, lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    removed = [line[1:] for line in lines if line[0] == '-']

    print 'additions, ignoring position'
    for line in added:
        if line not in removed:
            print line

def create_file_if_neccesary(filename):
    if os.path.isfile(filename):
        print ' -> ' + filename + ' - exists ...'
    else:
        print ' -> ' + filename + ' - creating new file ...'
        with open(filename, 'a'):
            os.utime(filename, None)


def xml_to_html(xml_text):
    import Template
    html_text = ''
    c = Template.HTML()
    for element in xml_tree.fromstring(xml_text)._children:
        if element.text is not None:
            if len(element.attrib) > 0:
                if 'scale' in element:
                    if element.attrib['scale'] == 'h1':
                        html_text += HTML.heading.format('1', element.text.encode('utf8'))
                    elif element.attrib['scale'] == 'h2':
                        html_text += HTML.heading.format('2', element.text.encode('utf8'))
                    else:
                        html_text += HTML.paragraph.format('2', element.text.encode('utf8'))
                else:
                    html_text += HTML.paragraph.format(element.text.encode('utf8'))
            else:
                for par_text in element.text.split('\n'):
                    html_text += HTML.paragraph.format(par_text.encode('utf8'))
        else:
            html_text += HTML.paragraph.format('... no content for this part ...\n')
    return html_text


def htm_to_plain_txt(htm_txt):
    soup = BeautifulSoup(htm_txt, 'html.parser')
    # return soup.get_text()
    return soup.body.get_text()
    
    
def test_utf_special_characters():
    print os.getcwd()
    veta=u"Žluťoučký kůň pěl ďábelské ódy."
    print veta
    log.file_write("aaa.log", "temp", veta)
    
    
def similar(seq1, seq2):
    try:
        return difflib.SequenceMatcher(a=seq1.lower(), 
        b=seq2.lower()).ratio() #> 0.9
    except:
        return difflib.SequenceMatcher(a=str(seq1).lower(), 
        b=str(seq2).lower()).ratio() #> 0.9

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Text proccess")
    parser.add_argument('-i', help='Input file', type=str, default='')
    parser.add_argument('-o', help='Output file', type=str, default='')
    parser.add_argument('-l', help='Logic', type=str, default='')
    args = parser.parse_args()

    if os.path.isfile(args.i):
        create_file_if_neccesary(args.o)
        export_text_to(args.o, replace_line_endings(load_text_from(args.i)))
    else:
        print args.i + ' -> input file does not exist ...'