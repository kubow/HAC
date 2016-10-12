import sys
import importlib
import pip

def install(package):
    pip.main(['install', package])

for arg in sys.argv[1:]:
    try:
        print arg
#        map(__import__, arg)
        importlib.import_module(arg)
        print 'succesfully imported ' + arg
    except ImportError:
        print arg + ' is not installed, installing it now!'
        install(arg)

print 'all of packages should be fine ...'
sys.exit(1)