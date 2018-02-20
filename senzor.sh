py_file=${PWD}/System/DBL.py
py_file2=${PWD}/System/DV72.py

if [ "$1" = "s" ]
then
    echo 'python '${py_file}' -m read_serial -l '${PWD}'/Multimedia/'
    python ${py_file} -m serial -l ${PWD}/Multimedia/
    python ${py_file2} -d serial -l ${PWD}/Multimedia/
elif [ "$1" = "l" ]
then
    echo 'python '${py_file}' -m inspector -l '${PWD}'/Multimedia/'
    python ${py_file} -m inspector -l ${PWD}/Multimedia/
elif [ "$1" = "c" ]
then
    echo "text mode"
else
    echo "1st argument"
    echo "    s - run serial reader"
    echo "    l - list devices"
    echo "    c - .. no func now"
fi

