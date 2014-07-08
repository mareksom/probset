#!/bin/bash

PID=`ps aux | grep "uwsgi --ini uwsgi.ini" | grep -v grep | cut -c10-14`
for i in $PID
do
	kill -9 $i
	echo "Killed $i"
done
uwsgi --ini uwsgi.ini > /dev/null 2> /dev/null &
PID=`ps aux | grep "uwsgi --ini uwsgi.ini" | grep -v grep | cut -c10-14 | head -n 1`
echo "Now $PID"
