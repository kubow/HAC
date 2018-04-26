# -*- coding: utf-8 -*-
from __future__ import unicode_literals

""" Proccessing Text (c) Kube Kubow
replace line endings, load/write text to a file
compare text simrality
"""

import datetime
import difflib
import json  # alternative simplejson not used
import re
import sys
import xml.etree.ElementTree
from glob import glob  # pdf reading purposes
from pprint import pprint
# from time import clock  # benchmark purposes

from DB74 import DataBaseObject
from OS74 import CurrentPlatform, FileSystemObject
from Template import HTML, SQL

# sys.setdefaultencoding('utf-8')
# from xml.dom.minidom import parseString

try:
    import requests
    import http.client
    request_logic = True
except ImportError:
    request_logic = False

try:
    import urllib.request
    url_logic = True
except ImportError:
    url_logic = False

try:
    import lxml.html
    html_easy = True
except ImportError:
    print("+++ lxml not imported, must determine html text alternatively")
    html_easy = False

try:
    html_easier = False  # change after debug
    from bs4 import BeautifulSoup
except ImportError:
    print("+++ beautiful soup not imported, must determine html text alternatively")
    html_easier = False

try:
    from html.parser import HTMLParser  # python 3x
except ImportError:
    from HTMLParser import HTMLParser  # python 2x

try:
    import feedparser
    web_easier = True
except ImportError:
    print("+++ feedparser not imported, cannot process rss")
    web_easier = False

try:
    import pandas
except ImportError:
    print('+++ using alternative csv parser')
finally:
    import csv

uah = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'
headers = {"User-Agent": uah}


class TextContent(object):
    def __init__(self, block_text='', file_name=''):
        try:
            if file_name:
                self.source = file_name
                with open(file_name, 'rb') as input_file:
                    self.block_text = input_file.read()
            else:
                self.block_text = block_text
                self.source = 'direct_input'
            self.valid = len(block_text) > 0
        except (OSError, IOError) as e:
            print(str(e.args))
        except:
            print('not valid string ... ' + str(self.block_text))
            self.valid = False

    def recompile_regexp(self):
        self.block_text = re.compile(r"(?ui)\W", self.block_text)

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
        if re.search('\r?\n', self.block_text):
            return re.sub('\r?\n', '\r\n', self.block_text)
        else:
            print('this text does not have any linux line endings, passing ...')
            return self.block_text

    def trim_line_last_n_chars(self, n=1):
        n_chars = (-1 * n) - 1
        block_text = []
        for line in self.block_text:
            block_text.append(line[:n_chars])
        return block_text

    def similar_to(self, compare_text):
        if isinstance(compare_text, str):
            return difflib.SequenceMatcher(a=self.block_text.lower(), b=compare_text.lower()).ratio()
        else:
            return difflib.SequenceMatcher(a=self.block_text.lower(), b=str(compare_text).lower()).ratio()


class WebContent(HTMLParser):
    """General class for reading HTML Pages or RSS Feeds"""

    def __init__(self, url, log_file='', mode='html'):
        self.headers = {"User-Agent": uah}
        self.easier = html_easier  # can use beatiful soup 4
        self.mode = mode
        self.recording = 0  # flag for exporting data
        self.data = []
        self.url = url
        self.div = None
        self.div_text = ''
        self.log_file = log_file

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
        self.div = ''
        self.div_text = ''
        self.div = whats_on(obj_type='html', obj_content=self.url, tag_type=tag_type, tag_name=tag_name)
        if not self.div:
            print('--- fetching whole page: {0} ( instead of tag {1}: {2} )'.format(self.url, tag_type, tag_name))
            self.div = whats_on(obj_type='html', obj_content=self.url)
        # pprint(vars(self))
        self.div_text = self.div

    def write_web_content_to_file(self, file_path, heading):
        if self.div:
            print('creating ' + file_path + ' from: ' + self.url)
            top = heading.encode('utf-8')
            try:
                FileSystemObject(file_path).object_write(HTML.skelet_titled.format(top, self.div.decode('utf-8')), 'w+')
                if self.log_file:
                    self.log_to_database(self.log_file.replace('.log', '.sqlite'), heading)
            except Exception as ex:
                print('failure: ' + str(ex.args))
                print(type(top))
                print(dir(top))
                # pprint(vars(self))
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
            print(csv_object.describe())
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
        try:
            if direct:
                self.content = json.loads(whats_on('http://'+location))
            else:
                self.path = location
                self.json_skeleton = '[\n{0}\n]'
                self.json_row = '[{0}, {1}],\n'
                if not write:
                    self.content = self.json_format()
                else:
                    self.process()
        except:
            print(location + ' > json_parse failure')
            pprint(vars(self))
            self.content = ''

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

    def write(self, file_name, content=''):
        json_file = FileSystemObject(file_name)
        final_content = ''
        for record in content:
            final_content += self.json_row.format(record, content[record])
        if json_file.exist:
            if JsonContent(file_name).json_format():
                final_content = 'read_whole_file' + final_content
                print('implement appending .. not now yet')
        json_file.object_write(self.json_skeleton.format(final_content))


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


