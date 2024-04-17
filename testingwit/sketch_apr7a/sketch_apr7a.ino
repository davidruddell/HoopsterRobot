#include <AccelStepper.h>
#include "DFRobot_WT61PC.h"

#define ANGLE_DIR_PIN 39
#define ANGLE_STEP_PIN 11
#define ANGLE_ENABLE_PIN 38

AccelStepper angleMotor(AccelStepper::DRIVER, ANGLE_STEP_PIN, ANGLE_DIR_PIN);
DFRobot_WT61PC sensor(&Serial1);

const float TARGET_ANGLE = 27.0f;     // Use a constant for the target angle
const float ANGLE_TOLERANCE = 0.25f;  // Tolerance for the target angle

unsigned long previousMillis = 0;
const unsigned long sensorInterval = 25;  // Read sensor data every 50 milliseconds

void setupAngleMotor() {
  angleMotor.setMaxSpeed(525);       // Increase maximum speed
  angleMotor.setAcceleration(30000);  // Increase acceleration
  pinMode(ANGLE_ENABLE_PIN, OUTPUT);
  digitalWrite(ANGLE_ENABLE_PIN, LOW);
}

void runAngleMotor(long steps, bool isClockwise) {
  long targetPosition = isClockwise ? steps : -steps;
  angleMotor.moveTo(targetPosition);
  while (angleMotor.distanceToGo() != 0) {
    angleMotor.run();
  }
}

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600);
  sensor.modifyFrequency(FREQUENCY_200HZ);  // Use a higher frequency for the sensor
  setupAngleMotor();
}

void loop() {
  unsigned long currentMillis = millis();
  float currentAngle;
  bool isClockwise;
  while (!(currentAngle >= TARGET_ANGLE - ANGLE_TOLERANCE && currentAngle <= TARGET_ANGLE + ANGLE_TOLERANCE)) {
    if (sensor.available()) {
      currentAngle = sensor.Angle.Y;
      Serial.println(currentAngle);
      isClockwise = currentAngle < TARGET_ANGLE;
    }

    float estimate = (currentAngle - TARGET_ANGLE) * (22000.0/13.0);
    if (currentAngle < TARGET_ANGLE - ANGLE_TOLERANCE || currentAngle > TARGET_ANGLE + ANGLE_TOLERANCE) {
      runAngleMotor(estimate, isClockwise);
    }
  }
}