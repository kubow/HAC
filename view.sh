log_file=${PWD}/Multimedia/logfile.log

if [ "$1" = "h" ] # HANA
then
    py_file=hdbalm.py
    echo 'python '${py_file}
    python ${py_file}
elif [ "$1" = "s" ] # SQLite
then
    py_file=${PWD}/System/SO74DB.py
    echo 'python '${py_file}' -a '$2' -l '${log_file}
    python ${py_file} -a $2 -l ${log_file}
elif [ "$1" = "t" ] # text file
then
    py_file=${PWD}/System/SO74TX.py
    python ${py_file} -i $2 -l ${log_file}
elif [ "$1" = "b" ] # directory
then
    py_file=${PWD}/System/OS74.py
    echo 'python '${py_file}' -m -m True/False -i '$2' -l '${log_file}
    python ${py_file} -m True -i $2 -l ${log_file}
elif [ "$1" = "l" ] # list directory files
then
    py_file=${PWD}/System/OS74.py
    echo 'python '${py_file}' -m -m True/False -i '$2' -l '${log_file}
    python ${py_file} -m -i $2 -l ${log_file}
if [ "$1" = "r" ] # rss
then
    py_file=${PWD}/System/SO74.py
    echo 'python '${py_file}' -g rss -w '${PWD}' -l '${log_file}
    python ${py_file} -g rss -w ${PWD} -l ${log_file}
else
    echo '1st parameter:'
    echo '- DATABASE MODE -'
    echo 'h - HANA '
    echo 's - SQLite'
    echo '- FILE MODE -'
    echo 't - pure text file'
    echo '- FOLDER MODE - '
    echo 'b - browse folders'
    echo 'l - list folder files'
    echo '- WEB MODE -'
    echo 'r - rss feed display'
    echo '2nd parameter: object location'
fi
