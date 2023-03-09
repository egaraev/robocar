# control-pibot.py
# Written by Prof. John Gallaugher. For build videos see:
# https://YouTube.com/profgallaugher
# You can control this subscriber program with an iOS app named
# Mil Mascaras, which you can download for free from the iOS App Store at:
# https://apps.apple.com/us/app/mil-mascaras/id1550345112?platform=iphone
#
# serverAddress, below is your pi's host name. But, since our Mosquitto broker and
# this program (which acts as the subscriber) are on the same Raspberry Pi
# we can simply use "localhost" as the server name.
serverAddress = "test.mosquitto.org"

# *** IMPORTANT ***
# The commands below also substitute localhost with your Pi's hostname.
# This works when you've opened a Terminal & connected to your Pi.
# If you're in a class with other students, you can substitue "localhost"
# with the name of their py (e.g. hostname.local if they're on a standard
# Wi-Fi network, or just "hostname" if they're on a network like the Boston
# College campus network, where "hostname" is the name of your friend's Pi.
#
# Once this code is running, you can test with the shell commands:
# To play any of the numbered sounds (substitute a diffrent number for "1" for a different sound:
# mosquitto_pub -h localhost -t "pibot/move" -m "1"
# To start the robot:
# mosquitto_pub -h localhost -t "pibot/move" -m "forward"
# To stop the robot:
# mosquitto_pub -h localhost -t "pibot/move" -m "stop"


import time
import paho.mqtt.client as mqtt



# don't modify the name below - this is correct
clientName = "PiBot"

client = mqtt.Client()
# Flag to indicate subscribe confirmation hasn't been printed yet.
didPrintSubscribeMessage = False




def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        client.subscribe("pibot/move")
        print("subscribed")

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')

    if message == "forward":
        print("^^^ moving forward! ^^^")

    elif message == "stop":
        print("!!! stopping!")
    elif message == "backward":
        print("\/ backward \/")
    elif message == "left":
        print("<- left")
    elif message == "right":
        print("-> right")


# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()