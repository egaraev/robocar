import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

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

def distance():
    print ("Starting distance sensor.....")
    while True:
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
            avgDistance = round(distance+1.15, 2)

        client.publish("pibot/distance", avgDistance)
        time.sleep(0.5)



distance()