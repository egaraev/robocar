#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/MotorService.py" | grep -v grep > /dev/null; then
	echo "MotorModule is running"
else
    echo "Start MotorModule service"
    nohup /usr/bin/python3 /home/eldar/robocar/MotorService.py &
fi 

if ps -ef | egrep -i "/home/eldar/robocar/Obstacle_avoidance.py" | grep -v grep > /dev/null; then
	echo "Obstacle_avoidance is running"
else
    echo "Start Obstacle_avoidance service"
    nohup /usr/bin/python3 /home/eldar/robocar/Obstacle_avoidance.py &  
fi 

if ps -ef | egrep -i "/home/eldar/robocar/Line_Detection.py" | grep -v grep > /dev/null; then
	echo "Line_Detection.py is running"
else
    echo "Start Line_Detection.py service"
    nohup /usr/bin/python3 /home/eldar/robocar/Line_Detection.py &
fi 