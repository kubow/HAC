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
# from xml.dom.minidom import parseString

try:
    from bs4 import BeautifulSoup
except ImportError:
    print 'using alternative html parser'
finally:
    import HTMLParser
# sys.setdefaultencoding('utf-8')
try:
    import pandas
except ImportError:
    print 'using alternative csv parser'
finally:
    import csv

from Template import HTML, SQL
from OS74 import FileSystemObject, CurrentPlatform
from SO74DB import DataBaseObject


class WebContent(HTMLParser.HTMLParser):
    """http://stackoverflow.com/questions/3276040/how-can-i-use-the-python-htmlparser-library-to-extract-data-from-a-specific-div"""

    def __init__(self, url, log_file=''):
        HTMLParser.HTMLParser.__init__(self)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        self.recording = 0
        self.data = []
        self.log_file = log_file
        self.url = url
        self.easier = True  # found BS4
        self.div = None
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
                content = FileSystemObject(self.url.split('///')[-1]).object_read()
                parsed_content = self.parse_html_text(content)
                done = True
            else:
                html = requests.get(self.url, timeout=(10, 5), headers=self.headers)
                parsed_content = self.parse_html_text(html.content)
                done = True
            self.div = ''
            self.div_text = ''
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
                self.div = ''
                self.div_text = ''

    def write_web_content_to_file(self, file_path, heading, log_file=''):
        if self.div:
            print 'creating ' + file_path + ' from: ' + self.url
            try:
                FileSystemObject(file_path).object_write(HTML.skelet_titled.format(heading.encode('utf-8'),
                                                                                 self.div.encode('utf-8')), 'w+')
            except:
                FileSystemObject(file_path).object_write(HTML.skelet_titled.format(heading.encode('utf-8'),
                                                                                 'cannot get text/bad char'), 'w+')
            if log_file:
                self.log_to_database(log_file.replace('.log', '.sqlite'), heading)
        else:
            print 'no content parsed from: ' + self.url

    def log_to_database(self, db_path, heading):
        user, domain = CurrentPlatform().get_username_domain()
        time_stamp = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        try:
            tag_content = self.div_text.encode('utf-8').replace('\n\n\n\n', '\n').replace('\n\n', '\n')
        except:
            tag_content = 'cannot catch div text...'
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

            
class CsvContent(object):
    def __init__(self, file_name, write=False, content='', date_format='%Y/%m/%d %H:%M:%S'):
        self.path = file_name
        self.time_stamp = self.get_time_from_file(date_format)
        self.read_success = False
        if not write:
            self.content = self.csv_format()
        else:
            self.write(content)

    def archive(self, folder):
        FileSystemObject(self.path).move_file_to(folder)

    def write(self, content='', device=''):
        """write a CSV file
        values - in dictionary
        timestamp of exact time measured
        device - which perform data read"""
        fs = FileSystemObject(self.path)
        if fs.exist:
            f = open(self.path, 'a')
            line = 2
            # TODO: check if header corresponds
        else:
            f = open(self.path, 'a+')
            line = 1
        # write time series and header
        if not isinstance(content, dict):
            print 'no proper content, skipping'
            return
        for ac_time, vals in content.iteritems():
            row = ''
            if line == 1:
                for d, v in vals.iteritems():
                    row += str(d) + ','
                row = 'datetime, ' + row
                f.write(row + '\n')
            row = str(ac_time) + ','
            for d, v in vals.iteritems():
                row += str(v) + ','
            f.write(row + '\n')
            line += 1
        f.close()

    def csv_format(self, separator=',', first_column_date=True):
        """read value from csv file
            return in dictionary"""
        values = {}
        try:
            # load field names as variables
            csv_object = pandas.read_csv(self.path, error_bad_lines=False)  # , parse_dates=True, index_col=0, header=0)
            for column in csv_object.describe().iteritems():
                if 'unnamed' in column[0].lower():
                    continue
                for statistic in column[1].iteritems():
                    if 'mean' in statistic[0]:
                        values[column[0]] = statistic[1]
                        break
            self.read_success = True
            return values
        except Exception as ex:
            print 'problem in csv ' + self.path + ' : ' + ex.args[0]
            return None

    def get_time_from_file(self, date_format):
        """build a date-time stamp from file name
        ... presuming structure <YYYYMMDD_hhmm>"""
        file_name = self.path.replace('\\', '/').split('/')[-1]
        not_csv = file_name.split('.')[0]
        file_date = not_csv.split('_')[0]
        file_time = not_csv.split('_')[1]
        file_year = int(file_date[:4])
        file_month = int(file_date[4:6])
        file_day = int(file_date[6:])
        file_hour = int(file_time[:2])
        file_minute = int(file_time[2:])
        return datetime.datetime(file_year, file_month, file_day, file_hour, file_minute, 0).strftime(date_format)


