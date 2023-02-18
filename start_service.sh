#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/MotorModuleMqtt.py" | grep -v grep > /dev/null; then
	echo "MotorModule is running"
else
    echo "Start MotorModule service"
    nohup /usr/bin/python3 /home/eldar/robocar/MotorModuleMqtt.py &  
fi 

if ps -ef | egrep -i "/home/eldar/robocar/Obstacle_avoidance.py" | grep -v grep > /dev/null; then
	echo "Obstacle_avoidance is running"
else
    echo "Start Obstacle_avoidance service"
    nohup /usr/bin/python3 /home/eldar/robocar/Obstacle_avoidance.py &  
fi 

if ps -ef | egrep -i "/home/eldar/robocar/IRModule.py" | grep -v grep > /dev/null; then
	echo "IRModule.py is running"
else
    echo "Start IRModule.py service"
    nohup /usr/bin/python3 /home/eldar/robocar/IRModule.py &  
fi 