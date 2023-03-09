import serial
import time

controller = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

class ServoController():
    def __init__(self, serial_port, serial_speed=9600):
        self.ser = serial.Serial(serial_port, serial_speed, timeout=1)
        # Wait for Arduino to initialize
        time.sleep(2)

    def servo(self, angle):
        cmd = "{:03d}\n".format(angle)
        self.ser.write(cmd.encode('utf-8'))
        time.sleep(0.1)
        print(self.ser.readline())

    def __del__(self):
        self.ser.close()


my_controller = ServoController(controller)
#my_controller.servo(70)
#my_controller.servo(70)
#my_controller.servo(180)
# my_controller.servo('middle')