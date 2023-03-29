import time
import pygame
import os
import sys
from MotorModule import Motor

os.environ["SDL_VIDEODRIVER"] = "dummy"



# Joystick buttons
BUTTON_CIRCLE = 13
BUTTON_SHARE = 8

axisUpDown = 1
axisUpDownInverted = False
axisLeftRight = 3
axisLeftRightInverted = False
interval = 0.1

global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
global moveCircle
global moveShare
global leftRight
leftRight = 0
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
moveCircle = False
moveShare = False
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def PygameHandler(events):
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    global moveCircle
    global moveShare
    global leftRight

    for event in events:
        if event.type == pygame.QUIT:
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = False
        elif event.type == pygame.JOYBUTTONDOWN:
            hadEvent = True
            if event.button == BUTTON_CIRCLE:
                moveCircle = True
            elif event.button == BUTTON_SHARE:
                moveShare = True
        elif event.type == pygame.JOYBUTTONUP:
            hadEvent = True
            if event.button == BUTTON_CIRCLE:
                moveCircle = False
            elif event.button == BUTTON_SHARE:
                moveShare = False
        elif event.type == pygame.JOYAXISMOTION:
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)

            if axisUpDownInverted:
                upDown = -upDown
            if axisLeftRightInverted:
                leftRight = -leftRight

            if upDown < -0.1:
                moveUp = True
                moveDown = False
            elif upDown > 0.1:
                moveUp = False
                moveDown = True
            else:
                moveUp = False
                moveDown = False

            if leftRight < -0.1:
                moveLeft = True
                moveRight = False
            elif leftRight > 0.1:
                moveLeft = False
                moveRight = True
            else:
                moveLeft = False
                moveRight = False

def getJS():
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    global moveCircle
    global moveShare
    global leftRight

    PygameHandler(pygame.event.get())
    hadEvent = False

    return {'axis1': moveLeft * -1 + moveRight * 1,
            'axis2': moveUp * 1 + moveDown * -1,
            'circle': moveCircle,
            'share': moveShare,
            'leftRight': leftRight}




if __name__ == "__main__":
    try:
        motor = Motor(22, 27, 17, 2, 4, 3)
        print("Press ESC to quit")
        while not moveQuit:
            joyVals = getJS()

            print(f"Circle: {joyVals['circle']}, Share: {joyVals['share']}, LeftRight: {joyVals['leftRight']}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()