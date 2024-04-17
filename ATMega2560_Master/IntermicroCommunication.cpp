#include "IntermicroCommunication.h"

// Variables for command processing
volatile uint32_t desiredInputIntTemp = 0;
volatile float desiredInputFloatTemp = 0.0;
volatile long int joystickInput1Temp = 0;
volatile long int joystickInput2Temp = 0;
volatile uint8_t controlButtons1Temp = 0;
volatile uint8_t controlButtons2Temp = 0;
volatile State currentStateTemp = IDLE;

static char buffer[BUFFER_SIZE];  // Buffer to hold incoming commands
static uint8_t bufPos = 0;        // Position in the buffer

void setupIntermicro() {
  Serial.begin(9600);
}

long int concatenateBytes(char* buffer, int start) {
  long int result = 0;
  for (int i = 0; i < 4; i++) {
    unsigned char byte = buffer[start + i];
    result |= (long int)byte << (8 * i);
  }
  return result;
}

void processBuffer() {
  Command receivedCommand = buffer[0];
  //Serial.println(receivedCommand);

  switch (receivedCommand) {
    case NO_COMMAND:
      currentStateTemp = IDLE;
      break;

    case DRIVE:
      // code to handle DRIVE command
      joystickInput1Temp = concatenateBytes(buffer, 1);
      joystickInput2Temp = concatenateBytes(buffer, 5);
      controlButtons1Temp = buffer[CONTROL_BUTTONS1_INDEX];
      controlButtons2Temp = buffer[CONTROL_BUTTONS2_INDEX];

      currentStateTemp = DRIVING;
      break;

    case CHANGE_AZIMUTH:
      // code to handle CHANGE_AZIMUTH command
      desiredInputFloatTemp = *((float*)(buffer + sizeof(uint8_t)));

      currentStateTemp = CHANGING_AZIMUTH;
      break;
    case CHANGE_AIM:
      // code to handle CHANGE_AIM command
      desiredInputFloatTemp = *((float*)(buffer + sizeof(uint8_t)));

      currentStateTemp = CHANGING_AIM;
      break;
    case CHANGE_MOTOR1_RPM:
      // code to handle CHANGE_MOTOR1_RPM command
      desiredInputIntTemp = *((int*)(buffer + sizeof(uint8_t)));

      currentStateTemp = CHANGING_MOTOR1_RPM;
      break;
    case CHANGE_MOTOR2_RPM:
      // code to handle CHANGE_MOTOR2_RPM command
      desiredInputIntTemp = *((int*)(buffer + sizeof(uint8_t)));

      currentStateTemp = CHANGING_MOTOR2_RPM;
      break;
    case LAUNCH:
      // code to handle LAUNCH command
      currentStateTemp = LAUNCHING;
      break;
    default:
      // code to handle unknown command
      currentStateTemp = ERROR;
      break;
  }
}

void checkBuffer(uint32_t* desiredInputInt, float* desiredInputFloat, long int* joystickInput1, long int* joystickInput2, uint8_t* controlButtons1, uint8_t* controlButtons2, State* currentState) {
  // Check if data is available to read
  int availableBytes = Serial.available();
  while (availableBytes-- > 0) {
    char inChar = Serial.read();  // Read a character

    if (inChar == START_CHAR) {
      // If the start character is received, reset the buffer
      bufPos = 0;
    } else if (inChar == END_CHAR && bufPos != 0) {
      // If the end character is received, parse the command
      processBuffer();
      bufPos = 0;

      // Update the values of the pointers
      *desiredInputInt = desiredInputIntTemp;
      *desiredInputFloat = desiredInputFloatTemp;
      *joystickInput1 = joystickInput1Temp;
      *joystickInput2 = joystickInput2Temp;
      *controlButtons1 = controlButtons1Temp;
      *controlButtons2 = controlButtons2Temp;
      *currentState = currentStateTemp;
    } else if (bufPos < BUFFER_SIZE) {
      // If buffer is not full, add character to buffer
      buffer[bufPos++] = inChar;
    }
  }
}