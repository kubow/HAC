# -*- coding: utf-8 -*-
import os
import sys

import log
print os.getcwd()
dir(sys)
#sys.setdefaultencoding('utf-8')
veta=u"Žluťoučký kůň pěl ďábelské ódy."
print veta
log.file_write("aaa.log", "temp", "random text")
