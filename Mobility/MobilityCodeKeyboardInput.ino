#include <AccelStepper.h>

// Right 1
const int motor1Pulse = 9;
const int motor1Direction = 43;
const int motor1Enable = 42; // Enable pin for motor 1
//Right 2
const int motor2Pulse = 8;
const int motor2Direction = 45;
const int motor2Enable = 44; // Enable pin for motor 2
// Left 1
const int motor3Pulse = 7;
const int motor3Direction = 35;
const int motor3Enable = 34; // Enable pin for motor 3
// Left 2
const int motor4Pulse = 6;
const int motor4Direction = 37;
const int motor4Enable = 36; // Enable pin for motor 4

AccelStepper stepperMotor1(AccelStepper::DRIVER, motor1Pulse, motor1Direction);
AccelStepper stepperMotor2(AccelStepper::DRIVER, motor2Pulse, motor2Direction);
AccelStepper stepperMotor3(AccelStepper::DRIVER, motor3Pulse, motor3Direction);
AccelStepper stepperMotor4(AccelStepper::DRIVER, motor4Pulse, motor4Direction);
char lastCommand = '\0';

void setup() {
  pinMode(motor1Enable, OUTPUT);
  pinMode(motor2Enable, OUTPUT);
  pinMode(motor3Enable, OUTPUT);
  pinMode(motor4Enable, OUTPUT);

  digitalWrite(motor1Enable, HIGH);
  digitalWrite(motor2Enable, HIGH);
  digitalWrite(motor3Enable, HIGH);
  digitalWrite(motor4Enable, HIGH);

  stepperMotor1.setMaxSpeed(1000);
  stepperMotor2.setMaxSpeed(1000);
  stepperMotor3.setMaxSpeed(1000);
  stepperMotor4.setMaxSpeed(1000);
  
  Serial.begin(9600);
}

void loop() {
  digitalWrite(motor1Enable, LOW);
  digitalWrite(motor2Enable, LOW);
  digitalWrite(motor3Enable, LOW);
  digitalWrite(motor4Enable, LOW);

  SerialEvent();

  // Check the last command and run in that direction
  // Forward Direction
  if (lastCommand == '1') {
    stepperMotor1.setSpeed(1000);
    stepperMotor2.setSpeed(1000);
    stepperMotor3.setSpeed(1000);
    stepperMotor4.setSpeed(1000);
  } 
  // Backward Direction
  else if (lastCommand == '2') {
    stepperMotor1.setSpeed(-1000);
    stepperMotor2.setSpeed(-1000);
    stepperMotor3.setSpeed(-1000);
    stepperMotor4.setSpeed(-1000);
  }
  // Right 
  else if (lastCommand == '3') {
    stepperMotor1.setSpeed(-1000);
    stepperMotor2.setSpeed(1000);
    stepperMotor3.setSpeed(1000);
    stepperMotor4.setSpeed(-1000);
  }
  // Left
  else if (lastCommand == '4') {
    stepperMotor1.setSpeed(1000);
    stepperMotor2.setSpeed(-1000);
    stepperMotor3.setSpeed(-1000);
    stepperMotor4.setSpeed(1000);  
  } 
  // Rotate Left
  else if (lastCommand == '5') {
    stepperMotor1.setSpeed(1000);
    stepperMotor2.setSpeed(1000);
    stepperMotor3.setSpeed(-1000);
    stepperMotor4.setSpeed(-1000);  
  } 
  // Rotate Right
  else if (lastCommand == '6') {
    stepperMotor1.setSpeed(-1000);
    stepperMotor2.setSpeed(-1000);
    stepperMotor3.setSpeed(1000);
    stepperMotor4.setSpeed(1000);
  }
  // Forward Right
  else if (lastCommand == '7') {
    stepperMotor1.setSpeed(0);
    stepperMotor2.setSpeed(1000);
    stepperMotor3.setSpeed(1000);
    stepperMotor4.setSpeed(0);  
  } 
  // Forward Left
  else if (lastCommand == '8') {
    stepperMotor1.setSpeed(1000);
    stepperMotor2.setSpeed(0);
    stepperMotor3.setSpeed(0);
    stepperMotor4.setSpeed(1000);
  }
  // Backward Right
  else if (lastCommand == '9') {
    stepperMotor1.setSpeed(-1000);
    stepperMotor2.setSpeed(0);
    stepperMotor3.setSpeed(0);
    stepperMotor4.setSpeed(-1000);
  }
  // Backward Left
  else if (lastCommand == '0') {
    stepperMotor1.setSpeed(0);
    stepperMotor2.setSpeed(-1000);
    stepperMotor3.setSpeed(-1000);
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
    char inputVariable = Serial.read();

    if(inputVariable == '1' || inputVariable == '2' || inputVariable == '3' || inputVariable == '4' || inputVariable == '5' || inputVariable == '6' || inputVariable == '7' || inputVariable == '8' || inputVariable == '9' || inputVariable == '0' || inputVariable == 'x') {
      // Update the last command
      lastCommand = inputVariable;
    }
  }
}

