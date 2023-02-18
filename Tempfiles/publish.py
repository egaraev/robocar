import paho.mqtt.client as mqtt

#message = "line_on"
message = "line_off"


client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

client.publish("pibot/line", str(message), qos=1)