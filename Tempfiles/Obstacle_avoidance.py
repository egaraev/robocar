import paho.mqtt.client as mqtt
import subprocess

serverAddress = "test.mosquitto.org"
clientName = "PiBot"
client = mqtt.Client()
didPrintSubscribeMessage = False

def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        client.subscribe("pibot/ultrasonic")
        print("subscribed")


def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    if message =="ultrasonic_on":
        print ("Obstacle avoidance start")
        subprocess.call(['sh', '/home/eldar/robocar/start_obstacle_avoid.sh'])
    else:
        print ("Obstacle avoidance stop")
        subprocess.call(['sh', '/home/eldar/robocar/stop_obstacle_avoid.sh'])


# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()
