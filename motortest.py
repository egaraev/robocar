import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

leftForward = 17
leftBackward = 22
leftEnable = 27

rightForward = 4
rightBackward = 3
rightEnable = 2



GPIO.setup(leftForward, GPIO.OUT)
GPIO.setup(leftBackward, GPIO.OUT)
GPIO.setup(leftEnable, GPIO.OUT)
GPIO.setup(rightForward, GPIO.OUT)
GPIO.setup(rightBackward, GPIO.OUT)
GPIO.setup(rightEnable, GPIO.OUT)

leftEnPWM = GPIO.PWM(leftEnable, 100)
leftEnPWM.start(50)
GPIO.output(leftEnable, GPIO.HIGH)

rightEnPWM = GPIO.PWM(rightEnable, 100)
rightEnPWM.start(50)
GPIO.output(rightEnable, GPIO.HIGH)


GPIO.output(leftForward, GPIO.HIGH)
GPIO.output(rightForward, GPIO.HIGH)
sleep(5)
leftEnPWM.ChangeDutyCycle(100)
rightEnPWM.ChangeDutyCycle(100)
#sleep(5)
#leftEnPWM.ChangeDutyCycle(50)
#rightEnPWM.ChangeDutyCycle(50)
sleep(5)
GPIO.output(leftForward, GPIO.LOW)
GPIO.output(rightForward, GPIO.LOW)
sleep(5)

#GPIO.output(leftBackward, GPIO.HIGH)
#GPIO.output(rightBackward, GPIO.HIGH)
#sleep(5)
#leftEnPWM.ChangeDutyCycle(100)
#rightEnPWM.ChangeDutyCycle(100)
#sleep(5)
#leftEnPWM.ChangeDutyCycle(50)
#rightEnPWM.ChangeDutyCycle(50)
#sleep(5)
#GPIO.output(leftBackward, GPIO.LOW)
#GPIO.output(rightBackward, GPIO.LOW)
#sleep(5)