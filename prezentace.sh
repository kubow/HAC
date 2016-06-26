#!/bin/sh

direct=${PWD}
mainHTML=${direct}'/index.html'
subHTML=${direct}'/Presenter/index.html'

echo '<html>' > $mainHTML
echo '<head>' >> $mainHTML
echo '	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' >> $mainHTML
echo '	<title>Prezentace</title>' >> $mainHTML
echo '	<link rel="stylesheet" type="text/css" href="Reader/style.css">' >> $mainHTML
echo '</head>' >> $mainHTML
echo '<body>' >> $mainHTML

echo '<div id="frame"><iframe src="Presenter/index.html" width="100%%" height="100%%"></iframe></div>' >> $mainHTML
echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100">' >> $mainHTML
#echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3">' >> $mainHTML
cat  ${direct}'/Presenter/text.txt' >> $mainHTML
echo '</marquee></div>' >> $mainHTML
echo '</body>' >> $mainHTML
echo '</html>' >> $mainHTML

# echo $subHTML

cat ${direct}'/Presenter/HTML_head.txt' > $subHTML
for f in ${direct}/Presenter/image/*
do
	echo '<li>' >> $subHTML
	echo '<span class="Centerer"></span>' >> $subHTML
	echo '<img class="Centered" src="image\'${f##*/}'" alt="X"/>' >> $subHTML
	echo '</li>' >> $subHTML
done
cat ${direct}'/Presenter/HTML_tail.txt' >> $subHTML
