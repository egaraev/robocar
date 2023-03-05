#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/InfraredModule.py" | grep -v grep > /dev/null; then
	echo "InfraredModulew is running, lets stop it"
    pkill -f 'InfraredModule.py'
else
    echo "There is no InfraredModule running, exiting"
 
fi 
