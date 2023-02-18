#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/UltrasonicModule.py" | grep -v grep > /dev/null; then
	echo "Obstacle avoidance is running"
else
    echo "Start Obstacle Avoidance service"
    nohup /usr/bin/python3 /home/eldar/robocar/UltrasonicModule.py &  
fi 
