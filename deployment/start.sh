#!/bin/bash

uwsgi --ini /home/others/probset/probset/deployment/uwsgi.ini > /dev/null 2> /dev/null &
PID=`ps aux | grep "uwsgi --ini /home/others/probset/probset/deployment/uwsgi.ini" | grep -v grep | cut -c10-14 | head -n 1`
echo "Now $PID"
