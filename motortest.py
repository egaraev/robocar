import RPi.GPIO as GPIO
from time import sleep

leftForward = 2
leftBackward = 3
leftEnable = 4

rightForward = 17
rightBackward = 22
rightEnable = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

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

while True:
    GPIO.output(leftForward, GPIO.HIGH)
    GPIO.output(rightForward, GPIO.HIGH)
    sleep(1)
    leftEnPWM.ChangeDutyCycle(100)
    rightEnPWM.ChangeDutyCycle(100)
    sleep(1)
    leftEnPWM.ChangeDutyCycle(50)
    rightEnPWM.ChangeDutyCycle(50)
    sleep(1)
    GPIO.output(leftForward, GPIO.LOW)
    GPIO.output(rightForward, GPIO.LOW)
    sleep(1)

    GPIO.output(leftBackward, GPIO.HIGH)
    GPIO.output(rightBackward, GPIO.HIGH)
    sleep(1)
    leftEnPWM.ChangeDutyCycle(100)
    rightEnPWM.ChangeDutyCycle(100)
    sleep(1)
    leftEnPWM.ChangeDutyCycle(50)
    rightEnPWM.ChangeDutyCycle(50)
    sleep(1)
    GPIO.output(leftBackward, GPIO.LOW)
    GPIO.output(rightBackward, GPIO.LOW)
    sleep(1)