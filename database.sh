log_file=${PWD}/Multimedia/logfile.log
mlt_dir='/home/kubow/Dokumenty/Web/'
py_for_file=${PWD}/System/OS74.py

# '-b', help='browse dir', type=str, default='')
# '-l', help='list dir', type=str, default='')
# '-f', help='file output', type=str, default='')
echo 'python '${py_for_file}' -b '${mlt_dir}' -f '${log_file}
python ${py_for_file} -b ${mlt_dir} -f ${log_file}
