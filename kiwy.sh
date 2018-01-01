log_file=${PWD}/Multimedia/logfile.log
py_file=${PWD}/System/UI74KW.py
if [ "$1" = "a" ]
then
    echo 'python '${py_file}
    python3 ${py_file}
elif [ "$1" = "b" ]
then
    echo 'python '${py_file}' -m inspector'
    python3 ${py_file} -m inspector
elif [ "$1" = "c" ]
then
    echo "text mode"
else
    echo "1st argument"
    echo "    a - Normal Run"
    echo "    b - Debug"
    echo "    c - Text version (not impplemented)"
fi

