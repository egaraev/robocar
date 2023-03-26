import cv2
import paho.mqtt.client as mqtt
from MotorModule import Motor
from LaneCurveDetect import getLaneCurve
from CameraModule import VideoCapture
import time


class LaneFollow:
    def __init__(self, mqtt_server, mqtt_port):
        self.video = VideoCapture()
        self.motor = Motor(22, 27, 17, 2, 4, 3)
        self.sensitivity = 1.3
        self.max_speed = 0.2

        # Set up MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(mqtt_server, mqtt_port, 60)

    def run(self):
        #reseting arduino to default servo coordinates
        message = "RESET"
        self.mqtt_client.publish("pibot/servo", message)

        # Set the desired coordinates for the X and Y servos
        x_mid = 640 // 2
        y_min = 480
        message = f'X{x_mid}Y{y_min}'
        time.sleep(10)

        # Send the coordinates repeatedly to force the servos to reach the desired positions
        for _ in range(20):  # Adjust the number of iterations as needed
            message = 'X{0:d}Y{1:d}'.format(x_mid, y_min)
            self.mqtt_client.publish("pibot/servo", message)
            time.sleep(0.1)  # Adjust the sleep time as needed
        while True:
            img = self.video.get_frame()
            curve_val = getLaneCurve(img, 2)

            if curve_val > self.max_speed:
                curve_val = self.max_speed
            elif curve_val < -self.max_speed:
                curve_val = -self.max_speed

            print(curve_val)

            if curve_val > 0:
                self.sensitivity = 1.7
                if curve_val < 0.05:
                    curve_val = 0
            else:
                if curve_val > -0.05:
                    curve_val = 0

            self.motor.move(0.22, -curve_val * self.sensitivity, 0.05)

            cv2.waitKey(1)



# Initialize the LaneFollow class with the MQTT server and port information
lane_follow = LaneFollow('test.mosquitto.org', 1883)
lane_follow.run()