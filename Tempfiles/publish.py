import paho.mqtt.client as mqtt

#message = "line_on"
message = "ultrasonic_off"


client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

client.publish("pibot/ultrasonic", str(message), qos=1)