import cv2
import serial,time
import paho.mqtt.client as mqtt
from MotorModule import Motor
from CameraModule import VideoCapture
motor = Motor(22, 27, 17, 2, 4, 3)
from imutils.video import FPS
import face_recognition
import imutils
import pickle

class FaceTracer:
    def __init__(self, port, baud_rate, face_cascade_file, mqtt_server, mqtt_port, recognize_interval=1):
        self.ser = serial.Serial(port, baud_rate, timeout=0.1)
        self.face_cascade = cv2.CascadeClassifier(face_cascade_file)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.connect(mqtt_server, mqtt_port, 60)
        self.distance = 0
        self.video_capture = VideoCapture(size=[640,480])
        self.frame_counter = 0
        self.recognize_interval = 20
        self.fps = FPS().start()
        self.currentname = "unknown"

    def _on_connect(self, client, userdata, flags, rc):
        self.mqtt_client.subscribe("pibot/distance", qos=2)

    def _on_message(self, client, userdata, msg):
        self.distance = float(msg.payload.decode(encoding='UTF-8'))

    def recognize_faces(self, frame):
        #currentname = "unknown"
        encodingsP = "encodings.pickle"
        data = pickle.loads(open(encodingsP, "rb").read())
        boxes = face_recognition.face_locations(frame)
        self.fps.update()
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                if self.currentname != name:
                    self.currentname = name  # store the name in a class attribute
                    print(self.currentname)
            if name != "Unknown": # only append the name if it's not "Unknown"
                names.append(name)


    def trace_faces(self):
        self.frame_counter += 1
        # check if it's time to recognize faces
        if self.frame_counter % self.recognize_interval == 0:
            frame = self.video_capture.get_frame()
            frame = cv2.flip(frame, 1)  # mirror the image
            self.recognize_faces(frame)
        else:
            # just get the frame
            frame = self.video_capture.get_frame()
            frame = cv2.flip(frame, 1)  # mirror the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 8)  # detect the face
        for x,y,w,h in faces:
            #sending coordinates to Arduino
            string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
            #print(string)
            self.mqtt_client.publish("pibot/servo", string)
            ##This is to send coordinates directly to arduino
            #self.ser.write(string.encode('utf-8'))
            ##This is to send coordinates directly to arduino
            #plot the center of the face
            cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
            #plot the roi
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.putText(frame, self.currentname, (x, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)
        #plot the squared region in the center of the screen
        cv2.rectangle(frame,(640//2-30,480//2-30),
                     (640//2+30,480//2+30),
                      (255,255,255),3)
        cv2.imshow('img',frame)



        # Get the distance value from MQTT
        self.mqtt_client.loop(timeout=0.01)
        # Check if distance is not zero and print it
        if self.distance != 0:
            print(self.distance)
            if self.distance>100.0:
                print ("Moving forward")
                motor.move(0.3, 0.0, 0.1)
            elif self.distance<50.0:
                print ("Moving backward")
                motor.backward(0.3, 0.1)
            else:
                motor.stop()

        self.fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()*self.recognize_interval))


class MainLoop:
    def __init__(self, face_tracer):
        self.face_tracer = face_tracer

    def run(self):
        while True:
            self.face_tracer.trace_faces()

            # press q to Quit
            if cv2.waitKey(10)&0xFF== ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    face_tracer = FaceTracer(
        '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0',
        9600,
        'haarcascade_frontalface_default.xml',
        'test.mosquitto.org',
        1883
    )
#    face_detector = FaceDetector(recognize_interval=5)

    main_loop = MainLoop(face_tracer)
    main_loop.run()