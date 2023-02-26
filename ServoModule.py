import serial
import time

class ServoController:
    def __init__(self, serial_port, serial_speed=115200):
        self.ser = serial.Serial(serial_port, serial_speed, timeout=1)
        # Wait for Arduino to initialize
        time.sleep(2)

    def servo(self, angle):
        cmd = str(angle) + "\n"
        self.ser.write(cmd.encode('utf-8'))
        time.sleep(5)
        print(self.ser.readline())
        #time.sleep(5)

    def __del__(self):
        self.ser.close()



my_controller = ServoController('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0')
my_controller.servo(120)
my_controller.servo(70)
my_controller.servo(180)
my_controller.servo('middle')