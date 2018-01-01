#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
media_path=$( realpath ../Web/64/Astrologie/ )
db_path=$( realpath ../H808E.ctb )
echo "running from "${parent_path}" - watch directory: "${media_path}" - enc database: "${db_path}
# calling batch menu (platform independent)
python3 ./System/H808E.py -d ${media_path} -c ${db_path} -l ./Multimedia/logfile.log
