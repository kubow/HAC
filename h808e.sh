#!/bin/bash
# same menu as in batch
# decide if dialog installed (debian, ubuntu)
runflag=1
# Loop forever (until break is issued)
while true; do
	#if [ "$runflag" -eq "0" ]; then
	#	echo "must quit..."
	#else
		#clear the screen
		clear
		#show the menu
		echo "============= -H_808_E- ============="
		echo "-------------------------------------"
		echo "1.  Open encyklopedia cherrytree"
		echo "2.  Open encyklopedia sqlite browser"
		echo "3.  Directory synchronizer"
		echo "4.  Generate structure from db"
		echo "5.  A"
		echo "6.  B"
		echo "7.  C"
		echo "-------------------------------------"
		echo "8.  Universal python project"
		echo "-------------------------------------"
		echo "9.  Browse pages in (FF/CH/IE)"
		echo "-------------------------------------"
		echo "==========PRESS 'Q' TO QUIT=========="

		options=("1" "2" "3" "4" "5" "6" "7" "8" "9" "0")
		PS3="Please select a number:"
		select opt in "${options[@]}"
		do 
			case $opt in
				"1" ) cherrytree;;
				"2" ) sqlitebrowser;;
				"3" ) echo "for all files in directory: /home/kubow/Dokumenty/Web";;
				"4" ) python /home/kubow/Dokumenty/H808E_gen.py;;
				"5" ) echo "Y";;
				"6" ) echo "You $opt";;
				"7" ) echo "Youked $opt";;
				"8" ) echo "You pic $opt";;
				"9" ) echo "You pcd $opt";;
				"0" ) echo "You picked $opt which is option $REPLY";;
				*) echo invalid option
			esac
		done
	#fi
done

