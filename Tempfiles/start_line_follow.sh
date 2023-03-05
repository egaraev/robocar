#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/InfraredModule.py" | grep -v grep > /dev/null; then
	echo "InfraredModule is running"
else
    echo "Start InfraredModule service"
    nohup /usr/bin/python3 /home/eldar/robocar/InfraredModule.py &
fi 
