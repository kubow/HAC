#!/bin/sh
if [ -d "${HOME}/App/jpass/" ]; then
	#jar_file=${HOME}/App/jpass/jpass-0.1.14.jar
	jar_file=$(ls ${HOME}/App/jpass/*.jar)
	echo "running ${jar_file} ... opening ${HOME}/Dropbox/BrainMemory.jpass"
	java -jar ${jar_file} ${HOME}/Dropbox/BrainMemory.jpass
else
	echo "cannot find jpass jar file in ${HOME}/App/jpass/"
fi
