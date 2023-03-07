import serial, re
import paho.mqtt.client as mqtt
from ServoModule import ServoController
import time, signal

serial_controller = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
ser = serial.Serial(serial_controller, 9600, timeout=0.1)
serverAddress = "test.mosquitto.org"
clientName = "PiBot"
client = mqtt.Client()
didPrintSubscribeMessage = False



def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        client.subscribe("pibot/servo")
        print("subscribed")


def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    print (message)
    if re.match(r'X\d+Y\d+', message):
        ser.write(message.encode('utf-8'))
    else:
        message = f"Z{message}\n"
        ser.write(message.encode('utf-8'))
        time.sleep(0.3)
        print(ser.readline())


# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder

def handle_exit(sig, frame):
    print("Closing serial port...")
    ser.close()
    print("Serial port closed")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# Connect to the MQTT server & loop forever..
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()