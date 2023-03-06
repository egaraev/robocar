#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/FaceTrackingModule.py" | grep -v grep > /dev/null; then
	echo "FaceTrackingModule.py is running"
else
    echo "Start InfrareFaceTrackingModule.pydModule service"
    /usr/bin/python3 /home/eldar/robocar/FaceTrackingModule.py
fi 
