#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'
mlt_dir=${PWD}'/Multimedia/'
py_file=${PWD}'/System/SO74.py'

rm ${mlt_dir}RestMenu/*
python ${py_file} -g restaurant -w ${PWD} -l ${mlt_dir}logfile.log

cat ${PWD}'/Structure/HTML_Base_head.txt' > ${mainHTML}

echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100">' >> ${mainHTML}
cat ${mlt_dir}text_horni_lista.txt >> ${mainHTML}
echo '</marquee></div>' >> ${mainHTML}

echo '<div id="frame"><iframe id="Left" src="Multimedia/RestMenu/zat.htm" width="49%" height="100%"></iframe>' >> ${mainHTML}
echo '  <iframe id="Right" src="Multimedia/RestMenu/bla.html" width="49%" height="100%"></iframe></div>' >> ${mainHTML}

echo '<button onclick="loadPages()">Click Me</button>' >> ${mainHTML}
echo '<script>' >> ${mainHTML}
echo '   function loadPages(){' >> ${mainHTML}
echo '       var left = "Multimedia/RestMenu/zat.html";' >> ${mainHTML}
echo '       var right = "Multimedia/RestMenu/sad.html";' >> ${mainHTML}

echo "       document.getElementById('Left').setAttribute('src', left);" >> ${mainHTML}
echo "       document.getElementById('Right').setAttribute('src', right);" >> ${mainHTML}
echo '    }' >> ${mainHTML}
echo '</script>' >> ${mainHTML}

echo '</body>' >> ${mainHTML}
echo '</html>' >> ${mainHTML}


