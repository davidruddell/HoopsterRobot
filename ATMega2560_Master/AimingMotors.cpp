#include "AimingMotors.h"

// Create a new instance of the AccelStepper class:
AccelStepper aimingMotor(AccelStepper::DRIVER, stepPin, dirPin);

// Use Serial1 for communication
DFRobot_WT61PC sensor(&Serial1);

void setupAimingMotor() {
  // Set the maximum speed and acceleration:
  aimingMotor.setMaxSpeed(500.0);
  aimingMotor.setAcceleration(100.0);

  // Enable the motor
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, HIGH);
}

void setupInclinometer() {
  // Use Serial1 for communication
  Serial1.begin(9600);
  // Revise the data output frequency of sensor
  sensor.modifyFrequency(FREQUENCY_10HZ);
}

void runAimingMotor(int steps, bool isClockwise) {
  // Set the target position:
  int targetPosition = isClockwise ? steps : -steps;
  aimingMotor.moveTo(targetPosition);

  // Run the motor to step and change its speed and direction based on the calling of moveTo():
  while (aimingMotor.distanceToGo() != 0) {
    aimingMotor.run();
  }
}

void checkAngles() {
  if (sensor.available()) {
    Serial.print("Acc\t");
    Serial.print(sensor.Acc.X);
    Serial.print("\t");
    Serial.print(sensor.Acc.Y);
    Serial.print("\t");
    Serial.println(sensor.Acc.Z);  //acceleration information of X,Y,Z
    Serial.print("Gyro\t");
    Serial.print(sensor.Gyro.X);
    Serial.print("\t");
    Serial.print(sensor.Gyro.Y);
    Serial.print("\t");
    Serial.println(sensor.Gyro.Z);  //angular velocity information of X,Y,Z
    Serial.print("Angle\t");
    Serial.print(sensor.Angle.X);
    Serial.print("\t");
    Serial.print(sensor.Angle.Y);
    Serial.print("\t");
    Serial.println(sensor.Angle.Z);  //angle information of X, Y, Z
    Serial.println(" ");
  }
}

void feedbackLoop() {
  
}