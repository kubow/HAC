@echo on
echo "P:\\czprg1-stor\Projects"
call net use p: "\\CZPRG1-STOR\Projects"

echo "W: "\\CZPRG1-STOR\_work"
call net use w: "\\CZPRG1-STOR\_work"

echo "t:99320100 - Water distribution tools"
call net use t: "\\czprg1-stor.hif.cz\Projects\99320100"

echo "i:Software install"
call net use i: "\\czprg1-stor\Projects\99320001\Install"

echo "a:DHICZ UWD Archive"
call net use a: "\\czprg1-stor\projects\32098092-99"

echo "e:32019130 - Education CZ-SOL"
call net use e: "\\czprg1-stor.hif.cz\Projects\32019130"

echo "s:99320000 - Static data "
call net use s: "\\czprg1-stor.hif.cz\Projects\99320000"

echo "m:32019632 - Monitoring"
call net use m: "\\czprg1-stor.hif.cz\Projects\32019632"

echo "Y: WD MyBookLive"
call net use Y: "\\MyBookLive\Public"
exit
