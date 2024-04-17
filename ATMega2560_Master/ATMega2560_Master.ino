// Include necessary libraries
#include "Commands.h"
#include "States.h"
#include "DrivingMotors.h"
#include "IntermicroCommunication.h"
#include "ShootingMotors.h"
#include "AimingMotors.h"
#include "FeedingMotor.h"
#include <Arduino.h>

// Variables for command processing
volatile uint32_t desiredInputInt = 0; // Variable to store desired integer input
volatile float desiredInputFloat = 0.0; // Variable to store desired float input
volatile long int joystickInput1 = 0; // Variable to store joystick 1 input
volatile long int joystickInput2 = 0; // Variable to store joystick 2 input
volatile uint8_t controlButtons1 = 0; // Variable to store control button 1 input
volatile uint8_t controlButtons2 = 0; // Variable to store control button 2 input
volatile State currentState = IDLE; // Variable to store the current state, initialized as IDLE

void setup() {
  setupDrivingMotors();
  setupShootingMotors();
  setupDrivingMotors();
  setupIntermicro();
  setupShootingMotors();
  setupAimingMotor();
  setupInclinometer();
  setupTachometer();
  setupFeedingMotor();
}

void loop() {

  checkBuffer(&desiredInputInt, &desiredInputFloat, &joystickInput1, &joystickInput2, &controlButtons1, &controlButtons2, &currentState);

  switch (currentState) {
    case IDLE:
      //do nothing
      break;

    case DRIVING:
      //Serial.println("Received DRIVE command");
      //Serial.print("Joystick 1: ");
      //Serial.println(joystickInput1);
      //Serial.print("Joystick 2: ");
      //Serial.println(joystickInput2);
      //Serial.print("Buttons 1: ");
      //Serial.println(controlButtons1);
      //Serial.print("Buttons 2: ");
      //Serial.println(controlButtons2);

      currentState = IDLE;
      break;
    case CHANGING_AZIMUTH:
      //Serial.println("Received CHANGE_AZIMUTH command");
      //Serial.print("Desired Angle: ");
      //Serial.println(desiredInputFloat, 2);

      currentState = CHECKING_AZIMUTH;
      break;
    case CHANGING_AIM:
      //Serial.println("Received CHANGE_AIM command");
      //Serial.print("Desired Angle: ");
      //Serial.println(desiredInputFloat, 2);

      currentState = CHECKING_AIM;
      break;
    case CHANGING_MOTOR1_RPM:
      //Serial.println("Received CHANGE_MOTOR1_RPM command");
      //Serial.print("Desired Angle: ");
      //Serial.println(desiredInputInt);

      currentState = CHECKING_MOTOR1_RPM;
      break;
    case CHANGING_MOTOR2_RPM:
      //Serial.println("Received CHANGE_MOTOR2_RPM command");
      //Serial.print("Desired Angle: ");
      //Serial.println(desiredInputInt);

      currentState = CHECKING_MOTOR2_RPM;
      break;
    case CHECKING_AZIMUTH:
      //Serial.println("Checking AZIMUTH");

      currentState = IDLE;
      break;
    case CHECKING_AIM:
      //Serial.println("Checking AIM");

      currentState = IDLE;
      break;
    case CHECKING_MOTOR1_RPM:
      //Serial.println("Checking MOTOR1_RPM");

      currentState = IDLE;
      break;
    case CHECKING_MOTOR2_RPM:
      //Serial.println("Checking MOTOR2_RPM");

      currentState = IDLE;
      break;
    case LAUNCHING:
      //Serial.println("Launching");

      currentState = IDLE;
      break;
    default:
      //Serial.println("Received unknown command");

      currentState = IDLE;
      break;
  }
}
