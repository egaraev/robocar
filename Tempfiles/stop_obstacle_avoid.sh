#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/UltrasonicModule.py" | grep -v grep > /dev/null; then
	echo "Obstacle avoid is running, lets stop it"
    pkill -f 'UltrasonicModule.py'
else
    echo "There is no Obstacle avoid  module running, exiting"
 
fi 
