log_file=${PWD}/Multimedia/logfile.log
py_file=${PWD}/System/SO74.py
mode_name="compare"
execute_py()
{
    echo 'python '${py_file}' -m '${mode_name}' -i '${in_object}' -o '${out_object}' -e '${extra_name}' -l '${log_file}
    python ${py_file} -m ${mode_name} -i ${in_object} -o ${out_object} -e ${extra_name} -l ${log_file}
}
if [ "$1" = "b" ]; then
    in_object=$2
    out_object=$3
    extra_name="database"
    execute_py  
elif [ "$1" = "d" ]; then
    in_object=$2
    out_object=$3
    extra_name="directory"
    execute_py 
elif [ "$1" = "t" ]; then
    in_object=$2
    out_object=$3
    extra_name="text"
    execute_py
else
    echo "1st argument - compare type"
    echo "    b - dataBase"
    echo "    d - Direcotry/file"
    echo "    t - Text version"
    echo "2nd argument - source file/folder"
    echo "3rd argument - destination file/folder"
fi

