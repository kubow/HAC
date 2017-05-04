#!/bin/sh

presName=Multimedia
tempName=Structure
presDir=${PWD}'/'${presName}
tempDir=${PWD}'/'${tempName}
mainHTML=${PWD}'/index.html'
subHTML=${presDir}'/presenting.html'

echo '<html>' > $mainHTML
echo '<head>' >> $mainHTML
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' >> $mainHTML
echo '  <title>Prezentace</title>' >> $mainHTML
echo '  <link rel="stylesheet" type="text/css" href="'${tempName}'/style.css">' >> $mainHTML
echo '</head>' >> $mainHTML
echo '<body>' >> $mainHTML
echo '<div id="frame"><iframe src="'${presName}'/presenting.html" width="100%%" height="100%%"></iframe></div>' >> $mainHTML
echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100">' >> $mainHTML
#echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100" scrollamount="3">' >> $mainHTML
cat  ${presDir}'/text_horni_lista.txt' >> $mainHTML
echo '</marquee></div>' >> $mainHTML
echo '</body>' >> $mainHTML
echo '</html>' >> $mainHTML
cat ${tempDir}'/HTML_Presenter_head.txt' > $subHTML

echo 'list files in directory: '${presDir}'/image/*'
for f in ${presDir}/image/*
do
    echo '<li>' >> $subHTML
    echo '<span class="Centerer"></span>' >> $subHTML
    imagePath='image\'${f##*/}
    echo ${imagePath}
    echo '<img class="Centered" src="'${imagePath}'" alt="X"/>' >> $subHTML
    echo '</li>' >> $subHTML
done
cat ${tempDir}'/HTML_Presenter_tail.txt' >> $subHTML
