# -*- coding: utf-8 -*-
""" Proccessing Text (c) Kube Kubow
replace line endings, load/write text to a file
compare text simrality
"""
import sys
import re
import argparse
import difflib
import datetime
import json
import xml.etree.ElementTree
import lxml.html
import feedparser
import requests
from glob import glob  #pdf reading purposes
from time import clock #benchmark purposes
# from xml.dom.minidom import parseString
# sys.setdefaultencoding('utf-8')

try:
    html_easier = True
    from bs4 import BeautifulSoup
except ImportError:
    html_easier = False

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

try:
    import pandas
except ImportError:
    print('using alternative csv parser')
finally:
    import csv

from Template import HTML, SQL
from OS74 import FileSystemObject, CurrentPlatform


class WebContent(HTMLParser):
    """General class for reading HTML Pages or RSS Feeds"""

    def __init__(self, url, log_file='', mode='html'):
        uah = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'
        HTMLParser.__init__(self)
        self.headers = {"User-Agent": uah}
        self.easier = html_easier # can use beatiful soup 4
        self.mode = mode
        self.recording = 0  # flag for exporting data
        self.data = []
        self.url = url
        self.div = None
        self.div_text = ''
        self.html_text = ''
        self.log_file = log_file

    def is_html(self):
        try:
            if lxml.html.fromstring(self.html_text).find('.//*') is not None:
                return True
            else:
                return False
        except:
            return False

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

    def parse_html_text(self):
        if self.easier:
            soup = BeautifulSoup(self.html_text, 'lxml')
            return soup
        else:
            # TODO: same logic as with beautiful soup
            p = WebContent()
            oups = p.feed(self.html_text)
            p.close()
            return oups

    def parse_rss_feed(self, the_feed):
        inner_text = ''
        for feed_entry in the_feed.entries:
            inner_text += "\n__________"
            inner_text += feed_entry.get("guid", "")
            inner_text += feed_entry.get("title", "")
            inner_text += feed_entry.get("link", "")
            inner_text += feed_entry.get("description", "")
            inner_text += "\n__________"
            for feed_namespace in the_feed.namespaces:
                if feed_namespace == 'media':
                    inner_text += 'Media'
                    allmediacontent = feed_entry.get("media_content", "")
                    for themediacontent in allmediacontent:
                        inner_text += themediacontent["url"]
                        inner_text += themediacontent["height"]
                        inner_text += themediacontent["width"]
        return inner_text

    def process_url(self, tag_type='', tag_name=''):    
        if 'id' in str(tag_type).lower():
            tag_type = 'id'
        elif 'class' in str(tag_type).lower():
            tag_type = 'class'
        done = False
        try:
            self.div = ''
            self.div_text = ''
            if 'rss' in self.mode:
                self.html_text = feedparser.parse(self.url)
                self.div_text = self.parse_rss_feed(self.html_text)
                done = True
            else:
                if self.url.startswith('file:'):
                    self.html_text = FileSystemObject(self.url.split('///')[-1]).object_read()
                elif self.url.startswith('ftp:'):
                    self.html_text = 'FTP read not implemented yet'
                elif self.url.startswith('http:') or self.url.startswith('https:'):
                    self.html_text = requests.get(self.url, timeout=(10, 5), headers=self.headers).content
                else:
                    self.html_text = requests.get('http://' + self.url, timeout=(10, 5), headers=self.headers).content
            if self.is_html():
                parsed_content = self.parse_html_text()
                done = True
                if self.easier:
                    if not tag_name:
                        self.div = parsed_content.find('body')
                        self.div_text = parsed_content.find('body').text
                    else:
                        self.div = parsed_content.find('div', {tag_type: tag_name})
                        if not self.div:
                            self.div = parsed_content.find('body')
                            self.div_text = parsed_content.find('body').text
                        else:
                            self.div_text = parsed_content.find('div', {tag_type: tag_name}).text
                else:
                    self.div = parsed_content
                    self.div_text = parsed_content
            else:
                self.div = self.html_text
                if not self.div_text:
                    self.div_text = self.html_text
        except:
            print('---some else error occurred (' + self.url + '): ' + str(sys.exc_info()[0]))
            if done:
                if parsed_content:
                    self.div = str(parsed_content)
                    print('---cannot parse content of {0} ({1})'.format(self.url, parsed_content[:10]))
                elif self.html_text:
                    self.div = str(self.html_text)
            else:
                self.div = ''
                self.div_text = ''

    def write_web_content_to_file(self, file_path, heading):
        if self.div:
            print('creating ' + file_path + ' from: ' + self.url)
            try:
                FileSystemObject(file_path).object_write(HTML.skelet_titled.format(heading, self.div), 'w+')
            except:
                FileSystemObject(file_path).object_write(HTML.skelet_titled.format(heading, 'cannot get text/bad char'), 'w+')
            if self.log_file:
                self.log_to_database(self.log_file.replace('.log', '.sqlite'), heading)
        else:
            print('no content parsed from: ' + self.url)

    def log_to_database(self, db_path, heading):
        user, domain = CurrentPlatform().environment
        time_stamp = datetime.datetime.now().strftime('%d.%m.%Y')
        try:
            tag_content = self.div_text.replace('\n\n\n\n', '\n').replace('\n\n', '\n')
        except:
            tag_content = 'cannot catch div text...'
        # table structure
        table_def = 'Log (Connection, CPName, Report, LogDate, User, Domain)'
        values_template = '"{0}", "{1}", "{2}", "{3}", "{4}", "{5}"'
        table_values = values_template.format(heading, 0, tag_content, time_stamp, user, domain)
        sql = SQL.insert.format(table_def, table_values)
        DataBaseObject(db_path).log_to_database('Log', sql)


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
            print('no proper content, skipping')
            return
        for ac_time, vals in content.items():
            row = ''
            if line == 1:
                for d, v in vals.items():
                    row += str(d) + ','
                row = 'datetime, ' + row
                f.write(row + '\n')
            row = str(ac_time) + ','
            for d, v in vals.items():
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
            for column in csv_object.describe().items():
                if 'unnamed' in column[0][0].lower():
                    continue
                for statistic in column[0][1].items():
                    if 'mean' in statistic[0][0]:
                        values[column[0][0]] = statistic[0][1]
                        break
            self.read_success = True
            return values
        except Exception as ex:
            print('problem in csv ' + self.path + ' : ' + ex.args[0])
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
    def __init__(self, location, write=False, direct=False):
        if direct:
            self.content = json.loads(location)
        else:
            self.path = location
            self.json_skeleton = '[\n{0}\n]'
            self.json_row = '[{0}, {1}],\n'
            if not write:
                self.content = self.json_format()
            else:
                self.process()

    def process(self):
        fs = FileSystemObject(self.path)
        for database in fs.object_read(filter='sqlite').items():
            db = DataBaseObject(FileSystemObject(self.path).append_objects(file=database[0]))
            for velocity in db.object_structure('measured'):
                if 'timestamp' in velocity or 'device' in velocity or not velocity:
                    continue
                velocity_name = velocity.split(' ')[0]
                if not db.return_one(SQL.measured_column_count.format(velocity_name, velocity_name, velocity_name))[0]:
                    continue  # determine if column contains data
                velocity_values = {}
                for value in db.return_many(SQL.column_select.format('timestamp, ' + velocity_name, 'measured')):
                    velocity_values[value[0]] = value[1]
                self.write(fs.append_objects(file=velocity_name + '.json'), velocity_values)

    def json_format(self):
        if FileSystemObject(self.path).is_file:
            print('file: ' + self.path)
            with open(self.path, 'r') as fh:
                # first = next(fh).decode()
                first = fh.readline()
                print('got first line' + first)
                print('*****************')
                fh.seek(-512, 2)
                # last = fh.readlines()
                last = fh.readlines()[-1].decode()
            return first, last
        else:
            print('cycle all json files in folder and recursively call this function')

    def write(self, file_name,  content=''):
        json_file = FileSystemObject(file_name)
        final_content = ''
        for record in content:
            final_content += self.json_row.format(record, content[record])
        if json_file.exist:
            if JsonContent(file_name).json_format():
                final_content = 'read_whole_file' + final_content
                print('implement appending .. not now yet')
        json_file.object_write(self.json_skeleton.format(final_content))


