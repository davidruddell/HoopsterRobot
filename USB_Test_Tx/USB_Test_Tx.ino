// Include necessary libraries
#include <Arduino.h>
#include <PrintEx.h>

// Enumerations for commands
enum Command {
  // Receiving
  NO_COMMAND,
  DRIVE,
  CHANGE_AZIMUTH,
  CHANGE_AIM,
  CHANGE_MOTOR1_RPM,
  CHANGE_MOTOR2_RPM,
  LAUNCH,
  // Sending
  AZIMUTH_SUCCESS,
  AIM_SUCCESS,
  MOTOR1_SUCCESS,
  MOTOR2_SUCCESS,
};

// Enumerations for states
enum State {
  IDLE,
  DRIVING,
  CHANGING_AZIMUTH,
  CHANGING_AIM,
  CHANGING_MOTOR1_RPM,
  CHANGING_MOTOR2_RPM,
  CHECKING_AZIMUTH,
  CHECKING_AIM,
  CHECKING_MOTOR1_RPM,
  CHECKING_MOTOR2_RPM,
  LAUNCHING,
  ERROR
};

// Create a StreamEx object for printf-style printing
StreamEx mySerial = Serial;

// Define start and end characters
#define START_CHAR '<'
#define END_CHAR '>'

void setup() {
  Serial.begin(500000);
}

void transmitCommand(Command command, uint32_t intArg = 0, float floatArg = 0.0) {
  Serial.write(START_CHAR);
  Serial.write((char*)&command, sizeof(uint8_t));
  if (command == DRIVE || command == CHANGE_MOTOR1_RPM || command == CHANGE_MOTOR2_RPM) {
    Serial.write((char*)&intArg, sizeof(uint32_t));
  } else if (command == CHANGE_AZIMUTH || command == CHANGE_AIM) {
    Serial.write((char*)&floatArg, sizeof(float));
  }
  Serial.write(END_CHAR);
}

void transmitCommandDrive(Command command, int32_t intArg1 = 0, int32_t intArg2 = 0, int8_t int8Arg1 = 0, int8_t int8Arg2 = 0) {
  Serial.write(START_CHAR);
  Serial.write((char*)&command, sizeof(int8_t));
  Serial.write((char*)&intArg1, sizeof(int32_t));
  Serial.write((char*)&intArg2, sizeof(int32_t));
  Serial.write((char*)&int8Arg1, sizeof(int8_t));
  Serial.write((char*)&int8Arg2, sizeof(int8_t));
  Serial.write(END_CHAR);
}

void testCommands() {

  delay(1000);

  // Test DRIVE command
  transmitCommandDrive(DRIVE, -32768, 32768, 254, 255);  // Replace 100 with your desired joystick input

  delay(1000);

  // Test CHANGE_AZIMUTH command
  transmitCommand(CHANGE_AZIMUTH, 0, 0.12345);  // Replace 45.0 with your desired angle

  delay(1000);

  // Test CHANGE_AIM command
  transmitCommand(CHANGE_AIM, 0, 360.123);  // Replace 30.0 with your desired angle

  delay(1000);

  // Test CHANGE_MOTOR1_RPM command
  transmitCommand(CHANGE_MOTOR1_RPM, 6942);  // Replace 5000 with your desired RPM

  delay(1000);

  // Test CHANGE_MOTOR2_RPM command
  transmitCommand(CHANGE_MOTOR2_RPM, 10000);  // Replace 6000 with your desired RPM

  delay(1000);

  // Test LAUNCH command
  transmitCommand(LAUNCH);

  delay(1000);
}

void loop() {
  testCommands();  // Call testCommands in setup to send the commands
}
