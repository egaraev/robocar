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
        client.subscribe("pibot/line")
        print("subscribed")


def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    if message =="line_on":
        print ("Starting Line follow")
        subprocess.call(['sh', '/home/eldar/robocar/start_line_follow.sh'])
    else:
        print ("Stopping Line follow")
        subprocess.call(['sh', '/home/eldar/robocar/stop_line_follow.sh'])



# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder


# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()


