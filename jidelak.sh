#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'
mlt_dir=${PWD}'/Multimedia/'
py_file=${PWD}'/System/SO74.py'

python ${py_file} -g restaurant -w ${PWD} -l ${mlt_dir}logfile.log

cat ${PWD}'/Structure/HTML_Base_head.txt' > ${mainHTML}
echo '<div id="frame"><iframe src="Multimedia/showing1.htm" width="100%%" height="100%%"></iframe></div>' >> ${mainHTML}
echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100">' >> ${mainHTML}
cat ${mlt_dir}text_horni_lista.txt >> ${mainHTML}
echo '</marquee></div>' >> ${mainHTML}
echo '</body>' >> ${mainHTML}
echo '</html>' >> ${mainHTML}

#for line in $(sqlite3 ${PWD}/System/DataReaderWeb.db 'select Shortcut,Address,ZomatoAddress,Tag from RestActive'); do
	#http://stackoverflow.com/questions/10520623/how-to-split-one-string-into-multiple-variables-in-bash-shell
	#echo $line
	#IFS='|' read -r shc add zom tag <<< $line
	#https://www.cyberciti.biz/faq/unix-linux-bash-script-check-if-variable-is-empty/
	#if [ -z "${add}" ] ; then
		#echo "daily-menu-conatiner"@${zom}
	#else
		#echo ${tag}@${add}
	#fi
	#python generate htm's
	#echo python ${PWD}'/System/DataReaderWeb.py '${shc}
	#python ${PWD}/System/DataReaderWeb.py ${shc}
	#echo ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#done

#alternative version using command line
#http://www.cyberciti.biz/faq/unix-linux-get-the-contents-of-a-webpage-in-a-terminal/
#http://blog.mattwynne.net/2008/04/26/fetch-and-parse-html-web-page-content-from-bash-wow/
#page=$(curl http://restaurace-trpaslik.webnode.cz/poledni-menu/)
#inner=$(xmllint --xpath "//body")
#echo $page
#http://stackoverflow.com/questions/21015587/bash-get-content-between-a-pair-of-html-tags
#xmllint --xpath "//body/node()" f.html

#http://stackoverflow.com/questions/10929453/read-a-file-line-by-line-assigning-the-value-to-a-variable
#while read p; do
#  echo $p
#done <peptides.txt
