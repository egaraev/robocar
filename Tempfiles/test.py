import cv2
import serial
import time
from CameraModule import getImg
import signal, sys



def signal_handler(signum, frame):
    # handle the signal by stopping the loop
    global stop_flag
    stop_flag = True

signal.signal(signal.SIGTERM, signal_handler)

# start the loop
stop_flag = False

while not stop_flag:
    frame = getImg(display=False)
    cv2.imshow('img', frame)
    # press q to Quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
