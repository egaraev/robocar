#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/Line_Follow.py" | grep -v grep > /dev/null; then
	echo "Line_Follow is running, lets stop it"
    pkill -f 'Line_Follow.py'
else
    echo "There is no Follow Line module running, exiting"
 
fi 
