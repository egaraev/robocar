#include <Servo.h>

Servo x, y, z;
int width = 640, height = 480;  // total resolution of the video
int xpos = 90, ypos = 90, zpos = 90;  // initial positions of all servos
int zState;

void setup() {

  Serial.begin(9600);
  x.attach(14);
  y.attach(15);
  z.attach(16);
  x.write(xpos);
  y.write(ypos);
  z.write(zpos);
}

const int angle = 1;   // degree of increment or decrement

void loop() {
if (Serial.available() > 0)
{
  int x_mid, y_mid, z_angle;
  if (Serial.read() == 'X')
  {
    x_mid = Serial.parseInt();  // read center x-coordinate
    if (Serial.read() == 'Y')
      y_mid = Serial.parseInt(); // read center y-coordinate
  }
  else
  {
    z_angle = Serial.parseInt(); // read Z servo angle
    // Check if angle is single digit
    if (Serial.available() > 0 && Serial.peek() != '\n')
    {
      // Read and append the next character
      char nextChar = Serial.read();
      z_angle = (z_angle * 10) + (nextChar - '0');
    }
  }
    /* adjust the servo within the squared region if the coordinates
        is outside it
    */
    if (x_mid > width / 2 + 30)
      xpos += angle;
    if (x_mid < width / 2 - 30)
      xpos -= angle;
    if (y_mid > height / 2 + 30)
      ypos -= angle;
    if (y_mid < height / 2 - 30)
      ypos += angle;

    // if the servo degree is outside its range
    if (xpos >= 180)
      xpos = 180;
    else if (xpos <= 0)
      xpos = 0;
    if (ypos >= 180)
      ypos = 180;
    else if (ypos <= 0)
      ypos = 0;

    x.write(xpos);
    y.write(ypos);

    if (z_angle >= 0 && z_angle <= 180) {
      Serial.print("Going to angle: ");
      Serial.println(z_angle);
      delay(3000);
      while (zState != z_angle) {
        if (zState < z_angle) {
          z.write(zState + 1);
          zState += 1;
          delay(25);
        }
        else {
          z.write(zState - 1);
          zState -= 1;
          delay(25);
        }
      }
    }
    else {
      Serial.println("Invalid angle");
    }
  }
}
