#!/bin/bash
# Script to check system load average levels to try to determine what processes are taking it overly high...
# set environment
dt=`date +%d%b%Y-%X`
# Obviously, change the following directories to where your log files actually are kept
tmpfile="/tmp/checkSystemLoad.tmp"
logfile="/tmp/checkSystemLoad.log"
msgLog="/var/log/messages"
mysqlLog="/var/log/mysqld.log"
# the first mailstop is standard email for reports. Second one is for cell phone (with a pared down report)
mailstop="sysadmin@mydomain.com"
mailstop1="15555555555@mycellphone.com"
machine=`hostname`

# The following three are for mytop use - use a db user that has decent rights
dbusr="username"
dbpw="password"
db="yourdatabasename"
# The following is the load level to check on - 10 is really high, so you might want to lower it.
levelToCheck=10

# Set variables from system:
loadLevel=`cat /proc/loadavg | awk '{print $1}'`
loadLevel=$( printf "%0.f" $loadLevel )
echo 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

# if the load level is greater than you want, start the script process. Otherwise, exit 0
echo $loadLevel
if [ $loadLevel -gt $levelToCheck ]; then
echo "" > $tmpfile
echo 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
echo "**************************************" >>$tmpfile
echo "Date: $dt " >>$tmpfile
echo "Check System Load & Processes " >>$tmpfile
echo "**************************************" >>$tmpfile

# Get more variables from system:
httpdProcesses=`ps -def | grep httpd | grep -v grep | wc -l`

# Show current load level:
echo "Load Level Is: $loadLevel" >>$tmpfile
echo "*************************************************" >>$tmpfile

# Show number of httpd processes now running (not including children):
echo "Number of httpd processes now: $httpdProcesses" >>$tmpfile
echo "*************************************************" >>$tmpfile
echo "" >>$tmpfile

# Show process list:
echo "Processes now running:" >>$tmpfile
ps f -ef >>$tmpfile
echo "*************************************************" >>$tmpfile
echo "" >>$tmpfile

# Show current MySQL info:
echo "Results from mytop:" >>$tmpfile
/usr/bin/mytop -u $dbusr -p $dbpw -b -d $db >>$tmpfile
echo "*************************************************" >>$tmpfile
echo "" >>$tmpfile

# Show current connections:
echo "netstat now shows:" >>$tmpfile
/bin/netstat -p >>$tmpfile
echo "*************************************************" >>$tmpfile
echo "" >>$tmpfile

# Check disk space
echo "disk space:" >>$tmpfile
/bin/df -k >>$tmpfile
echo "*************************************************" >>$tmpfile
echo "" >>$tmpfile

# Send results to log file:
/bin/cat $tmpfile >>$logfile

# And email results to sysadmin:
/usr/bin/mutt -s "$machine has a high load level! - $dt" -a $mysqlLog -a $msgLog $mailstop <$tmpfile /usr/bin/mutt -s "$machine has a high load level! - $dt" $mailstop1 <$topfile echo "**************************************" >>$logfile

# And then remove the temp file:
rm $tmpfile
rm $topfile
fi

#
exit 0
