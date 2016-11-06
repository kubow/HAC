#!/bin/sh

mainHTML=${PWD}'/index.html'
subHTML=${PWD}'/Reader/index.html'

#[]

cat ${PWD}'/Reader/HTML_head.txt' > $subHTML

python
#http://www.cyberciti.biz/faq/unix-linux-get-the-contents-of-a-webpage-in-a-terminal/
#http://blog.mattwynne.net/2008/04/26/fetch-and-parse-html-web-page-content-from-bash-wow/
page=$(curl http://www.cyberciti.biz/faq/bash-for-loop/)
page=$(curl http://restaurace-trpaslik.webnode.cz/poledni-menu/)

inner=$(xmllint --xpath "//body")
echo $page

#http://stackoverflow.com/questions/10929453/read-a-file-line-by-line-assigning-the-value-to-a-variable
#while read p; do
#  echo $p
#done <peptides.txt
#http://stackoverflow.com/questions/21015587/bash-get-content-between-a-pair-of-html-tags
#xmllint --xpath "//body/node()" f.html

