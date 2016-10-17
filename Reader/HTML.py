import os
import sqlite3
import requests
try:
  from bs4 import BeautifulSoup
  import HTMLParser
  easier = True
except:
  import HTMLParser
  easier = False

# http://stackoverflow.com/questions/3276040/how-can-i-use-the-python-htmlparser-library-to-extract-data-from-a-specific-div

class LinksParser(HTMLParser.HTMLParser):
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
      if name == 'id' and value == 'contentwsw':
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

def process_url(url, tag_name):
  '''proccess text from url, given url, tag type and id'''
  html = requests.get(url)
  if easier:
    soup = BeautifulSoup(html.content, "lxml") 
    div = soup.find('div', id=tag_name)
    return ''.join(map(str, div.contents))
  else:
    p = LinksParser()
    div = p.feed(html)
    p.close()
    return div

def write_html(file_name, content):
  '''write html content to a file using template'''
  print file_name
  print content
  
''' read restaurant menus, write to separate htm files'''
conn=sqlite3.connect(os.getcwd()+'/Reader.db')
rest=conn.execute('SELECT * FROM RestActive;').fetchall()
for row in rest:
  print row[3]+' > '+row[2]+'.htm'
  if not row[4]:
    # zomato address
    parsed_content=process_url(row[5], 'daily-menu-container')
  else:
    # dependalble on input text
    parsed_content=process_url(row[4], row[6])
  write_html(os.getcwd()+'/'+row[2]+'.htm', )


