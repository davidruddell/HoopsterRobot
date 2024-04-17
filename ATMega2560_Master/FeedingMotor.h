#ifndef FEEDING_MOTOR_h
#define FEEDING_MOTOR_h

#include <AccelStepper.h>

// Define the stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver.
#define dirPin 41
#define stepPin 3
#define enablePin 40

void setupFeedingMotor();

void runFeedingMotor(int steps, bool isClockwise);
#endif