import cv2
import os
import time
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
from MotorModule import Motor
from LaneCurveDetect import getLaneCurve
from CameraModule import VideoCapture
import threading
from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate


# Lane Following
class LaneFollow:
    def __init__(self, motor, video_capture=None):
        self.video = video_capture or cv2.VideoCapture(0)
        self.motor = motor
        self.sensitivity = 1.3
        self.max_speed = 0.2

    def run(self, duration=None):
        start_time = time.time()
        while True:
            if duration and time.time() - start_time > duration:
                break
            ret, img = self.video.read()
            if not ret:
                print("Failed to read frame from the camera")
                continue
            curve_val = getLaneCurve(img, 1)
            #line_curve_val = getLineCurve(img)
            line_curve_val = 0
            line_curve_val = round(line_curve_val, 2)
            average_curve_val = (curve_val +line_curve_val)/2

            if curve_val > self.max_speed:
                curve_val = self.max_speed
            elif curve_val < -self.max_speed:
                curve_val = -self.max_speed

            print("Curve value", curve_val)
            print("Line curve value", line_curve_val)
            print("Average curve value", average_curve_val)

            if average_curve_val > 0:
                self.sensitivity = 1.7
                if average_curve_val < 0.05:
                    average_curve_val = 0
            else:
                if average_curve_val > -0.05:
                    average_curve_val = 0

            self.motor.move(0.3, -average_curve_val * self.sensitivity, 0.05)

            cv2.waitKey(1)

