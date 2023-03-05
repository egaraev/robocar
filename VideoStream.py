import cv2
import serial
import time
from CameraModule import VideoCapture
import signal, sys

video = VideoCapture()

def signal_handler(signum, frame):
    # handle the signal by stopping the loop
    global stop_flag
    stop_flag = True

signal.signal(signal.SIGTERM, signal_handler)

# start the loop
stop_flag = False

while not stop_flag:
    frame = video.get_frame(display=False)
    cv2.imshow('img', frame)
    # press q to Quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()