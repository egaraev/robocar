import cv2

from MotorModule import Motor
from LaneDetectionModule import getLaneCurve
import CameraModule
import cv2

#################################
motor = Motor(27, 22, 17, 2, 4, 3)
#################################

def main():
    img = CameraModule.getImg()
    curveVal = getLaneCurve(img,2)

    sen = 1.3 # Sensitivity
    maxVAl = 0.2  #Max speed
    if curveVal>maxVAl: curveVal=maxVAl
    if curveVal<-maxVAl: curveVal=-maxVAl
    print (curveVal)
    if curveVal>0:
        sen = 1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.05: curveVal=0

    motor.move(0.25, -curveVal*sen,0.05)

    cv2.waitKey(1)



if __name__ == '__main__':
    while True:
        main()