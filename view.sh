log_file=${PWD}/Multimedia/logfile.log
if [ "$1" = "h" ]; then # HANA
    py_file=hdbalm.py
        echo 'python '${py_file}
    python ${py_file}
elif [ "$1" = "s" ]; then # SQLite
    py_file=${PWD}/System/DB74.py
    echo 'python '${py_file}' -a '$2' -l '${log_file}
    python ${py_file} -a $2 -l ${log_file}
elif [ "$1" = "t" ]; then # text file
    py_file=${PWD}/System/SO74TX.py
    python ${py_file} -i $2 -l ${log_file}
elif [ "$1" = "b" ]; then # directory
    py_file=${PWD}/System/OS74.py
    echo 'python '${py_file}' -m -m True/False -i '$2' -l '${log_file}
    python ${py_file} -m True -i $2 -l ${log_file}
elif [ "$1" = "l" ]; then # list directory files
    py_file=${PWD}/System/OS74.py
    echo 'python '${py_file}' -m -m True/False -i '$2' -l '${log_file}
    python ${py_file} -m -i $2 -l ${log_file}
elif [ "$1" = "r" ]; then # rss
    py_file=${PWD}/System/UI74SO.py
    echo 'python '${py_file}' -g rss -w '${PWD}' -l '${log_file}
    python ${py_file} -g rss -w ${PWD} -l ${log_file}
else
    echo '1st parameter:'
    echo '- - - DATABASE MODE - - -'
    echo '  h - HANA '
    echo '  s - SQLite'
    echo '- - - FILE MODE - - -'
    echo '  t - pure text file'
    echo '- - - FOLDER MODE - - -'
    echo '  b - browse folders'
    echo '  l - list folder files'
    echo '- - - WEB MODE -'
    echo '  r - rss feed display'
    echo '2nd parameter: object location'
fi

