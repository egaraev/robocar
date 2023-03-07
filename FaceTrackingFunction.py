import cv2
import serial,time
import paho.mqtt.client as mqtt
from MotorModule import Motor
from CameraModule import VideoCapture
motor = Motor(22, 27, 17, 2, 4, 3)

class FaceTracer:
    def __init__(self, port, baud_rate, face_cascade_file, mqtt_server, mqtt_port):
        self.ser = serial.Serial(port, baud_rate, timeout=0.1)
        self.face_cascade = cv2.CascadeClassifier(face_cascade_file)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.connect(mqtt_server, mqtt_port, 60)
        self.distance = 0
        self.video_capture = VideoCapture(size=[640,480])

    def _on_connect(self, client, userdata, flags, rc):
        self.mqtt_client.subscribe("pibot/distance", qos=2)

    def _on_message(self, client, userdata, msg):
        self.distance = float(msg.payload.decode(encoding='UTF-8'))

    def trace_faces(self):
        frame = self.video_capture.get_frame()
        frame = cv2.flip(frame, 1)  # mirror the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 6)  # detect the face
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
        #plot the squared region in the center of the screen
        cv2.rectangle(frame,(640//2-30,480//2-30),
                     (640//2+30,480//2+30),
                      (255,255,255),3)
        cv2.imshow('img',frame)

        # Get the distance value from MQTT
        self.mqtt_client.loop(timeout=0.01)
        # Check if distance is not zero and print it
#        if self.distance != 0:
#            print(self.distance)
#            if self.distance>100.0:
#                print ("Moving forward")
#                motor.move(0.3, 0.0, 0.1)
#            elif self.distance<50.0:
#                print ("Moving backward")
#                motor.backward(0.3, 0.1)
#            else:
#                motor.stop()


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
    main_loop = MainLoop(face_tracer)
    main_loop.run()