from MotorModule import Motor
import time
import paho.mqtt.client as mqtt


class ObstacleAvoidance():
    def __init__(self):
        self.motor = Motor(22, 27, 17, 2, 4, 3)
        self.client = mqtt.Client()
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.on_message = self.on_message
        self.client.subscribe("pibot/distance", qos=2)
        time.sleep(2)
        self.count = 0
        self.flag = 0

    def on_message(self, client, userdata, message):
        # Convert message payload to string
        message_str = str(message.payload.decode("utf-8"))
        avgDistance = float(message_str)
        print (message_str)

        if avgDistance <= 25:
            print("Average distance is:", avgDistance, "cm")
            self.count += 1
            self.motor.stop()
            time.sleep(1)
            print("Move backward")
            self.motor.backward(0.3, 0.5)
            time.sleep(1.5)
            if self.count % 3 == 1 and (self.flag == 0):
                print("Move right")
                self.motor.move(0, -0.8, 1)
                self.flag = 1
            else:
                print("Move left")
                self.motor.move(0, 0.8, 1)
                self.flag = 0
                time.sleep(1.5)
                self.motor.stop()
                time.sleep(1)
        else:
            print("Move forward")
            self.motor.move(0.3, 0.0, 0.1)
            self.flag = 0

    def start(self):
        while True:
            self.client.loop()


obstacle_avoid = ObstacleAvoidance()
obstacle_avoid.start()