#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/MotorModuleMqtt.py" | grep -v grep > /dev/null; then
	echo "MotorModule is running"
else
    echo "Start MotorModule service"
    nohup /usr/bin/python3 /home/eldar/robocar/MotorModuleMqtt.py &  
fi 
