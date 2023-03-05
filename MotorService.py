from MotorModule import Motor
import paho.mqtt.client as mqtt

serverAddress = "test.mosquitto.org"
clientName = "PiBot"
client = mqtt.Client()
didPrintSubscribeMessage = False


motor = Motor(22, 27, 17, 2, 4, 3)
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
        motor.move(0.25, 0.0, 2)
        motor.stop(5)
    elif message == "stop":
        print("!!! stopping!")
        motor.stop()
    elif message == "backward":
        print("\/ backward \/")
        motor.backward(0.25, 2)
        motor.stop(5)
    elif message == "left":
        print("<- left")
        motor.move(0, 0.25, 2)
        motor.stop(5)
    elif message == "right":
        print("-> right")
        motor.move(0, -0.25, 2)
        motor.stop()
    elif message == "None":
        pass
    else:
        print("moving")
        print (message)
        motor.move(message)


# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder

# Connect to the MQTT server & loop forever..
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()



if __name__ == '__main__':
    motor = Motor(22, 27, 17, 2, 4, 3)
    # main()
