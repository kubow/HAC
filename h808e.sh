#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
script_path=`dirname $(readlink -f $0)`
media_path=$( realpath ${script_path}/../Web/64/Astrologie/ )
if [ ! -d "${media_path}" ]; then
  media_path=$( realpath ${script_path}/../Web/ )
fi
db_path=$( realpath ${script_path}/../H808E.ctb )
echo "running from "${parent_path}" - watch directory: "${media_path}" - enc database: "${db_path}

# calling batch menu (platform independent)
${script_path}/System/H808E.py -d ${media_path} -c ${db_path} -l ${script_path}/Multimedia/logfile.log
