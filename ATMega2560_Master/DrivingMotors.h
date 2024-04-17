// DrivingMotors.h
#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <AccelStepper.h>
#include <float.h>

#define SPEED FLT_MAX
#define ACCELERATION 750

// Right 1
#define motor1Pulse 7
#define motor1Direction 43
#define motor1Enable 42

//Right 2
#define motor2Pulse 6
#define motor2Direction 45
#define motor2Enable 44

// Left 1
#define motor3Pulse 5
#define motor3Direction 35
#define motor3Enable 34

// Left 2
#define motor4Pulse 4
#define motor4Direction 37
#define motor4Enable 36

void runRotatingMotors(int steps, bool isRight);
void setupDrivingMotors();
void runDrivingMotors();
void SerialEvent();
void setupTachometer();
void runTachometer();
void Pulse_Event();
void Pulse_Event2();

#endif