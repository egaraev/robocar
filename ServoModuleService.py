import serial, re
import paho.mqtt.client as mqtt
import time, signal, sys

serial_controller = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
ser = serial.Serial(serial_controller, 9600, timeout=0.1)
serverAddress = "test.mosquitto.org"
clientName = "PiBot"
client = mqtt.Client()
didPrintSubscribeMessage = False

def reset_arduino_connection(ser):
    print("Resetting Arduino connection...")
    ser.close()  # Close the current serial connection
    time.sleep(5)  # Wait for 1 second to ensure the connection is closed
    ser.open()  # Reopen the serial connection
    print("Arduino connection reset")

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
    elif message == "RESET":
        reset_arduino_connection(ser)
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