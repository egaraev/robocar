from MotorModule import Motor
import paho.mqtt.client as mqtt


class LineFollow:
    def __init__(self):
        self.motor = Motor(22, 27, 17, 2, 4, 3)
        self.speed = 0.25
        self.curveVal = 0.3
        self.sens = 1.7

        self.client = mqtt.Client()
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.on_message = self.on_message
        self.client.subscribe("pibot/infrared")

    def on_message(self, client, userdata, message):
        # Convert message payload to string
        message_str = str(message.payload.decode("utf-8"))

        # Unpack values from message string
        left_value, central_value, right_value = message_str.split(",")

        # Convert values to integers
        left_value = int(left_value)
        central_value = int(central_value)
        right_value = int(right_value)

        # Use sensor values to control the robot
        if right_value and central_value:
            print("Robot is straying off to the right, move left!")
            self.motor.move(self.speed, self.curveVal * self.sens, 0.05)
        elif left_value and central_value:
            print("Robot is straying off to the left, move right!")
            self.motor.move(self.speed, -self.curveVal * self.sens, 0.05)
        elif right_value and left_value:
            print("Following the line!")
            self.motor.move(self.speed, 0.0, 0.05)

    def start(self):
        while True:
            self.client.loop()


line_follow = LineFollow()
line_follow.start()
