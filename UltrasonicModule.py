import RPi.GPIO as GPIO
import time
from MotorModule import Motor


class ObstacleAvoidance:
    def __init__(self):
        self.motor = Motor(22, 27, 17, 2, 4, 3)
        self.TRIG = 14
        self.ECHO = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, False)
        print("Calibrating.....")
        time.sleep(2)
        self.count = 0
        self.flag = 0

    def run(self):
        try:
            while True:
                i = 0
                avgDistance = 0
                for i in range(5):
                    GPIO.output(self.TRIG, False)
                    time.sleep(0.1)
                    GPIO.output(self.TRIG, True)
                    time.sleep(0.00001)
                    GPIO.output(self.TRIG, False)

                while GPIO.input(self.ECHO) == 0:
                    pulse_start = time.time()

                while GPIO.input(self.ECHO) == 1:
                    pulse_end = time.time()
                    pulse_duration = pulse_end - pulse_start
                    distance = pulse_duration * 17150
                    avgDistance = round(distance + 1.15, 2)

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
        except KeyboardInterrupt:
            GPIO.cleanup()


if __name__ == "__main__":
    obstacle_avoidance = ObstacleAvoidance()
    obstacle_avoidance.run()