class TextContent(object):
    def __init__(self, block_text='', file_name=''):
        if file_name:
            self.file_name = file_name
            with open(file_name, 'rb') as input_file:
                self.block_text = input_file.read()
        else:
            self.block_text = block_text
            self.file_name = ''

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
            print('this text does not have any windows line endings, passing ...')
            return self.block_text

    def replace_lf_crlf(self):
        # replace linux line endings with windows line endings
        if re.search('\r?\n'):
            return re.sub('\r?\n', '\r\n', self.block_text)
        else:
            print('this text does not have any linux line endings, passing ...')
            return self.block_text

    def trim_line_last_n_chars(self, n=1):
        n_chars = (-1*n)-1
        block_text = []
        for line in self.block_text:
            block_text.append(line[:n_chars])
        return block_text

    def similar_to(self, compare_text):
        if isinstance(compare_text, str):
            return difflib.SequenceMatcher(a=self.block_text.lower(), b=compare_text.lower()).ratio()
        else:
            return difflib.SequenceMatcher(a=self.block_text.lower(), b=str(compare_text).lower()).ratio()


class PdfContent(object):
    def __init__(self, path_containing_pdf):
        self.path = path_containing_pdf

    def count(self):
        """
        Takes one argument: the path where you want to search the files.
        Returns a dictionary with the file name and number of pages for each file.
        https://www.daniweb.com/programming/software-development/threads/152831/read-number-of-pages-in-pdf-files
        """
        #
        # cdef double ti = clock() #Used for benchmark.
        #
        pdf_file_list = glob(self.path + "\\" + '*.pdf')
        vPages = 0
        vMsg = {}
        #
        for pdf_file in pdf_file_list:
            print(pdf_file)
            pdf_file_content = open(pdf_file, mode='r', buffering=1, encoding='utf-8')
            for line in pdf_file_content.readlines():
                print(line)
                if "/Count " in line:
                    vPages = int(re.search("/Count \d*", line).group()[7:])
            vMsg[pdf_file] = vPages
            pdf_file_content.close()
        #
        # cdef double tf = clock() #Used for benchmark.
        #
        # print tf-ti
        return vMsg


