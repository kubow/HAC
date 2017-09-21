if [[ $# -eq 0 ]] 
then
    echo "Please supply location to a text file"
else
    python ./System/SO74TX.py -i $1 -l ./Multimedia/logfile.log
fi
