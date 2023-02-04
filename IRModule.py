from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

left_sensor = 10
central_sensor = 9
right_sensor = 11

GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(central_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)

try:
	while True:
		if  GPIO.input(right_sensor):
			print("Robot is straying off to the right, move left captain!")
		elif  GPIO.input(left_sensor):
			print("Robot is straying off to the left, move right captain!")
		else:
			print("Following the line!")
		sleep(0.2)
except:
	GPIO.cleanup()