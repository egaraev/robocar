#include <Servo.h>

Servo myServo;
int servoState;

void setup() {
  // put your setup code here, to run once:
  myServo.attach(14);

  Serial.begin(115200);
  delay(2000);

}

void loop() {
  // put your main code here, to run repeatedly:
  String servoCommand = Serial.readStringUntil('\n');

  if (servoCommand == "up") {
    Serial.println("Going UP");
    delay(3000);
    while (servoState > 0) {
      myServo.attach(14);
      myServo.write(servoState - 1);
      servoState -= 1;
      delay(25);
    }

    //Serial.print("Current Servo Angle: ");
    //Serial.println(servoState);
  }

  if (servoCommand == "down") {
    Serial.println("Going DOWN");
    delay(3000);
    while (servoState < 90) {
      myServo.write(servoState + 1);
      servoState += 1;
      delay(25);
    } 
    
    
    //Serial.print("Current Servo Angle: ");
    //Serial.println(servoState); 
  }

  if (servoCommand == "middle") {
    Serial.println("Going MIDDLE");
    delay(3000);
    if (servoState < 45) {
      while (servoState < 45) {
        myServo.write(servoState + 1);
        servoState += 1;
        delay(25);

      }
    }
    else {
      while (servoState > 45) {
        myServo.write(servoState - 1);
        servoState -= 1;
        delay(25);
      }
    }

    //Serial.print("Current Servo Angle: ");
    //Serial.println(servoState);
  }

if (servoCommand.length() > 0) {
  boolean isNumber = true;
  for (int i = 0; i < servoCommand.length(); i++) {
    if (!isdigit(servoCommand.charAt(i))) {
      isNumber = false;
      break;
    }
  }
  if (isNumber) {
    int angle = servoCommand.toInt();
    if (angle >= 0 && angle <= 180) {
      Serial.print("Going to angle: ");
      Serial.println(angle);
      delay(3000);
      while (servoState != angle) {
        if (servoState < angle) {
          myServo.write(servoState + 1);
          servoState += 1;
          delay(25);
        }
        else {
          myServo.write(servoState - 1);
          servoState -= 1;
          delay(25);
        }
      }
    }
    else {
      Serial.println("Invalid angle");
   }
  }
 }
}
