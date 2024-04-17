#ifndef SHOOTING_MOTORS_H
#define SHOOTING_MOTORS_H

#include <Arduino.h>

// Define the motor pins
#define MOTORA 9
#define MOTORB 10

// Define the motor control pins
#define MOTOR_A1 46
#define MOTOR_A2 47
#define MOTOR_B1 48
#define MOTOR_B2 49

// Define the min and max PWM values
#define MIN_PWM 0
#define MAX_PWM 1023

void setupShootingMotors();

void runShootingMotorA(int targetPWM);

void runShootingMotorB(int targetPWM);

int checkRPM1();

int checkRPM2();

void feedbackLoop1();

void feedbackLoop2();

#endif  // SHOOTING_MOTORS_H