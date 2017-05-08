# -*- coding: utf-8 -*- 
import os
import sys
import sqlite3
import requests
try:
    from bs4 import BeautifulSoup
    import HTMLParser
    easier = True
except:
    import HTMLParser
    easier = False

class LinksParser(HTMLParser.HTMLParser):
    """http://stackoverflow.com/questions/3276040/how-can-i-use-the-python-htmlparser-library-to-extract-data-from-a-specific-div """
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attributes): #, tag_type, tag_name):
        if tag != 'div':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if name == 'id' and value == 'daily-menu-container':
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

def process_url(url, tag_name, data_type):
    '''proccess text from url, given url, tag type and id'''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
    try:
        html = requests.get(url, timeout=(10, 5))
    except Exception as ex:
        return '<a href="'+url+'">'+url+'</a>\n'+ex.args[0]
    print 'got '+url
    if data_type=='HTML':
        try:
            print 'searching for tag: '+tag_name
            if easier:
                soup = BeautifulSoup(html.content, "lxml") 
                div = soup.find('div', {'id': tag_name})
                print div
                return ''.join(map(str, div.contents))
            else:
                p = LinksParser()
                div = p.feed(html.content)
                print div
                p.close()
                return div
        except Exception as ex:
            return ex.args[0]
    elif data_type=='XML':
        return html
    else:
        return 'cannot parse '+data_type

def read_tempfile(file_paths):
    '''read content from a file and return it'''
    file_content=''
    file_count=1
    for tf in file_paths:
        f=open(tf, 'r')
        for line in f:
            file_content=file_content+line # +'\n'
        f.close()
        if file_count==1:
            file_content=file_content+'\n{1}\n'
        file_count+=1
    return file_content

def write_html(file_name, content, html_template):
    '''write html content to a file using template'''
    print file_name
    f=open(file_name,'w')
    f.write(html_template.format('Restaurant Menu', content))
    #f.write(content.encode('utf8'))
    f.close()
    
""" read restaurant menus, write to separate htm files
workpath can be either command line parameter
or if not given to current working directory"""
workpath=os.path.dirname(os.getcwd()+'/Multimedia/')
temppath=os.path.dirname(os.getcwd()+'/Structure/')
# workpath=os.path.dirname(os.path.realpath(__file__))
# directory = os.path.dirname(os.path.realpath(__file__)+'/HTML')
# check if RestMenu folder exists
print workpath
if not os.path.exists(workpath+'/RestMenu'):
    os.makedirs(workpath+'/RestMenu')
    print 'directory '+workpath+'/RestMenu folder created ...'
# print 'connecting from '+os.path.dirname(os.path.realpath(__file__))
conn=sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+'/DataReaderWeb.db')
# Determine if passed parguments for running over a directory
if len(sys.argv)>1:
    # process command line arguments
    if len(sys.argv)<3:
        where='Shortcut = "'+''.join(sys.argv[1:])+'"'
    else:
        where='" OR Shortcut = "'.join(sys.argv[1:])
    sql='SELECT * FROM RestActive WHERE {0};'.format(where)
else:
    # or just select all
    sql='SELECT * FROM RestActive;'
print sql
rest=conn.execute(sql).fetchall()
# load html template file
temp=read_tempfile((temppath+'/HTML_Base_head.txt',temppath+'/HTML_Base_tail.txt'))
# iterate returned restaurants from table
for row in rest:
    #print '---- Restaurant: '+row[3].encode('utf-8')+' > '+row[2]+'.htm'
    if not row[4] or row[4]=='':
        # zomato address
        parsed_content=process_url(row[5], 'daily-menu-container', row[9])
    else:
        # dependalble on input text
        parsed_content=process_url(row[4], row[6], row[9])
    write_html(workpath+'/RestMenu/'+row[2]+'.htm', parsed_content, temp)
