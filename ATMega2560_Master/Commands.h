#ifndef COMMAND_H
#define COMMAND_H

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

#endif