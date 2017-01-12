
# Determine if passed parguments for running over a directory
if len(sys.argv) > 1:
    # might chceck for trailing \
    directory = sys.argv[1:]
else:
    # os.getcwd() - not applicable if being called from elsewhere
    directory = os.path.dirname(os.path.realpath(__file__))
print 'exporting for new files in directory :' + directory
