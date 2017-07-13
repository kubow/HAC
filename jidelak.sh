#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'
#subHTML=${PWD}'/Multimedia/presenting.html'
subHTML1=${PWD}'/Multimedia/showing1.html'
subHTML2=${PWD}'/Multimedia/showing2.html'
subHTML3=${PWD}'/Multimedia/showing3.html'

python ${PWD}/System/SO74.py -g 1 -w ${PWD}/Multimedia

#cat ${PWD}'/Structure/HTML_Base_head.txt' > $subHTML1
#cat ${PWD}'/Structure/HTML_Base_head.txt' > $subHTML2
#cat ${PWD}'/Structure/HTML_Base_head.txt' > $subHTML3

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

#cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $subHTML1
#cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $subHTML2
#cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $subHTML3

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
