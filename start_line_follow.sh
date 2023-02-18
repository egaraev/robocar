#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/Line_Follow.py" | grep -v grep > /dev/null; then
	echo "Line_Follow is running"
else
    echo "Start Line_Follow service"
    nohup /usr/bin/python3 /home/eldar/robocar/Line_Follow.py &  
fi 
