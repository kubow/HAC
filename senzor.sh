py_file=${PWD}/System/DV72.py

if [ "$1" = "s" ]
then
    echo 'python '${py_file}' -m read_serial -l '${PWD}'/Multimedia/'
    ${py_file} -m read_serial -l ${PWD}/Multimedia/
elif [ "$1" = "l" ]
then
    echo 'python '${py_file}' -m inspector -l '${PWD}'/Multimedia/'
    ${py_file} -m inspector -l ${PWD}/Multimedia/
elif [ "$1" = "c" ]
then
    echo "text mode"
else
    echo "1st argument"
    echo "    s - run serial reader"
    echo "    l - list devices"
    echo "    c - .. no func now"
fi

