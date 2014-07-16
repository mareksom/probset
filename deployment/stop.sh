#!/bin/bash

PID=`ps aux | grep "uwsgi --ini /home/others/wic2014-probset/probset/deployment/uwsgi.ini" | grep -v grep | cut -c10-14`
for i in $PID
do
	kill -9 $i
	echo "Killed $i"
done
