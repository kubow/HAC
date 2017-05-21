# check if pip present
# - not implemented yet
# read packages from text file
set -- $(<py_packages.txt)
echo checking if installed: $@
# put all of them as an argument
python installer.py $@ > logfile.log
