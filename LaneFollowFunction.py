import cv2
from MotorModule import Motor
from LaneCurveDetect import getLaneCurve
from CameraModule import VideoCapture


class LaneFollow:
    def __init__(self):
        self.video = VideoCapture()
        self.motor = Motor(22, 27, 17, 2, 4, 3)
        self.sensitivity = 1.3
        self.max_speed = 0.2

    def run(self):
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


lane_follow = LaneFollow()
lane_follow.run()
