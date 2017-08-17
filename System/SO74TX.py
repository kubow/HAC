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
import datetime
import xml.etree.ElementTree as xml_tree
import lxml.html
import feedparser
import requests
from xml.dom.minidom import parseString

try:
    from bs4 import BeautifulSoup
except:
    print 'using alternative html parser'
import HTMLParser
# sys.setdefaultencoding('utf-8')
from Template import HTML, SQL
from OS74 import FileSystemObject, CurrentPlatform
from DB74 import DataBaseObject

class WebContent(HTMLParser.HTMLParser):
    """http://stackoverflow.com/questions/3276040/how-can-i-use-the-python-htmlparser-library-to-extract-data-from-a-specific-div """

    def __init__(self, url):
        HTMLParser.HTMLParser.__init__(self)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        self.recording = 0
        self.data = []
        self.div = None
        self.url = url
        self.easier = True  # found BS4
        self.div_text = ''

    def handle_starttag(self, tag, attributes):  # , tag_type, tag_name):
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

    def parse_html_text(self, html_text):
        if is_html_text(html_text):
            if self.easier:
                soup = BeautifulSoup(html_text, 'lxml')
                return soup
            else:
                # TODO: same logic as with beautiful soup
                p = WebContent()
                oups = p.feed(html_text)
                p.close()
                return oups

    def process_url(self, tag_type='', tag_name=''):
        content = None
        if 'id' in str(tag_type).lower():
            tag_type = 'id'
        elif 'class' in str(tag_type).lower():
            tag_type = 'class'
        done = False
        try:
            if 'file:' in self.url:
                content = FileSystemObject(self.url.split('///')[-1]).read_object()
                parsed_content = self.parse_html_text(content)
                done = True
            else:
                html = requests.get(self.url, timeout=(10, 5), headers=self.headers)
                parsed_content = self.parse_html_text(html.content)
                done = True
            if self.easier:
                if not tag_name:
                    self.div = parsed_content.find('body')
                    self.div_text = parsed_content.find('body').text
                else:
                    self.div = parsed_content.find('div', {tag_type: tag_name})
                    self.div_text = parsed_content.find('div', {tag_type: tag_name}).text
            else:
                # TODO: same logic as with beautiful soup
                print 'HTML parser not working now...'
        except HTMLParser.HTMLParseError, e:
            print '---cannot fetch address {0}, ({1})'.format(self.url, e)
        except:
            print '---some else error occurred: ' + self.url
            if done:
                if content:
                    self.div = str(content)
                    print '---cannot parse content of {0} ({1})'.format(self.url, content)
                elif html:
                    self.div = str(html.content)
            else:
                self.div = None

    def write_web_content_to_file(self, file_path, heading, log=False):
        if self.div:
            print 'creating ' + file_path + ' from: ' + self.url
            try:
                FileSystemObject(file_path).object_write(HTML.skelet_titled.format(heading.encode('utf-8'),
                                                                                 self.div.encode('utf-8')), 'w+')
                if log:
                    self.log_to_database(log, heading)
            except:
                print '!!! cannot write/log content'
        else:
            print 'no content parsed from: ' + self.url

    def log_to_database(self, db_path, heading):
        user, domain = CurrentPlatform().get_current_settings()
        time_stamp = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        tag_content = self.div_text.encode('utf-8').replace('\n\n\n\n', '\n').replace('\n\n', '\n')
        # table structure
        table_def = 'Log (Connection, CPName, Report, LogDate, User, Domain)'
        values_template = '"{0}", "{1}", "{2}", "{3}", "{4}", "{5}"'
        table_values = values_template.format(heading.encode('utf-8'), 0, tag_content, time_stamp, user, domain)
        sql = SQL.insert.format(table_def, table_values)
        DataBaseObject(db_path).log_to_database('Log', sql)


class RssContent(object):
    def __init__(self, rss_url):
        self.url = rss_url
        thefeed = feedparser.parse(self.url)
        self.title = thefeed.feed.get("title", "")
        self.link = thefeed.feed.get("link", "")
        self.desc = thefeed.feed.get("description", "")
        self.pub = thefeed.feed.get("published", "")
        # self.pub_pars = thefeed.feed.get("published_parsed",
        #                   thefeed.feed.published_parsed)
        inner_text = ''
        for thefeedentry in thefeed.entries:
            inner_text += "\n__________"
            inner_text += thefeedentry.get("guid", "")
            inner_text += thefeedentry.get("title", "")
            inner_text += thefeedentry.get("link", "")
            inner_text += thefeedentry.get("description", "")
            inner_text += "\n__________"

            # Parsing Namespaces
            for thefeednamespace in thefeed.namespaces:
                if (thefeednamespace == "media"):
                    # parse for Yahoo Media
                    inner_text += "Media"
                    allmediacontent = thefeedentry.get("media_content", "")
                    for themediacontent in allmediacontent:
                        inner_text += themediacontent["url"]
                        inner_text += themediacontent["height"]
                        inner_text += themediacontent["width"]
        self.div = inner_text

    def write_rss_content_to_file(self, file_path, heading):
        if self.div:
            print 'creating ' + file_path + ' from: ' + self.url
            FileSystemObject(file_path).file_refresh(HTML.skelet_titled.format(heading.encode('utf-8'),
                                                                               self.div.encode('utf-8')))
            log_path = FileSystemObject(file_path).get_another_directory_file('logfile.sqlite')

            # self.log_to_database(log_path, heading)
        else:
            print 'no content parsed from: ' + self.url


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


