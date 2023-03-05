import serial, re
import paho.mqtt.client as mqtt
from ServoModule import ServoController

serial_controller = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
ser = serial.Serial(serial_controller, serial_speed=9600, timeout=0.1)
serverAddress = "test.mosquitto.org"
clientName = "PiBot"
client = mqtt.Client()
didPrintSubscribeMessage = False



def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        client.subscribe("pibot/servoxy")
        client.subscribe("pibot/servo")
        print("subscribed")


def messageDecoder(client, userdata, msg):
    global controller
    message = msg.payload.decode(encoding='UTF-8')
    if re.match(r'X\d+Y\d+', message):
        ser.write(message.encode('utf-8'))
    else:
        sc = ServoController(controller)
        if message.isnumeric():
            sc.servo(int(message))
        else:
            sc.servo(message)


# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder

# Connect to the MQTT server & loop forever..
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()

