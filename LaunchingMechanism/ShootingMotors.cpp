#include "ShootingMotors.h"

void setupShootingMotors() {
  // Set the LED pins as output
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  // Set the motor control pins as output
  pinMode(MOTOR_A1, OUTPUT);
  pinMode(MOTOR_A2, OUTPUT);
  pinMode(MOTOR_B1, OUTPUT);
  pinMode(MOTOR_B2, OUTPUT);
}

void loopShootingMotors() {
  // Read the potentiometer values
  int potValue1 = analogRead(POT_PIN1);
  int potValue2 = analogRead(POT_PIN2);

  // Map the potentiometer values to a range suitable for PWM (0 - 255)
  int pwmValue1 = map(potValue1, 0, 1023, 0, 255);
  int pwmValue2 = map(potValue2, 0, 1023, 0, 255);

  digitalWrite(MOTOR_A1, HIGH); // Set motor A direction
  digitalWrite(MOTOR_A2, LOW);
  digitalWrite(MOTOR_B1, LOW); // Set motor B direction
  digitalWrite(MOTOR_B2, HIGH);
  
  // Write the PWM values to the LEDs
  analogWrite(LED1, pwmValue1);
  analogWrite(LED2, pwmValue2);
}
