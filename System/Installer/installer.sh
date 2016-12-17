# check if pip present
set -- $(<py_packages.txt)
echo checking if installed: $@
python installer.py $@
