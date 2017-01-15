#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'

for line in $(sqlite3 ${PWD}/System/Reader/Reader.db 'select Shortcut,Address,ZomatoAddress,Tag from RestActive'); do
	#http://stackoverflow.com/questions/10520623/how-to-split-one-string-into-multiple-variables-in-bash-shell
	#echo $line
	IFS='|' read -r shc add zom tag <<< $line
	#https://www.cyberciti.biz/faq/unix-linux-bash-script-check-if-variable-is-empty/
	if [ -z "${add}" ] ; then
		echo "daily-menu-conatiner"@${zom}
	else
		echo ${tag}@${add}
	fi
	#python generate htm's
	#echo python ${PWD}'/System/Reader/Reader.py '${shc}
	python ${PWD}/System/Reader/Reader.py ${shc}
	echo Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨Â¨
done

cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $subHTML1
cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $subHTML2
cat ${PWD}'/Structure/HTML_Base_tail.txt' >> $subHTML3

