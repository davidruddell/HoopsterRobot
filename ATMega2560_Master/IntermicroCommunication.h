#ifndef INTERMICRO_COMMUNICATION_H
#define INTERMICRO_COMMUNICATION_H

#include <Arduino.h>
#include "Commands.h"
#include "States.h"

// Buffer size
#define BUFFER_SIZE 16

// Control buttons index
#define CONTROL_BUTTONS1_INDEX 9
#define CONTROL_BUTTONS2_INDEX 10

// Start and end characters
#define START_CHAR '<'
#define END_CHAR '>'

// Function prototypes
void setupIntermicro();
long int concatenateBytes(char* buffer, int start);
void processBuffer();
void checkBuffer(uint32_t* desiredInputInt, float* desiredInputFloat, long int* joystickInput1, long int* joystickInput2, uint8_t* controlButtons1, uint8_t* controlButtons2, State* currentState);

#endif