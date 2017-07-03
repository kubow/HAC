import os
import platform

from sys import platform as _platform


# platform digger

class Platform()
    def __init__(self):
        self.main = which platform()

def get_system():
    return platform.version()
    

def get_release():
    return platform.release()

def which_platform():
    if _platform == "linux" or _platform == "linux2":
        # linux
        print "linux"
    elif _platform == "darwin":
        # MAC OS X
        print "mac"
    elif _platform == "win32" or _platform == "win64":
        # Windows
        print "win"
    else :
        print _platform

if __name__ == '__main__':
    print dir(platform)
    which_platform()
    print "system".format(get_system())
    print "release - {0}".format(get_release())
