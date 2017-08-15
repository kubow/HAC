#import argparse
#import win32com.client
import os
import socket
from smtplib import SMTP_SSL as SMTP  # secure SMTP (port 465, uses SSL)
# from smtplib import SMTP            # standard SMTP (port 25, no enc)
from email.mime.text import MIMEText

from OS74 import CurrentPlatform

class Message():
    def __init___(self):
        self.server = 'localhost'
        self.sender = 'jav@p297c.local'
        self.reciever = ['jakub.vajda@mdsaptech.cz']
        # typical values for text_subtype are plain, html, xml
        self.text_subtype = 'plain'

        # Prepare actual message
        self.subject = 'Hello!'
        self.content = '''\
        The contents of message goes here

        %s
        ''' % ('some special text goes here')

def send_mail():
    m = Message()

    message = MIMEText(m.content, m.text_subtype)
    message['Subject'] = m.subject
    message['From'] = m.sender

    # Send the message via our own SMTP server
    conn = SMTP(SMTPserver)
    xonn.set_debuglevel(False)

    s = smtplib.SMTP(m.server)

    s.sendmail(m.sender, m.reciever, m.message)
    s.quit()

def monitor_command_output(cmd):
    os.system(cmd)
    f = open('conn.tmp', 'r')
    f.readline();f.readline();f.readline()
    conn = []
    host = f.readline()
    while host[0] == '\\':
        conn.append(host[2:host.find(' ')])
    host = f.readline()
    f.close()
    print conn

def monitor_net_connections():
    os.system('net view > conn.tmp')
    f = open('conn.tmp', 'r')
    f.readline();f.readline();f.readline()

    conn = []
    host = f.readline()
    while host[0] == '\\':
        conn.append(host[2:host.find(' ')])
        host = f.readline()

    print conn
    f.close()   

def adodb_conn():
    conn = win32com.client.Dispatch(r'ADODB.Connection')
    DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/MyDB.mdb;'
    conn.Open(DSN)

    conn.Close(DSN)

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description="Monitor network")
    #parser.add_argument('-d', help='directory', type=str, default='')
    #args = parser.parse_args()

    monitor_command_output('net view > conn.tmp')

def socket_networking():
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8642 # H808E Port
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
     
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #Start listening on socket
    s.listen(10)
    print 'Socket now listening'
     
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
         
    s.close()