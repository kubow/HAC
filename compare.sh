log_file=${PWD}/Multimedia/logfile.log
if [ "$1" = "b" ]
then
    py_file=${PWD}/System/SO74DB.py
    echo 'python '${py_file}' -m compare -l '$2' -r '$3' -f table_name'
    python ${py_file} -m compare -l $2 -r $3 -f node
elif [ "$1" = "d" ]
then
    mlt_dir='/home/kubow/Dokumenty/Web/'
    py_file=${PWD}/System/OS74.py
    # '-b', help='browse dir', type=str, default='')
    # '-l', help='list dir', type=str, default='')
    # '-f', help='file output', type=str, default='')
    echo 'python '${py_file}' -b '${mlt_dir}' -f '${log_file}
    python ${py_file} -b ${mlt_dir} -f ${log_file}
elif [ "$1" = "t" ]
then
    echo "text mode"
else
    echo "1st argument - compare type"
    echo "    b - dataBase"
    echo "    d - Direcotry"
    echo "    t - Text version"
    echo "2nd argument - source file/folder"
    echo "3rd argument - destination file/folder"
fi

