'''simple function to install missing packages
using command line arguments as package names
then trying to import or install them with pip'''
import sys
import importlib
import pip

def install(package):
    '''actual installation'''
    try:
        pip.main(['install', package])
        importlib.import_module(package)
        print 'successfully installed "' + package + '"'
    except:
        print 'error installing "' + package + '"'
        global all_good
        all_good = False

'''parse command line arguments'''
all_good = True
for pkg in sys.argv[1:]:
    try:
        print pkg
#        map(__import__, pkg)
        importlib.import_module(pkg)
        print 'package "' + pkg + '" is installed'
    except ImportError:
        print 'package "' + pkg + '" is not installed, installing now...'
        install(pkg)
if all_good:
    print 'all of packages should be fine ...'
else:
    print 'there was some error...'
sys.exit(1)