# Sign Recognition
class CarController:
    def __init__(self, motor=None, interpreter=None, threshold=0.6, top_k=1, labels_path='labels.txt', video_capture=None):
        self.motor = motor
        self.video = video_capture
        self.speed = 0.25
        self.curveVal = 0.0
        self.sens = 1.5
        self.current_speed_limit = None
        self.green_light = False
        self.red_light = False
        self.stop_sign = False
        self.person_detected = False
        self.interpreter = make_interpreter("efficientdet-lite_edgetpu.tflite")  # Add this line
        self.interpreter.allocate_tensors()  # Add this line
        self.threshold = threshold
        self.top_k = top_k
        self.labels = self.load_labels(labels_path)


    def load_labels(self, path):
        with open(path, 'r') as f:
            labels = {}
            for i, row in enumerate(f.readlines()):
                label_name = row.strip()
                labels[i] = label_name
            return labels



    def process_objects(self, objects, labels):
        print("Processing objects...")
        self.reset_flags()

        for obj in objects:
            label = labels.get(obj.id, obj.id)

            if label == "limit 30":
                self.current_speed_limit = 30
            elif label == "limit 50":
                self.current_speed_limit = 50
            elif label == "green light":
                self.green_light = True
            elif label == "red light":
                self.red_light = True
            elif label == "stop":
                self.stop_sign = True
            elif label == "person":
                self.person_detected = True

        self.control_car()

    def reset_flags(self):
        self.green_light = False
        self.red_light = False
        self.stop_sign = False
        self.person_detected = False

    def control_car(self):
        print("Controlling car...")
        if self.stop_sign:
            print("Stop sign detected")
            self.motor.stop()
            time.sleep(5)
        elif self.red_light:
            print("Red light detected")
            self.motor.stop()
        elif self.person_detected:
            print("Person detected")
            self.motor.stop()
        else:
            print("No sign or obstacle detected, moving forward")
            if self.current_speed_limit is not None:
                self.speed = self.current_speed_limit / 100

            # Print the curve and speed values
            print("Curve value:", self.curveVal)
            print("Speed value:", self.speed)

            self.motor.move(self.speed, self.curveVal * self.sens, 0.05)


    def update_flags(self, interpreter, threshold, top_k, labels):
        ret, frame = self.video.read()
        if not ret:
            return

        cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        inference_size = input_size(interpreter)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
        run_inference(interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(interpreter, threshold)[:top_k]

        self.reset_flags()
        for obj in objs:
            label = labels.get(obj.id, obj.id)
            print(f"Detected object: {label}")  # Add this line for debugging

            if label == "green light":
                self.green_light = True
            elif label == "red light":
                self.red_light = True
            elif label == "person":
                self.person_detected = True
            elif label == "stop":  # Add this line
                self.stop_sign = True  # Add this line
        if not self.red_light and not self.person_detected:
            self.control_car()

# Autonomous Car combining both Lane Following and Sign Recognition
class AutonomousCar:
    def __init__(self, motor=None, interpreter=None, video_capture=None):
        self.lane_follow = LaneFollow(motor, video_capture=video_capture)
        self.car_controller = CarController(self.lane_follow.motor, interpreter, video_capture=video_capture)
        self.detected_objects = []

    def run_lane_following(self):
        while True:
            ret, img = self.lane_follow.video.read()
            if not ret:
                print("Failed to read frame from the camera")
                continue
            curve_val = getLaneCurve(img, 1)
            line_curve_val = 0
            line_curve_val = round(line_curve_val, 2)
            average_curve_val = (curve_val + line_curve_val) #/ 2

            if curve_val > self.lane_follow.max_speed:
                curve_val = self.lane_follow.max_speed
            elif curve_val < -self.lane_follow.max_speed:
                curve_val = -self.lane_follow.max_speed

            self.car_controller.curveVal = average_curve_val
            cv2.waitKey(1)

    def run_sign_recognition(self):
        while True:
            ret, frame = self.car_controller.video.read()
            if not ret:
                continue

            cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            inference_size = input_size(self.car_controller.interpreter)
            cv2_im_rgb_resized = cv2.resize(cv2_im_rgb, inference_size)
            run_inference(self.car_controller.interpreter, cv2_im_rgb_resized.tobytes())
            objs = get_objects(self.car_controller.interpreter, self.car_controller.threshold)[:self.car_controller.top_k]

            self.detected_objects = objs  # Update the detected_objects attribute

            self.car_controller.process_objects(objs, self.car_controller.labels)
            cv2.waitKey(1)


    def display_frames(self):
        while True:
            ret, frame = self.car_controller.video.read()
            if not ret:
                print("Failed to read frame from the camera")
                continue

            self.draw_objects_on_frame(frame, input_size(self.car_controller.interpreter), self.detected_objects, self.car_controller.labels, self.car_controller.threshold)  # Updated call

            cv2.imshow("Autonomous Car", frame)
            cv2.waitKey(1)



    def draw_objects_on_frame(self, frame, inference_size, objects, labels, threshold):
        height, width, channels = frame.shape
        scale_x, scale_y = width / inference_size[0], height / inference_size[1]

        for obj in objects:
            if obj.score < threshold:
                continue

            bbox = obj.bbox.scale(scale_x, scale_y)
            x0, y0 = int(bbox.xmin), int(bbox.ymin)
            x1, y1 = int(bbox.xmax), int(bbox.ymax)

            percent = int(100 * obj.score)
            label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

            frame = cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            frame = cv2.putText(frame, label, (x0, y0-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


    def run(self):
        lane_following_thread = threading.Thread(target=self.run_lane_following)
        sign_recognition_thread = threading.Thread(target=self.run_sign_recognition)
        display_frames_thread = threading.Thread(target=self.display_frames)  # Add this line

        lane_following_thread.start()
        sign_recognition_thread.start()
        display_frames_thread.start()  # Add this line

        lane_following_thread.join()
        sign_recognition_thread.join()
        display_frames_thread.join()  # Add this line


# Main function
def main():
    interpreter = Interpreter(
        model_path="efficientdet-lite_edgetpu.tflite",
        experimental_delegates=[load_delegate("libedgetpu.so.1")],
    )
    video_capture = cv2.VideoCapture(0)
    motor = Motor(22, 27, 17, 2, 4, 3)
    autonomous_car = AutonomousCar(motor, interpreter, video_capture)
    autonomous_car.run()
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()