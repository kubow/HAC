mainHTML=${PWD}/index.html
mlt_dir=${PWD}'/Multimedia/'
py_for_file=${PWD}/System/SO74.py

python ${py_for_file} -g rss -w ${PWD} -l ${mlt_dir}logfile.log
