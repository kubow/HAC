#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'
subHTML=${PWD}'/Multimedia/presenting.html'

cat ${PWD}'/Structure/HTML_Base_head.txt' > $mainHTML
for line in $(sqlite3 ${PWD}/System/Reader/Reader.db 'select Shortcut,Address,ZomatoAddress,Tag from RestActive'); do
	#http://stackoverflow.com/questions/10520623/how-to-split-one-string-into-multiple-variables-in-bash-shell
	echo $line
	IFS='|' read -r shc add zom tag <<< $line
	#https://www.cyberciti.biz/faq/unix-linux-bash-script-check-if-variable-is-empty/
	if [ -z "${add}" ] ; then
		echo ${shc}--"daily-menu-conatiner"@${zom}
	else
		echo ${shc}--${tag}@${add}
	fi
	#python generate htm's
	#echo python ${PWD}'/System/Reader/Reader.py '${shc}
	python ${PWD}/System/Reader/Reader.py ${shc}
	echo ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
done

cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $mainHTML

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
