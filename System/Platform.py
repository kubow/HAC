import os
import platform

from sys import platform as _platform


# platform digger


def get_system():
    return platform.system()
    

def get_release():
    return platform.release()

def software_list_generate():
    if _platform == "linux" or _platform == "linux2":
       # linux
    elif _platform == "darwin":
       # MAC OS X
    elif _platform == "win32":
       # Windows
    elif _platform == "win64":
        # Windows 64-
