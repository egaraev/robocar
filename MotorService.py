import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#

serverAddress = "test.mosquitto.org"
import paho.mqtt.client as mqtt
clientName = "PiBot"
client = mqtt.Client()
didPrintSubscribeMessage = False




class Motor():
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmB.start(0);

    def move(self, speed=0.5, turn=0.0, t=0):
        speed *= 100
        turn *= 70
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100

        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        if leftSpeed > 0:
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW)
        else:
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)

        if rightSpeed > 0:
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)
        else:
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)

        sleep(t)


    def backward(self, speed=0.3, t=0):
        speed *= 100
        self.pwmA.ChangeDutyCycle(speed);
        self.pwmB.ChangeDutyCycle(speed);
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.HIGH)
        GPIO.output(self.In1B, GPIO.LOW)
        GPIO.output(self.In2B, GPIO.HIGH)
        sleep(t)


    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        sleep(t)


GPIO.cleanup()

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
    elif message == "None" or message == "joystick_on" or message == "joystick_off":
        pass
    else:
        print("moving")
        print (message)
        motor.move(message)


# Set up calling functions to mqttClient
client.on_connect = connectionStatus
client.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()



if __name__ == '__main__':
    motor = Motor(22, 27, 17, 2, 4, 3)
    # main()