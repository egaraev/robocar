#!/usr/bin/bash

if ps -ef | egrep -i "/home/eldar/robocar/MotorService.py" | grep -v grep > /dev/null; then
	echo "MotorModule is running"
else
    echo "Start MotorModule service"
    nohup /usr/bin/python3 /home/eldar/robocar/MotorService.py &
fi 

if ps -ef | egrep -i "/home/eldar/robocar/UltrasonicSensor.py" | grep -v grep > /dev/null; then
	echo "UltrasonicSensor is running"
else
    echo "Start UltrasonicSensor service"
    nohup /usr/bin/python3 /home/eldar/robocar/UltrasonicSensor.py &
fi

if ps -ef | egrep -i "/home/eldar/robocar/InfraRedSensor.py" | grep -v grep > /dev/null; then
	echo "InfraRedSensor is running"
else
    echo "Start InfraRedSensor service"
    nohup /usr/bin/python3 /home/eldar/robocar/InfraRedSensor.py &
fi

if ps -ef | egrep -i "/home/eldar/robocar/ServoService.py" | grep -v grep > /dev/null; then
	echo "ServoService is running"
else
    echo "Start ServoService service"
    nohup /usr/bin/python3 /home/eldar/robocar/ServoService.py &
fi