class MyHTMLParser(HTMLParser):
    def __init__(self, tag_type, tag_name):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
        print(tag_type + ' / ' + tag_name)
        self.start_tag_type = tag_type
        self.start_tag_name = tag_name

    def handle_starttag(self, tag, attributes):
        if tag != 'div':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if str(name) == self.start_tag_type and str(value) == self.start_tag_name:
                print('found ' + name + ' tag: ' + value)
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        print('debug in parser handle_data: ' + str(self.recording))
        if self.recording:
            self.data.append(data)


def file_content_difference(file1, file2):
    diff = difflib.unified_diff(a=file1, b=file2, lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    removed = [line[1:] for line in lines if line[0] == '-']

    print('additions, ignoring position')
    for line in added:
        if line not in removed:
            print(line)


def whats_on(obj_type='', obj_content='', tag_type='', tag_name=''):
    """function for parsing and extracting texts from objects
    URL link to a site - using feed parser
    HTML content - using bs4 or HTMLParser
    XML content - using feedparser or lxml
    JSON content - 
    TEXT content - using match pattern or regexp
    """
    # if any(s in str(obj_type) for s in ['url', 'link', 'web', 'rss', 'xml']):
    # if is address
    if '://' in obj_content:
        print('... loading content from web address ' + obj_content)
        obj_content = load_content(obj_content)
    # distinct logic based on input object type (presuming obj_content already contain text)
    if any(s in str(obj_type) for s in ['htm', 'url', 'link', 'web']):
        if html_easier:
            parsed = BeautifulSoup(obj_content, 'lxml')
        else:
            parsed = obj_content.decode()
    elif any(s in str(obj_type) for s in ['xml', 'rss']):
        parsed1 = xml.etree.ElementTree.fromstring(obj_content)
        # compare variables parsed1 and parsed
    elif any(s in str(obj_type) for s in ['json', 'js']):
        print('json proccess - ' + str(obj_content))
        if not obj_content:
            return 'cannot parse content (' + str(obj_content) + ')'
        parsed = json.loads(obj_content)
    else:
        parsed = obj_content.decode()
    # second step is voluntary - extract only filtered tags
    # pprint(parsed)
    # uncomment above for debug purposes
    if tag_type or tag_name:
        try:
            if any(s in str(obj_type) for s in ['htm', 'url', 'link', 'web']):
                if html_easy:
                    print('--- lxml processing')
                    build = [a for a in parsed.cssselect('a')]
                    return ', '.join(build)
                elif html_easier:
                    print('- - - beatifulSoup processing')
                    return parsed.find('div', {tag_type: tag_name})
                else:
                    print('- - - HTMLParser processing')
                    return MyHTMLParser(tag_type, tag_name).feed(parsed.decode('utf-8')).data
            elif any(s in str(obj_type) for s in ['xml', 'rss']):
                return parsed[tag_name]
            else:
                return TextContent(parsed).similar_to(tag_name)
        except:
            print('!!! cannot find tag ' + tag_type + ' - ' + tag_name)
            return parsed
    else:
        return parsed


def load_content(content_address, is_local=False):
    content_address = str(content_address)
    if is_local:
        return FileSystemObject(content_address).object_read()
    elif content_address.startswith('file:'):
        return FileSystemObject(content_address.split('///')[-1]).object_read()
    elif content_address.startswith('ftp:') or content_address.startswith('ftp.'):
        return 'FTP read not implemented yet'
    else:
        if not content_address.startswith(('http://', 'https://')):
            # append http in case of missing
            content_address = 'http://' + content_address
        try:
            if request_logic:
                request = requests.get(content_address, timeout=(10, 5), headers=headers)
                print('--- > successfully used requests to download')
                return request.content
            elif html_easy:
                request = lxml.html.parse(content_address)
                print('--- > successfully used lxml.html to download')
                return request.getroot()
            elif url_logic: # urllib seems to be malfunctioning in some environments
                request = urllib.request.Request(content_address, data=None, headers=headers)
                print('--- > successfully used urllib to download')
                return urllib.request.urlopen(request).read()
            elif web_easier:
                request = feedparser.parse(content_address)
                print('--- > successfully used feedparser to download')
                return request
            else:
                conn = http.client.HTTPSConnection(content_address)
                conn.request("GET", "/")
                request = conn.getresponse()
                request_data = request.read()
                conn.close()
                return request_data
        except Exception as ex:
            print('!!! failure while fetching (' + content_address + '): ' + str(sys.exc_info()))  # + str(ex.args))


def is_html(query_text=''):
    try:
        if lxml.html.fromstring(query_text).find('.//*') is not None:
            return True
        else:
            return False
    except:
        return False


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
