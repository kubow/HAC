py_file=${PWD}/System/SO74.py
log_file=${PWD}/Multimedia/logfile.log
execute_py()
{
    echo 'python '${py_file}' -m '${mode_name}' -i '${in_object}' -e '${extra_name}' -l '${log_file}
    python ${py_file} -m ${mode_name} -i ${in_object} -e ${extra_name} -l ${log_file}
}
if [ "$1" = "h" ]; then # HANA
    py_file=hdbalm.py
        echo 'python '${py_file}
    python ${py_file}
elif [ "$1" = "s" ]; then # SQLite
    mode_name="browser"
    extra_name="database"
    in_object=$2
    execute_py
elif [ "$1" = "t" ]; then # text file
    mode_name="browser"
    extra_name="text"
    in_object=$2
    execute_py
elif [ "$1" = "b" ]; then # directory
    mode_name="browser"
    extra_name="directory"
    in_object=$2
    execute_py
elif [ "$1" = "l" ]; then # list directory files
    mode_name="lister"
    extra_name="directory"
    in_object=$2
    execute_py
elif [ "$1" = "r" ]; then # rss
    mode_name="browser"
    extra_name="rss"
    in_object=$2
    execute_py
elif [ "$1" = "w" ]; then # web
    mode_name="browser"
    extra_name="web"
    in_object=$2
    execute_py
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
    echo '  w - web address display'
    echo '2nd parameter: object location'
fi

