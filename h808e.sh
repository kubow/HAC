#!/bin/bash
# same menu as in batch
# repeated menu with 9 custom selections

### display main menu ###
dialog --clear --help-button --backtitle "Linux Shell Script Tutorial" \
--title "============= -H_808_E- =============" \
--menu "-------------------------------------"15 50 4 \
CherryTree "1. Open encyklopedia cherrytree" \
SQLite "2. Open encyklopedia sqlite browser" \
DirSync "3. Directory synchronizer" \
Structure "4. Generate structure" \
A "5. A" \
B "6. B" \
C "7. C" \
UniPy "8.  Universal python project" \
BrowsePages "9. Browse pages in (FF/CH/IE)" \
Exit "Exit to the shell" 2>"${INPUT}"

menuitem=$(<"${INPUT}") 

# make decission
case $menuitem in
	CherryTree) show_date;;
	SQLite) show_calendar;;
	DirSync) $vi_editor;;
	Structure) $vi_editor;;
	DirSync) $vi_editor;;
	A) continue;;
	B) continue;;
	C) continue;;
	UniPy) continue;;
	BrowsePages) continue;;
	Exit) echo "Bye"; break;;
esac
