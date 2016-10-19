server = 'localhost'
sender = 'jav@midisgroup.local'
reciever = ['jakub.vajda@mdsaptech.cz']
# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'

# Prepare actual message
subject = 'Hello!'
content = '''\
The contents of message goes here

%s
''' % ('some special text goes here')

import sys
import os
import re

from smtplib import SMTP_SSL as SMTP       # secure SMTP (port 465, uses SSL)
# from smtplib import SMTP                  # standard SMTP (port 25, no enc)

from email.mime.text import MIMEText

message = MIMEText(content, text_subtype)
message['Subject'] = subject
message['From'] = sender

# Send the message via our own SMTP server
conn = SMTP(SMTPserver)
xonn.set_debuglevel(False)

s = smtplib.SMTP(server)

s.sendmail(sender, to, message)
s.quit()