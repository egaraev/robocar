import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

leftForward = 27
leftBackward = 17
leftEnable = 22

rightForward = 4
rightBackward = 3
rightEnable = 2


GPIO.setup(leftForward, GPIO.OUT)
GPIO.setup(leftBackward, GPIO.OUT)
GPIO.setup(leftEnable, GPIO.OUT)
GPIO.setup(rightForward, GPIO.OUT)
GPIO.setup(rightBackward, GPIO.OUT)
GPIO.setup(rightEnable, GPIO.OUT)

leftEnPWM = GPIO.PWM(leftEnable, 100);
leftEnPWM.start(0);

rightEnPWM = GPIO.PWM(rightEnable, 100);
rightEnPWM.start(0);


leftEnPWM.ChangeDutyCycle(50)
rightEnPWM.ChangeDutyCycle(50)
sleep(2)

print ("Right goes backward")
GPIO.output(rightForward, GPIO.LOW)
GPIO.output(rightBackward, GPIO.HIGH)
sleep(2)

print ("Right goes forward")
GPIO.output(rightForward, GPIO.HIGH)
GPIO.output(rightBackward, GPIO.LOW)
sleep(2)


print ("Left goes backward")
GPIO.output(leftForward, GPIO.LOW)
GPIO.output(leftBackward, GPIO.HIGH)
sleep(2)

print ("Left goes forward")
GPIO.output(leftForward, GPIO.HIGH)
GPIO.output(leftBackward, GPIO.LOW)
sleep(2)

leftEnPWM.ChangeDutyCycle(0)
rightEnPWM.ChangeDutyCycle(0)

