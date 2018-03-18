#!/bin/bash
#!/usr/bin python

mainHTML=${PWD}'/index.html'
mlt_dir=${PWD}'/Multimedia/'
menu_dir=${mlt_dir}'RestMenu/'
py_file=${PWD}'/System/SO74.py'

if [ -d "${menu_dir}" ]; then
    echo 'directory exists'
    rm -rf "${menu_dir}*" || true
else
    
    mkdir -p "${menu_dir}"
fi

python ${py_file} -m restaurant -i ${PWD} -l ${mlt_dir}logfile.log

cat ${PWD}'/Structure/HTML_Base_head.txt' > "${mainHTML}"

echo '<div id="top"><marquee behavior="scroll" direction="left" scrolldelay="100">' >> "${mainHTML}"
cat ${mlt_dir}text_horni_lista.txt >> "${mainHTML}"
echo '</marquee></div>' >> "${mainHTML}"

echo '<div id="frame"><iframe id="Left" src="Multimedia/RestMenu/zat.htm" width="49%" height="100%"></iframe>' >> "${mainHTML}"
echo '  <iframe id="Right" src="Multimedia/RestMenu/bla.html" width="49%" height="100%"></iframe></div>' >> "${mainHTML}"

#echo '<button onclick="loadPages()">Click Me</button>' >> "${mainHTML}"
echo '<script>' >> "${mainHTML}"
echo '   window.setInterval(function(){' >> "${mainHTML}"
echo '   /// call your function here' >> "${mainHTML}"
echo '   /// var left = "Multimedia/RestMenu/zat.html";' >> "${mainHTML}"
echo '   /// var right = "Multimedia/RestMenu/sad.html";' >> "${mainHTML}"

echo '    var srcs = [' >> "${mainHTML}"

for dir in ${mlt_dir}RestMenu/*/
do
    dir=${dir%*/}
    echo ' "${dir##*/} , "' >> "${mainHTML}"
done
echo '   ]' >> "${mainHTML}"

echo '   document.getElementById("Left").setAttribute("src", srcs[Math.floor(Math.random() * srcs.length));' >> "${mainHTML}"
echo '   document.getElementById("Right").setAttribute("src", srcs[Math.floor(Math.random() * srcs.length));' >> "${mainHTML}"
echo '   // document.getElementById("Left").src += document.getElementById('Left').src;' >> "${mainHTML}"
echo '   // document.getElementById("Right").src += document.getElementById('Right').src;' >> "${mainHTML}"
echo '   document.getElementById("west").innerHTML = document.getElementById("Left").contentDocument.title;' >> "${mainHTML}"
echo '   document.getElementById("east").innerHTML = document.getElementById("Right").contentDocument.title;' >> "${mainHTML}"
echo '   }, 10000);' >> "${mainHTML}"
echo '</script>' >> "${mainHTML}"


echo '</body>' >> "${mainHTML}"
echo '</html>' >> "${mainHTML}"


