# Load library functions we want
import time
import pygame
from MotorModule import Motor
motor = Motor(22, 27, 17, 2, 4, 3)

axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 3                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit

    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = False
        elif event.type == pygame.JOYAXISMOTION:
            # A joystick has been moved, read axis positions (-1 to +1)
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            # Invert any axes which are incorrect
            if axisUpDownInverted:
                upDown = -upDown
            if axisLeftRightInverted:
                leftRight = -leftRight
            # Determine Up / Down values
            if upDown < -0.1:
                moveUp = True
                moveDown = False


            elif upDown > 0.1:
                moveUp = False
                moveDown = True


            else:
                moveUp = False
                moveDown = False
            # Determine Left / Right values
            if leftRight < -0.1:
                moveLeft = True
                moveRight = False


            elif leftRight > 0.1:
                moveLeft = False
                moveRight = True


            else:
                moveLeft = False
                moveRight = False
try:
    print ('Press [ESC] or Press PS3 O button to quit')
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            if moveQuit:
                break
            elif moveLeft:
                print ("Moving left")
                motor.move(0, 0.7, 0.1)
            elif moveRight:
                print ("Moving right")
                motor.move(0, -0.7, 0.1)
            elif moveUp:
                print ("Moving forward")
                motor.move(0.3, 0.0, 0.1)
            elif moveDown:
                print ("Moving backward")
                motor.backward(0.3, 0.1)
            else:
                print ("Slowing down")
                motor.stop()
        # Wait for the interval period
        time.sleep(interval)

except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    motor.stop(5)