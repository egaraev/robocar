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
        client.subscribe("pibot/face")
        print("subscribed")


def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    if message =="face_on":
        print ("Starting Face tracking")
        subprocess.call(['sh', '/home/eldar/robocar/start_face_tracking.sh'])
    else:
        print ("Stopping Face tracking")
        subprocess.call(['sh', '/home/eldar/robocar/stop_face_tracking.sh'])



# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder


# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()


