log_file=${PWD}/Multimedia/logfile.log

if [ "$1" = "b" ] # directory
then
    mlt_dir='/home/kubow/Dokumenty/Web/'
    py_file=${PWD}/System/OS74.py

    # '-i', help='input dir', type=str, default='')
    # '-o', help='output dir', type=str, default='')
    # '-l', help='log file', type=str, default='')
    echo 'python '${py_file}' -m graphic -i '${mlt_dir}' -l '${log_file}
    python ${py_file} -m graphic -i ${mlt_dir} -l ${log_file}
elif [ "$1" = "s" ]
then
    py_file=${PWD}/System/SO74DB.py
    mlt_dir=$2
    echo 'python '${py_file}' -a '${mlt_dir}' -l '${log_file}
    python ${py_file} -a ${mlt_dir} -l ${log_file}
else
    echo "1st argument - cycle type"
    echo "    b - Browse directory"
    echo "    s - SQLite database file"
fi
