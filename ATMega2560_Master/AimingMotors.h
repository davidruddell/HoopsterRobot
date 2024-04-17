#ifndef AIMING_MOTOR_h
#define AIMING_MOTOR_h

#include <AccelStepper.h>
#include "DFRobot_WT61PC.h"

// Define the stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver.
#define dirPin 39
#define stepPin 2
#define enablePin 38

void setupAimingMotor();

void setupInclinometer();

void runAimingMotor(int steps, bool isClockwise);

int checkAngle();

void feedbackLoop();

#endif