def file_content_difference(file1, file2):
    diff = difflib.unified_diff(fromfile=file1, tofile=file2, lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    removed = [line[1:] for line in lines if line[0] == '-']

    print('additions, ignoring position')
    for line in added:
        if line not in removed:
            print(line)


def xml_to_html(xml_text):
    html_text = ''
    h = HTML()
    if not xml.etree.ElementTree.fromstring(xml_text).text:
        return None
    for element in xml.etree.ElementTree.fromstring(xml_text)._children:
        if element.text is not None:
            if len(element.attrib) > 0:
                if 'scale' in element:
                    if element.attrib['scale'] == 'h1':
                        html_text += h.heading.format('1', element.text)
                    elif element.attrib['scale'] == 'h2':
                        html_text += h.heading.format('2', element.text)
                    else:
                        html_text += h.paragraph.format('2', element.text)
                else:
                    html_text += h.paragraph.format(element.text)
            else:
                for par_text in element.text.split('\n'):
                    html_text += h.paragraph.format(par_text)
        else:
            html_text += h.paragraph.format('... no content for this part ...\n')
    return html_text


def test_utf_special_characters(logger=''):
    veta = u'Žluťoučký kůň pěl ďábelské ódy.'
    print(veta)
    if logger:
        logger.file_write('aaa.log', 'temp', veta)


if __name__ == '__main__':
    from log import Log
    from DB74 import DataBaseObject

    parser = argparse.ArgumentParser(description='Text proccess')
    parser.add_argument('-i', help='Input file/dir', type=str, default='')
    parser.add_argument('-o', help='Output file/dir', type=str, default='')
    parser.add_argument('-m', help='Mode/Logic', type=str, default='')
    parser.add_argument('-l', help='Logfile', type=str, default='')
    args = parser.parse_args()

    logger = Log(args.l, args.i + ' + ' + args.o, __file__, True)
    input_object = FileSystemObject(args.i)

    if input_object.is_file:
        input_text = input_object.object_read()
        output_object = args.o
        if not output_object:
            output_object = args.i+'2'
        FileSystemObject(output_object).object_write(TextContent(input_text).replace_line_endings())
    elif input_object.is_folder:
        folder_list = input_object.object_read()
        for f_name in folder_list.items():
            file_name = folder_list[f_name[0]]
            input_text = FileSystemObject(args.i + '/' + file_name).object_read()
            output_object = args.o + '/' + file_name
            if 'lin' in args.m:
                FileSystemObject(output_object).object_write(TextContent(input_text).replace_crlf_lf())
            else:
                FileSystemObject(output_object).object_write(TextContent(input_text).replace_lf_crlf())
    else:
        print(args.i + ' -> input file/dir does not exist ...')