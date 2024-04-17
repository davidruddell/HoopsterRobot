// DrivingMotors.cpp
// Code for Mobility System

#include "DrivingMotors.h"

// Define Stepper Motors
//Right 1
AccelStepper stepperMotor1(AccelStepper::DRIVER, motor1Pulse, motor1Direction);
//Right 2
AccelStepper stepperMotor2(AccelStepper::DRIVER, motor2Pulse, motor2Direction);
//Left 1
AccelStepper stepperMotor3(AccelStepper::DRIVER, motor3Pulse, motor3Direction);
//Left 2
AccelStepper stepperMotor4(AccelStepper::DRIVER, motor4Pulse, motor4Direction);

volatile char lastCommand = 'x';

// Define your functions here
void setupMotors() {
  pinMode(motor1Enable, OUTPUT);
  pinMode(motor2Enable, OUTPUT);
  pinMode(motor3Enable, OUTPUT);
  pinMode(motor4Enable, OUTPUT);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  pinMode(LED6, OUTPUT);
  pinMode(LED7, OUTPUT);
  pinMode(LED8, OUTPUT);
  pinMode(LED9, OUTPUT);
  pinMode(LED0, OUTPUT);

  digitalWrite(motor1Enable, HIGH);
  digitalWrite(motor2Enable, HIGH);
  digitalWrite(motor3Enable, HIGH);
  digitalWrite(motor4Enable, HIGH);

  //MaxSpeed
  stepperMotor1.setMaxSpeed(MaxSpeed);
  stepperMotor2.setMaxSpeed(MaxSpeed);
  stepperMotor3.setMaxSpeed(MaxSpeed);
  stepperMotor4.setMaxSpeed(MaxSpeed);

  //Acceleration
  stepperMotor1.setAcceleration(Acceleration);
  stepperMotor2.setAcceleration(Acceleration);
  stepperMotor3.setAcceleration(Acceleration);
  stepperMotor4.setAcceleration(Acceleration);

  Serial.begin(9600);
}

void loopMotors() {
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  digitalWrite(LED4, LOW);
  digitalWrite(LED5, LOW);
  digitalWrite(LED6, LOW);
  digitalWrite(LED7, LOW);
  digitalWrite(LED8, LOW);
  digitalWrite(LED9, LOW);
  digitalWrite(LED0, LOW);

  SerialEvent();

  // Check the last command and run in that direction
  // Forward Direction
  if (lastCommand == '1') {
    digitalWrite(LED1, HIGH);
    stepperMotor1.setSpeed(Speed);
    stepperMotor2.setSpeed(Speed);
    stepperMotor3.setSpeed(Speed);
    stepperMotor4.setSpeed(Speed);
  }
  // Backward Direction
  else if (lastCommand == '2') {
    digitalWrite(LED2, HIGH);
    stepperMotor1.setSpeed(-Speed);
    stepperMotor2.setSpeed(-Speed);
    stepperMotor3.setSpeed(-Speed);
    stepperMotor4.setSpeed(-Speed);
  }
  // Right
  else if (lastCommand == '3') {
    digitalWrite(LED3, HIGH);
    stepperMotor1.setSpeed(-Speed);
    stepperMotor2.setSpeed(Speed);
    stepperMotor3.setSpeed(Speed);
    stepperMotor4.setSpeed(-Speed);
  }
  // Left
  else if (lastCommand == '4') {
    digitalWrite(LED4, HIGH);
    stepperMotor1.setSpeed(Speed);
    stepperMotor2.setSpeed(-Speed);
    stepperMotor3.setSpeed(-Speed);
    stepperMotor4.setSpeed(Speed);
  }
  // Rotate Left
  else if (lastCommand == '5') {
    digitalWrite(LED5, HIGH);
    stepperMotor1.setSpeed(Speed);
    stepperMotor2.setSpeed(Speed);
    stepperMotor3.setSpeed(-Speed);
    stepperMotor4.setSpeed(-Speed);
  }
  // Rotate Right
  else if (lastCommand == '6') {
    digitalWrite(LED6, HIGH);
    stepperMotor1.setSpeed(-Speed);
    stepperMotor2.setSpeed(-Speed);
    stepperMotor3.setSpeed(Speed);
    stepperMotor4.setSpeed(Speed);
  }
  // Forward Right
  else if (lastCommand == '7') {
    digitalWrite(LED7, HIGH);
    stepperMotor1.setSpeed(0);
    stepperMotor2.setSpeed(Speed);
    stepperMotor3.setSpeed(Speed);
    stepperMotor4.setSpeed(0);
  }
  // Forward Left
  else if (lastCommand == '8') {
    digitalWrite(LED8, HIGH);
    stepperMotor1.setSpeed(Speed);
    stepperMotor2.setSpeed(0);
    stepperMotor3.setSpeed(0);
    stepperMotor4.setSpeed(Speed);
  }
  // Backward Right
  else if (lastCommand == '9') {
    digitalWrite(LED9, HIGH);
    stepperMotor1.setSpeed(-Speed);
    stepperMotor2.setSpeed(0);
    stepperMotor3.setSpeed(0);
    stepperMotor4.setSpeed(-Speed);
  }
  // Backward Left
  else if (lastCommand == '0') {
    digitalWrite(LED0, HIGH);
    stepperMotor1.setSpeed(0);
    stepperMotor2.setSpeed(-Speed);
    stepperMotor3.setSpeed(-Speed);
    stepperMotor4.setSpeed(0);
  }
  // Stop Motion
  else if (lastCommand == 'x') {
    stepperMotor1.setSpeed(0);
    stepperMotor2.setSpeed(0);
    stepperMotor3.setSpeed(0);
    stepperMotor4.setSpeed(0);
  }

  // Run the motors at a constant speed
  stepperMotor1.runSpeed();
  stepperMotor2.runSpeed();
  stepperMotor3.runSpeed();
  stepperMotor4.runSpeed();
}

void SerialEvent() {
  while (Serial.available() > 0) {
    // Read from Serial Input value
    char inputVariable = Serial.read();

    if (inputVariable == '1' || inputVariable == '2' || inputVariable == '3' || inputVariable == '4' || inputVariable == '5' || inputVariable == '6' || inputVariable == '7' || inputVariable == '8' || inputVariable == '9' || inputVariable == '0' || inputVariable == 'x') {
      // Update the last command
      lastCommand = inputVariable;
    }
  }
}
