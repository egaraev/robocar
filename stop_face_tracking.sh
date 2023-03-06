#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/FaceTrackingModule.py" | grep -v grep > /dev/null; then
	echo "FaceTrackingModule is running, lets stop it"
    pkill -f 'FaceTrackingModule.py'
else
    echo "There is no FaceTrackingModule running, exiting"
 
fi 
