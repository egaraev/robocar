import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#
Ena = 2
In1 = 3
In2 = 4
GPIO.setup(Ena, GPIO.OUT)
GPIO.setup(In1, GPIO.OUT)
GPIO.setup(In2, GPIO.OUT)
pwmA = GPIO.PWM(Ena, 100);
pwmA.start(0);

######################

pwmA.ChangeDutyCycle(60);
GPIO.output(In1,GPIO.LOW)
GPIO.output(In1,GPIO.HIGH)
sleep(2)
pwmA.ChangeDutyCycle(0);