def replace_crlf_lf(block_text):
    # replace windows line endings with linux line endings
    if '\r\n' in block_text:
        block_text.replace('\r\n', '\n')
    else:
        print 'this text does not have any windows line endings, passing ...'
    return block_text


def replace_lf_crlf(block_text):
    # replace linux line endings with windows line endings
    if re.search('\r?\n'):
        block_text = re.sub('\r?\n', '\r\n', block_text)
    else:
        print 'this text does not have any linux line endings, passing ...'
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
    if text:
        if lxml.html.fromstring(text).find('.//*') is not None:
            return True
        else:
            return False
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
        f = open(file_name, 'a')
        line = 2
        # TODO: check if header corresponds
    else:
        f = open(file_name, 'a+')
        line = 1
    # write time series and header
    for actime, vals in values.iteritems():
        row = ''
        if line == 1:
            for d, v in vals.iteritems():
                row += str(d) + ','
            row = 'datetime, ' + row
            f.write(row + '\n')
        row = str(actime) + ','
        for d, v in vals.iteritems():
            row += str(v) + ','
        f.write(row + '\n')
        line += 1
    f.close()


def readCSV(csvfile):
    """read value from csv file
    return in dictionary"""
    try:
        fileobj = open(csvfile, 'r')
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
                        flds.append('val_' + str(i))
                        vels.append(hd[i].strip())
                        values['val_' + str(i)] = 0
                val += 1
            else:
                for fld in flds:
                    idx = int(fld.split('_')[-1])
                    values[fld] = int(values[fld]) + int(hd[idx])
                val += 1
        for field, sum_vals in values.iteritems():
            values[field] = sum_vals / val
            # get index of field - change to proper list
            velocities[vels[flds.index(field)]] = sum_vals / val
        timestamps[timestamp] = velocities
        return timestamps
    except Exception as ex:
        print ex.args[0]
        print 'problem in csv ' + csvfile + ' (line{0})'.format(str(val))
        return None


def readJSON(file):
    print 'file: ' + file
    with open(file, 'r') as fh:
        # first = next(fh).decode()
        first = fh.readline()
        print 'got first line' + first
        print '*****************'
        fh.seek(-512, 2)
        # last = fh.readlines()
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
        # print get_ts
        json = open(location + col + '.json', 'w')
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
    html_text = ''
    h = HTML()
    for element in xml_tree.fromstring(xml_text)._children:
        if element.text is not None:
            if len(element.attrib) > 0:
                if 'scale' in element:
                    if element.attrib['scale'] == 'h1':
                        html_text += h.heading.format('1', element.text.encode('utf8'))
                    elif element.attrib['scale'] == 'h2':
                        html_text += h.heading.format('2', element.text.encode('utf8'))
                    else:
                        html_text += h.paragraph.format('2', element.text.encode('utf8'))
                else:
                    html_text += h.paragraph.format(element.text.encode('utf8'))
            else:
                for par_text in element.text.split('\n'):
                    html_text += h.paragraph.format(par_text.encode('utf8'))
        else:
            html_text += h.paragraph.format('... no content for this part ...\n')
    return html_text


def htm_to_plain_txt(htm_txt):
    soup = BeautifulSoup(htm_txt, 'html.parser')
    # return soup.get_text()
    return soup.body.get_text()


def test_utf_special_characters():
    print os.getcwd()
    veta = u'Žluťoučký kůň pěl ďábelské ódy.'
    print veta
    logger.file_write('aaa.log', 'temp', veta)


def similar(seq1, seq2):
    try:
        return difflib.SequenceMatcher(a=seq1.lower(),
                                       b=seq2.lower()).ratio()  # > 0.9
    except:
        return difflib.SequenceMatcher(a=str(seq1).lower(),
                                       b=str(seq2).lower()).ratio()  # > 0.9


if __name__ == '__main__':

    import DV72
    from log import Log

    parser = argparse.ArgumentParser(description='Text proccess')
    parser.add_argument('-i', help='Input file/dir', type=str, default='')
    parser.add_argument('-o', help='Output file/dir', type=str, default='')
    parser.add_argument('-m', help='Mode/Logic', type=str, default='')
    parser.add_argument('-l', help='Logfile', type=str, default='')
    args = parser.parse_args()

    logger = Log(args.l, args.i + ' + ' + args.o, __file__, True)

    if os.path.isfile(args.i):
        create_file_if_neccesary(args.o)
        export_text_to(args.o, replace_line_endings(load_text_from(args.i)))
    elif os.path.isdir(args.i):
        for filename in os.listdir(args.i):
            file_path = args.i + '/' + filename
            print file_path
            if 'lin' in args.l:
                export_text_to(args.o + '/' + filename, replace_crlf_lf(load_text_from(file_path)))
            elif 'win' in args.l:
                export_text_to(args.o + '/' + filename, replace_lf_crlf(load_text_from(file_path)))
            else:
                export_text_to(args.o + '/' + filename, replace_lf_crlf(load_text_from(file_path)))
    else:
        print args.i + ' -> input file/dir does not exist ...'
