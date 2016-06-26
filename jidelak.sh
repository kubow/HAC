#http://stackoverflow.com/questions/10929453/read-a-file-line-by-line-assigning-the-value-to-a-variable
while read p; do
  echo $p
done <peptides.txt
#http://www.cyberciti.biz/faq/unix-linux-get-the-contents-of-a-webpage-in-a-terminal/
page="$(curl http://www.cyberciti.biz/faq/bash-for-loop/)"
#http://stackoverflow.com/questions/21015587/bash-get-content-between-a-pair-of-html-tags
xmllint --xpath "//body/node()" f.html

