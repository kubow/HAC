py_file=${PWD}/System/DV72.py

if [ "$1" = "s" ]
then
    echo 'python '${py_file}' -l '${PWD}'/Multimedia/ -m read'
    python ${py_file} -l ${PWD}/Multimedia/ -m read
elif [ "$1" = "l" ]
then
    echo 'python '${py_file}' -l '${PWD}'/Multimedia/ -m inspector'
    python ${py_file} -l ${PWD}/Multimedia/ -m inspector
elif [ "$1" = "c" ]
then
    echo "text mode"
else
    echo "1st argument"
    echo "    s - run serial reader"
    echo "    l - list devices"
    echo "    c - .. no func now"
fi



