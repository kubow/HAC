#!/bin/sh

presName=Multimedia
tempName=Structure
presDir=${PWD}'/'${presName}
tempDir=${PWD}'/'${tempName}
mainHTML=${PWD}'/index.html'
subHTML=${PresDir}'/index.html'

echo '<html>' > $mainHTML
echo '<head>' >> $mainHTML
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' >> $mainHTML
echo '  <title>Prezentace</title>' >> $mainHTML
echo '  <link rel="stylesheet" type="text/css" href="'${tempName}'/style.css">' >> $mainHTML
echo '</head>' >> $mainHTML
echo '<body>' >> $mainHTML
echo '<div id="frame"><iframe src="'${presName}'/index.html" width="100%%" height="100%%"></iframe></div>' >> $mainHTML
echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100">' >> $mainHTML
#echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3">' >> $mainHTML
cat  ${PresDir}'/text.txt' >> $mainHTML
echo '</marquee></div>' >> $mainHTML
echo '</body>' >> $mainHTML
echo '</html>' >> $mainHTML

# echo 'Presenting images ...'

cat ${tempDir}'/HTML_Presenter_head.txt' > $subHTML
for f in ${PresDir}'/image/*'
do
    echo '<li>' >> $subHTML
    echo '<span class="Centerer"></span>' >> $subHTML
    echo ${PresDir}'/image/'${f##*/}
    echo '<img class="Centered" src="image\' >> $subHTML
    echo ${f##*/}'" alt="X"/>' >> $subHTML
    echo '</li>' >> $subHTML
done
cat ${tempDir}'/HTML_Presenter_tail.txt' >> $subHTML
