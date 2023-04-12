import cv2
import os
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
import time
from MotorModule import Motor

# Initialize the Motor
motor = Motor(22, 27, 17, 2, 4, 3)

class CarController:
    def __init__(self, motor):
        self.motor = motor
        self.speed = 0.25
        self.curveVal = 0.0
        self.sens = 1.7
        self.current_speed_limit = None
        self.green_light = False
        self.red_light = False
        self.stop_sign = False
        self.person_detected = False

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
            while self.red_light:
                pass
        elif self.person_detected:
            print("Person detected")
            self.motor.stop()
            while self.person_detected:
                pass
        else:
            print("No sign or obstacle detected, moving forward")
            if self.current_speed_limit is not None:
                self.speed = self.current_speed_limit / 100

            self.motor.move(self.speed, self.curveVal * self.sens, 0.05)

    def update_flags(self):
        ret, frame = cap.read()
        if not ret:
            return

        cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
        run_inference(interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(interpreter, threshold)[:top_k]

        self.reset_flags()
        for obj in objs:
            label = labels.get(obj.id, obj.id)

            if label == "green light":
                self.green_light = True
            elif label == "red light":
                self.red_light = True
            elif label == "person":
                self.person_detected = True

def main():
    model_path = 'efficientdet-lite_edgetpu.tflite'
    label_path = 'labels.txt'
    top_k = 10
    threshold = 0.2

    print('Loading {} with {} labels.'.format(model_path, label_path))
    interpreter = make_interpreter(model_path)
    interpreter.allocate_tensors()
    labels = read_label_file(label_path)
    global inference_size
    inference_size = input_size(interpreter)

    global cap
    cap = cv2.VideoCapture(0)  # Use the default camera

    # Create an instance of CarController and pass the Motor instance
    car_controller = CarController(motor)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2_im = frame
        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
        run_inference(interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(interpreter, threshold)[:top_k]
        cv2_im = append_objs_to_img(cv2_im, inference_size, objs, labels, threshold)

        # Call the `process_objects` method with the detected objects and labels
        car_controller.process_objects(objs, labels)

        cv2.imshow('Live Inference', cv2_im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Add this line to introduce a small delay
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


def append_objs_to_img(cv2_im, inference_size, objs, labels, threshold):
    height, width, channels = cv2_im.shape
    scale_x, scale_y = width / inference_size[0], height / inference_size[1]
    for obj in objs:
        if obj.score < threshold:  # Skip objects with a low score
            continue

        bbox = obj.bbox.scale(scale_x, scale_y)
        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        percent = int(100 * obj.score)
        label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

        cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2_im = cv2.putText(cv2_im, label, (x0, y0-10),
                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return cv2_im

if __name__ == '__main__':
    main()