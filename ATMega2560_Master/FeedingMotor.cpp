#include "FeedingMotor.h"

// Create a new instance of the AccelStepper class:
AccelStepper feedingMotor(AccelStepper::DRIVER, stepPin, dirPin);

void setupFeedingMotor() {
  // Set the maximum speed and acceleration:
  feedingMotor.setMaxSpeed(500.0);
  feedingMotor.setAcceleration(100.0);

  // Enable the motor
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, HIGH);
}

void runFeedingMotor(int steps, bool isClockwise) {
  // Set the target position:
  int targetPosition = isClockwise ? steps : -steps;

  feedingMotor.moveTo(targetPosition);

  feedingMotor.runToPosition();

  delay(1000); // Wait for a second

  // Move the motor back to the original position:
  feedingMotor.moveTo(0);

  feedingMotor.runToPosition();

  delay(1000); // Wait for a second
}