class JsonContent(object):
    def __init__(self, location, write=False):
        self.path = location
        self.json_skeleton = '[\n{0}\n]'
        self.json_row = '[{0}, {1}],\n'
        if not write:
            self.content = self.json_format()
        else:
            self.process()

    def process(self):
        fs = FileSystemObject(self.path)
        for database in fs.object_read(filter='sqlite').iterkeys():
            db = DataBaseObject(FileSystemObject(self.path).append_file(database))
            for velocity in db.object_structure('measured'):
                if 'timestamp' in velocity or 'device' in velocity or not velocity:
                    continue
                velocity_name = velocity.split(' ')[0]
                if not db.return_one(SQL.measured_column_count.format(velocity_name, velocity_name, velocity_name))[0]:
                    continue  # determine if column contains data
                velocity_values = {}
                for value in db.return_many(SQL.column_select.format('timestamp, ' + velocity_name, 'measured')):
                    velocity_values[value[0]] = value[1]
                self.write(fs.append_file(velocity_name + '.json'), velocity_values)


    def json_format(self):
        print 'file: ' + self.path
        with open(self.path, 'r') as fh:
            # first = next(fh).decode()
            first = fh.readline()
            print 'got first line' + first
            print '*****************'
            fh.seek(-512, 2)
            # last = fh.readlines()
            last = fh.readlines()[-1].decode()
        return first, last

    def write(self, file_name,  content=''):
        json_file = FileSystemObject(file_name)
        final_content = ''
        for record in content:
            final_content += self.json_row.format(record, content[record])
        if json_file.exist:
            if JsonContent(file_name).json_format():
                final_content = 'read_whole_file' + final_content
                print 'implement appending .. not now yet'
        json_file.object_write(self.json_skeleton.format(final_content))


class TextContent(object):
    def __init__(self, block_text):
        self.block_text = block_text

    def replace_line_endings(self):
        # replace double carriage return with tildos
        block_text = re.sub(r'\n\n', r'~~~', self.block_text)
        # then remove dash followed with carriage return
        block_text = re.sub(r'-\n', r'', block_text)
        # then replace all remaining carriage returns with space
        block_text = re.sub(r'\n', r' ', block_text)
        # and finally put back new line characters
        block_text = re.sub(r'~~~', r'\n\n', block_text)
        return block_text

    def replace_crlf_lf(self):
        # replace windows line endings with linux line endings
        if '\r\n' in self.block_text:
            return self.block_text.replace('\r\n', '\n')
        else:
            print 'this text does not have any windows line endings, passing ...'
            return self.block_text

    def replace_lf_crlf(self):
        # replace linux line endings with windows line endings
        if re.search('\r?\n'):
            return re.sub('\r?\n', '\r\n', self.block_text)
        else:
            print 'this text does not have any linux line endings, passing ...'
            return self.block_text


def trim_line_last_chars(file_name):
    new_line = []
    for line in load_text_from(file_name):
        new_line.append(line[:-2])
    return new_line


def filter_lines(text_file, with_filter):
    stream = ''
    for line in text_file:
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


def load_text_from(file_name):
    with open(file_name, 'rb') as input_file:
        text = input_file.read()
        # for m in re.findall(r'\n\n', whole_data):
        # print m
    return text


def export_text_to(file_name, text):
    with open(file_name, 'w+') as output_file:
        output_file.write(text)


def file_content_difference(file1, file2):
    diff = difflib.unified_diff(fromfile=file1, tofile=file2, lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    removed = [line[1:] for line in lines if line[0] == '-']

    print 'additions, ignoring position'
    for line in added:
        if line not in removed:
            print line


def create_file_if_neccesary(file_name):
    FileSystemObject(file_name).object_create_neccesary()


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

    from log import Log

    parser = argparse.ArgumentParser(description='Text proccess')
    parser.add_argument('-i', help='Input file/dir', type=str, default='')
    parser.add_argument('-o', help='Output file/dir', type=str, default='')
    parser.add_argument('-m', help='Mode/Logic', type=str, default='')
    parser.add_argument('-l', help='Logfile', type=str, default='')
    args = parser.parse_args()

    logger = Log(args.l, args.i + ' + ' + args.o, __file__, True)
    input_object = FileSystemObject(args.i)

    if input_object.is_file:
        input_text = load_text_from(args.i)
        if not args.o:
            output_object = args.i+'2'
        else:
            create_file_if_neccesary(args.o)
            output_object = args.o
        export_text_to(output_object, TextContent(input_text).replace_line_endings())
    elif input_object.is_folder:
        for file_name in os.listdir(args.i):
            input_text = load_text_from(args.i + '/' + file_name)
            output_object = args.o + '/' + file_name
            if 'lin' in args.m:
                export_text_to(output_object, TextContent(input_text).replace_crlf_lf())
            elif 'win' in args.m:
                export_text_to(output_object, TextContent(input_text).replace_lf_crlf()) 
            else:
                export_text_to(output_object, TextContent(input_text).replace_lf_crlf())
    else:
        print args.i + ' -> input file/dir does not exist ...'
