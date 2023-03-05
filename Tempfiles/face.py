import cv2
import serial
import time
from CameraModule import VideoCapture
video = VideoCapture()

import signal, sys

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# ArduinoSerial = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0',9600,timeout=0.1)
time.sleep(1)


def signal_handler(signum, frame):
    # handle the signal by stopping the loop
    global stop_flag
    stop_flag = True

signal.signal(signal.SIGTERM, signal_handler)

# start the loop
stop_flag = False

while not stop_flag:
    frame = video.get_frame(display=False)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)
    for x, y, w, h in faces:
        # sending coordinates to Arduino
        string = 'X{0:d}Y{1:d}'.format((x+w//2), (y+h//2))
        print(string)
        # ArduinoSerial.write(string.encode('utf-8'))
        # plot the center of the face
        cv2.circle(frame, (x+w//2, y+h//2), 2, (0, 255, 0), 2)
        # plot the roi
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
    # plot the squared region in the center of the screen
    cv2.rectangle(frame, (640//2-30, 480//2-30), (640//2+30, 480//2+30), (255, 255, 255), 3)
    cv2.imshow('img', frame)
    # press q to Quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
