import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

left_sensor = 10
central_sensor = 9
right_sensor = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(central_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)

def infrared():
    while True:
        # Read sensor values
        left_value = GPIO.input(left_sensor)
        central_value = GPIO.input(central_sensor)
        right_value = GPIO.input(right_sensor)

        # Pack values into a message
        message = f"{left_value},{central_value},{right_value}"

        # Publish message via MQTT
        client.publish("pibot/infrared", message, qos=0)

        # Wait for some time before reading the sensors again
        time.sleep(0.1)


infrared()



