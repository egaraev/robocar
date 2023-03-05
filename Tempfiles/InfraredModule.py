from RPi import GPIO
from time import sleep
from MotorModule import Motor
motor = Motor(22, 27, 17, 2, 4, 3)
speed = 0.25
curveVal = 0.3
sens = 1.7

class LineTracking:
    def __init__(self):
        self.left_sensor = 10
        self.central_sensor = 9
        self.right_sensor = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_sensor, GPIO.IN)
        GPIO.setup(self.central_sensor, GPIO.IN)
        GPIO.setup(self.right_sensor, GPIO.IN)

    def run(self):
        while True:
            if  GPIO.input(self.right_sensor) and GPIO.input(self.central_sensor):
                print("Robot is straying off to the right, move left captain!")#
                motor.move(speed, curveVal*sens, 0.05)
            elif  GPIO.input(self.left_sensor) and GPIO.input(self.central_sensor):
                print("Robot is straying off to the left, move right captain!")
                motor.move(speed, -curveVal*sens, 0.05)
            elif GPIO.input(self.right_sensor) and GPIO.input(self.left_sensor):
                print("Following the line!")
                motor.move(speed, 0.0, 0.05)

    def disable(self):
        motor.stop()

tracking = LineTracking()
tracking.run()