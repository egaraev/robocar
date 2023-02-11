import RPi.GPIO as GPIO
import time
from MotorModule import Motor
motor = Motor(22, 27, 17, 2, 4, 3)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 14
ECHO = 16
i=0

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print ("Calibrating.....")
time.sleep(2)


try:
    count =0
    while True:
        i =0
        avgDistance =0
        for i in range (5):
            GPIO.output(TRIG, False)
            time.sleep(0.1)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            avgDistance = avgDistance+distance
            avgDistance=avgDistance/5
            #print(avgDistance)
        flag =0
        if avgDistance<15:
            print ("distance:",avgDistance,"cm")
            count = count+1
            motor.stop()
            time.sleep(1)
            print ("Move backward")
            motor.backward(0.3, 0.5)
            time.sleep(1.5)
            if count%3==1&(flag==0):
                print ("Move right")
                motor.move(0, -0.7, 0.5)
                flag=1
            else:
                print ("Move left")
                motor.move(0, 0.7, 0.5)
                flag =0
                time.sleep(1.5)
                motor.stop()
                time.sleep(1)
        else:
            print ("distance:",avgDistance,"cm")
            print ("Move forward")
            motor.move(0.3, 0.0, 0.5)
            flag =0

except KeyboardInterrupt:
        GPIO.cleanup()
