from RPi import GPIO
from time import sleep
from MotorModule import Motor
motor = Motor(27, 22, 17, 2, 4, 3)
GPIO.setmode(GPIO.BCM)

left_sensor = 10
central_sensor = 9
right_sensor = 11

GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(central_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)
speed = 0.25
curveVal = 0.3
sens = 1.7

while True:
    if  GPIO.input(right_sensor) and GPIO.input(central_sensor):
        print("Robot is straying off to the right, move left captain!")
        motor.move(speed, curveVal*sens, 0.05)
    elif  GPIO.input(left_sensor) and GPIO.input(central_sensor):
        print("Robot is straying off to the left, move right captain!")
        motor.move(speed, -curveVal*sens, 0.05)
    elif GPIO.input(right_sensor) and GPIO.input(left_sensor):
        print("Following the line!")
        motor.move(speed, 0.0, 0.05)