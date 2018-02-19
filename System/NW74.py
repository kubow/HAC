#import argparse
import os, sys
import socket
from email.mime.text import MIMEText
import shlex  
from subprocess import Popen, PIPE, STDOUT
import numpy

try:
    import netifaces as ni
except ImportError:
    print('... not using network interfaces...')
try:
    import pexpect
except ImportError:
    print('... not using pexpect')
try:
    from smtplib import SMTP_SSL as SMTP  # secure SMTP (port 465, uses SSL)
    # from smtplib import SMTP            # standard SMTP (port 25, no enc)
    import win32com.client
except ImportError:
    print('... win specific modules not load')

from OS74 import CurrentPlatformControl


class HostLocal(object):
    def __init__(self):
        CurrentPlatformControl.__init__(self)

    def ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def ip_address_eth0(self):
        ni.ifaddresses('eth0')
        ip = ni.ifaddresses('eth0')[2][0]['addr']
        return ip



class Message():
    def __init___(self):
        self.server = 'localhost'
        self.sender = 'jav@p297c.local'
        self.reciever = ['kubow@tiscali.cz']
        # typical values for text_subtype are plain, html, xml
        self.text_subtype = 'plain'

        # Prepare actual message
        self.subject = 'Hello!'
        self.content = '''\
        The contents of message goes here

        %s
        ''' % ('some special text goes here')


class WifiLatencyBenchmark(object):
    def __init__(self, ip):
        object.__init__(self)

        self.ip = ip
        self.interval = 0.5

        ping_command = 'ping -i ' + str(self.interval) + ' ' + self.ip
        self.ping = pexpect.spawn(ping_command)

        self.ping.timeout = 1200
        self.ping.readline()  # init
        self.wifi_latency = []
        self.wifi_timeout = 0

    def run_test(self, n_test):
        for n in range(n_test):
            p = self.ping.readline()

            try:
                ping_time = float(p[p.find('time=') + 5:p.find(' ms')])
                self.wifi_latency.append(ping_time)
                print('test:', n + 1, '/', n_test, ', ping latency :', ping_time, 'ms')
            except:
                self.wifi_timeout = self.wifi_timeout + 1
                print('timeout')

        self.wifi_timeout = self.wifi_timeout / float(n_test)
        self.wifi_latency = numpy.array(self.wifi_delay)

    def get_results(self):
        print('mean latency', numpy.mean(self.wifi_latency), 'ms')
        print('std latency', numpy.std(self.wifi_latency), 'ms')
        print('timeout', self.wifi_timeout * 100, '%')


def send_mail():
    m = Message()

    message = MIMEText(m.content, m.text_subtype)
    message['Subject'] = m.subject
    message['From'] = m.sender

    # Send the message via our own SMTP server
    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)

    s = SMTP(m.server)

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
    print(conn)

def monitor_net_connections():
    os.system('net view > conn.tmp')
    f = open('conn.tmp', 'r')
    f.readline();f.readline();f.readline()

    conn = []
    host = f.readline()
    while host[0] == '\\':
        conn.append(host[2:host.find(' ')])
        host = f.readline()

    print(conn)
    f.close()   

def adodb_conn():
    conn = win32com.client.Dispatch(r'ADODB.Connection')
    DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/MyDB.mdb;'
    conn.Open(DSN)

    conn.Close(DSN)


def socket_networking():
    HOST = ''  # Symbolic name, meaning all available interfaces
    PORT = 8642  # H808E Port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    print('Socket bind complete')

    # Start listening on socket
    s.listen(10)
    print('Socket now listening')

    # now keep talking with the client
    while 1:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

    s.close()


def get_simple_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a simple external command and get its output.
    """
    print('run ' + cmd)
    args = shlex.split(cmd)
    print(args)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]


def get_ping_time(host):
    host = host.split(':')[0]
    ping = CurrentPlatformControl('ping')
    #cmd = "ping {host}".format(host=host)
    #res = [float(x) for x in get_simple_cmd_output(cmd).strip().split(':')[-1].split() if x != '-']
    #res = get_simple_cmd_output(cmd)
    res = ping.check_output(host, timeout=5)
    if len(res) > 0:
        return sum(res) / len(res)
    else:
        return 999999


if __name__ == '__main__':

    #parser = argparse.ArgumentParser(description="Monitor network")
    #parser.add_argument('-d', help='directory', type=str, default='')
    #args = parser.parse_args()

    #monitor_command_output('net view > conn.tmp')
    #while True:
        #response = WifiLatencyBenchmark('8.8.8.8')

        #response.run_test(n_test)
        #response.get_results()
    print(HostLocal().ip_address())

    print(get_ping_time('8.8.8.8'))

