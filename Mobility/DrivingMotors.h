// DrivingMotors.h

#ifndef DRIVING_MOTORS_H
#define DRIVING_MOTORS_H

#include <AccelStepper.h>

#define MaxSpeed 1000
#define Speed 500
#define Acceleration 100

// Define global variables
#define LED1 22
#define LED2 23
#define LED3 24
#define LED4 25
#define LED5 26
#define LED6 27
#define LED7 28
#define LED8 29
#define LED9 30
#define LED0 31

// Right 1
#define motor1Pulse 9
#define motor1Direction 43
#define motor1Enable 42  // Enable pin for motor 1

//Right 2
#define motor2Pulse 8
#define motor2Direction 45
#define motor2Enable 44  // Enable pin for motor 2

// Left 1
#define motor3Pulse 7
#define motor3Direction 35
#define motor3Enable 34  // Enable pin for motor 3

// Left 2
#define motor4Pulse 6
#define motor4Direction 37
#define motor4Enable 36  // Enable pin for motor 4

// Declare your functions here
void setupMotors();
void loopMotors();
void SerialEvent();

#endif
