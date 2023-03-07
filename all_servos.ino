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
unsigned long previousMillis = 0;  // variable to store the previous time
const long interval = 25;          // interval at which to update the servo

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
    String incomingString = Serial.readStringUntil('\n');
    z_angle = incomingString.toInt(); // read Z servo angle
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
      zState = z.read();
      int delta = z_angle - zState;
      int increment = delta > 0 ? 1 : -1;
      while (zState != z_angle) {
        unsigned long currentMillis = millis();
        if (currentMillis - previousMillis >= interval) {
          previousMillis = currentMillis;
          zState += increment;
          z.write(zState);
        }
      }
    }
    else {
      Serial.println("Invalid angle");
    }
  }
}