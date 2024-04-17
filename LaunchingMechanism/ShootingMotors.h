#ifndef ShootingMotors_h
#define ShootingMotors_h

#include "Arduino.h"

// Define the LED pins
#define LED1 7
#define LED2 8

// Define the motor control pins
#define MOTOR_A1 2
#define MOTOR_A2 3
#define MOTOR_B1 4
#define MOTOR_B2 5

// Define the potentiometer pins
#define POT_PIN1 A0
#define POT_PIN2 A1

void setupShootingMotors();
void loopShootingMotors();

#endif
