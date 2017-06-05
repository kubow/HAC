# -*- coding: utf-8 -*-
import os
import sys

import log

def test_utf_special_characters():
    print os.getcwd()
    veta=u"Žluťoučký kůň pěl ďábelské ódy."
    print veta
    log.file_write("aaa.log", "temp", veta)

if __name__ == '__main__':
    #sys.setdefaultencoding('utf-8')
    test_utf_special_characters()
    dir(sys)
