#!/usr/bin/bash

FILE=/dev/input/js0
if [ -e "$FILE" ]
then
  echo "$FILE exists."
	if ps -ef | egrep -i "/home/eldar/robocar/JoystickModule.py" | grep -v grep > /dev/null; then
		echo "Joystick is running"
	else
	    echo "Start jopystick service"
   	    #nohup /usr/bin/python3 /home/eldar/robocar/JoystickModule.py &  
	fi 
else 
    echo "$FILE does not exist."
    pkill -f 'JoystickModule.py'
    echo "Removing joystick service"
fi
