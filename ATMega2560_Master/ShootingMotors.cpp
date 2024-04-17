#include "ShootingMotors.h"

void setupShootingMotors() {
  // Set the motor pins as output
  pinMode(MOTORA, OUTPUT);
  pinMode(MOTORB, OUTPUT);

  // Set the motor control pins as output
  pinMode(MOTOR_A1, OUTPUT);
  pinMode(MOTOR_A2, OUTPUT);
  pinMode(MOTOR_B1, OUTPUT);
  pinMode(MOTOR_B2, OUTPUT);

  // Set motor A direction
  digitalWrite(MOTOR_A1, HIGH);
  digitalWrite(MOTOR_A2, LOW);

  // Set motor B direction
  digitalWrite(MOTOR_B1, LOW);
  digitalWrite(MOTOR_B2, HIGH);

  // Set the PWM frequency for 16-bit Timer1
  TCCR1A = (1 << COM1A1) | (1 << COM1B1) | (1 << WGM11);  // non-inverting mode for OC1A and OC1B, Mode 14: Fast PWM, TOP=ICR1
  TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS10);     // prescaler set to 1, Mode 14: Fast PWM, TOP=ICR1
  ICR1 = 1023;                                            // TOP value for 10bit resolution
}

void runShootingMotorA(int targetPWM) {
  // Check if the target PWM value is within the range
  if (targetPWM < MIN_PWM) {
    targetPWM = MIN_PWM;
  } else if (targetPWM > MAX_PWM) {
    targetPWM = MAX_PWM;
  }

  // Gradually increase the PWM value to the motor
  for (int PWM1 = MIN_PWM; PWM1 <= targetPWM; PWM1++) {
    OCR1A = PWM1;  // Use OCR1A for pin 9 (MOTORA)
    delay(10);     // Add a delay to control the speed of the PWM increase
  }
}

void runShootingMotorB(int targetPWM) {
  // Check if the target PWM value is within the range
  if (targetPWM < MIN_PWM) {
    targetPWM = MIN_PWM;
  } else if (targetPWM > MAX_PWM) {
    targetPWM = MAX_PWM;
  }

  // Gradually increase the PWM value to the motor
  for (int PWM2 = MIN_PWM; PWM2 <= targetPWM; PWM2++) {
    OCR1B = PWM2;  // Use OCR1B for pin 10 (MOTORB)
    delay(10);     // Add a delay to control the speed of the PWM increase
  }
}

int checkRPM1() {

  return 0;
}

int checkRPM2() {

  return 0;
}

void feedbackLoop1() {

}

void feedbackLoop2() {

}