#include "DrivingMotors.h"

AccelStepper stepperMotor1(AccelStepper::DRIVER, motor1Pulse, motor1Direction);
AccelStepper stepperMotor2(AccelStepper::DRIVER, motor2Pulse, motor2Direction);
AccelStepper stepperMotor3(AccelStepper::DRIVER, motor3Pulse, motor3Direction);
AccelStepper stepperMotor4(AccelStepper::DRIVER, motor4Pulse, motor4Direction);
volatile char lastCommand = '\0';

void setupDrivingMotors() {
  pinMode(motor1Enable, OUTPUT);
  pinMode(motor2Enable, OUTPUT);
  pinMode(motor3Enable, OUTPUT);
  pinMode(motor4Enable, OUTPUT);

  digitalWrite(motor1Enable, HIGH);
  digitalWrite(motor2Enable, HIGH);
  digitalWrite(motor3Enable, HIGH);
  digitalWrite(motor4Enable, HIGH);

  stepperMotor1.setMaxSpeed(SPEED);
  stepperMotor2.setMaxSpeed(SPEED);
  stepperMotor3.setMaxSpeed(SPEED);
  stepperMotor4.setMaxSpeed(SPEED);

  stepperMotor1.setAcceleration(ACCELERATION);
  stepperMotor2.setAcceleration(ACCELERATION);
  stepperMotor3.setAcceleration(ACCELERATION);
  stepperMotor4.setAcceleration(ACCELERATION);

  Serial2.begin(9600);
}

void runDrivingMotors() {

  SerialEvent();

  // Check the last command and run in that direction
  // Forward Direction
  if (lastCommand == '1') {
    stepperMotor1.moveTo(-SPEED);
    stepperMotor2.moveTo(-SPEED);
    stepperMotor3.moveTo(SPEED);
    stepperMotor4.moveTo(SPEED);
  }
  // Backward Direction
  else if (lastCommand == '2') {
    stepperMotor1.moveTo(SPEED);
    stepperMotor2.moveTo(SPEED);
    stepperMotor3.moveTo(-SPEED);
    stepperMotor4.moveTo(-SPEED);
  }
  // Right
  else if (lastCommand == '3') {
    stepperMotor1.moveTo(SPEED);
    stepperMotor2.moveTo(-SPEED);
    stepperMotor3.moveTo(SPEED);
    stepperMotor4.moveTo(-SPEED);
  }
  // Left
  else if (lastCommand == '4') {
    stepperMotor1.moveTo(-SPEED);
    stepperMotor2.moveTo(SPEED);
    stepperMotor3.moveTo(-SPEED);
    stepperMotor4.moveTo(SPEED);
  }
  // Rotate Left
  else if (lastCommand == '5') {
    stepperMotor1.moveTo(-SPEED);
    stepperMotor2.moveTo(-SPEED);
    stepperMotor3.moveTo(-SPEED);
    stepperMotor4.moveTo(-SPEED);
  }
  // Rotate Right
  else if (lastCommand == '6') {
    stepperMotor1.moveTo(SPEED);
    stepperMotor2.moveTo(SPEED);
    stepperMotor3.moveTo(SPEED);
    stepperMotor4.moveTo(SPEED);
  }
  // Forward Right
  else if (lastCommand == '7') {
    stepperMotor1.moveTo(0);
    stepperMotor2.moveTo(-SPEED);
    stepperMotor3.moveTo(SPEED);
    stepperMotor4.moveTo(0);
  }
  // Forward Left
  else if (lastCommand == '8') {
    stepperMotor1.moveTo(-SPEED);
    stepperMotor2.moveTo(0);
    stepperMotor3.moveTo(0);
    stepperMotor4.moveTo(SPEED);
  }
  // Backward Right
  else if (lastCommand == '9') {
    stepperMotor1.moveTo(SPEED);
    stepperMotor2.moveTo(0);
    stepperMotor3.moveTo(0);
    stepperMotor4.moveTo(-SPEED);
  }
  // Backward Left
  else if (lastCommand == '0') {
    stepperMotor1.moveTo(0);
    stepperMotor2.moveTo(SPEED);
    stepperMotor3.moveTo(-SPEED);
    stepperMotor4.moveTo(0);
  }
  // Stop Motion
  else if (lastCommand == 'x') {
    stepperMotor1.stop();
    stepperMotor2.stop();
    stepperMotor3.stop();
    stepperMotor4.stop();
    stepperMotor1.runToPosition();
    stepperMotor2.runToPosition();
    stepperMotor3.runToPosition();
    stepperMotor4.runToPosition();
    //stepperMotor1.setCurrentPosition(0);
    //stepperMotor2.setCurrentPosition(0);
    //stepperMotor3.setCurrentPosition(0);
    //stepperMotor4.setCurrentPosition(0);
  }
  stepperMotor1.run();
  stepperMotor2.run();
  stepperMotor3.run();
  stepperMotor4.run();
}

void runRotatingMotors(int steps, bool isRight) {

  int targetPosition = isRight ? steps : -steps;

  stepperMotor1.moveTo(targetPosition);
  stepperMotor2.moveTo(targetPosition);
  stepperMotor3.moveTo(targetPosition);
  stepperMotor4.moveTo(targetPosition);

  while (stepperMotor1.distanceToGo() != 0) {
    stepperMotor1.run();
    stepperMotor2.run();
    stepperMotor3.run();
    stepperMotor4.run();
  }
}

void SerialEvent() {
  while (Serial2.available() > 0) {
    char inputVariable = Serial2.read();

    if (inputVariable == '1' || inputVariable == '2' || inputVariable == '3' || inputVariable == '4' || inputVariable == '5' || inputVariable == '6' || inputVariable == '7' || inputVariable == '8' || inputVariable == '9' || inputVariable == '0' || inputVariable == 'x') {
      // Update the last command
      lastCommand = inputVariable;
    }
  }
}


// Set how many pulses there are on each revolution.
const byte PulsesPerRevolution = 2;
const byte PulsesPerRevolution2 = 2;

// For high response time, a good value would be 100000. For reading very low RPM, a good value would be 300000.
const unsigned long ZeroTimeout = 100000;
const unsigned long ZeroTimeout2 = 100000;

// Calibration for smoothing RPM:
const byte numReadings = 2;
const byte numReadings2 = 2;

//////////// Sensor 1:

volatile unsigned long LastTimeWeMeasured;                        // Stores the last time we measured a pulse so we can calculate the period.
volatile unsigned long PeriodBetweenPulses = ZeroTimeout + 1000;  // Stores the period between pulses in microseconds.
                                                                  // It has a big number so it doesn't start with 0 which would be interpreted as a high frequency.
volatile unsigned long PeriodAverage = ZeroTimeout + 1000;        // Stores the period between pulses in microseconds in total, if we are taking multiple pulses.
                                                                  // It has a big number so it doesn't start with 0 which would be interpreted as a high frequency.
unsigned long FrequencyRaw;                                       // Calculated frequency, based on the period. This has a lot of extra decimals without the decimal point.
unsigned long FrequencyReal;                                      // Frequency without decimals.
unsigned long RPM;                                                // Raw RPM without any processing.
unsigned int PulseCounter = 1;                                    // Counts the amount of pulse readings we took so we can average multiple pulses before calculating the period.
unsigned long PeriodSum;                                          // Stores the summation of all the periods to do the average.
unsigned long LastTimeCycleMeasure = LastTimeWeMeasured;          // Stores the last time we measure a pulse in that cycle.
unsigned long CurrentMicros = micros();                           // Stores the micros in that cycle.

unsigned int AmountOfReadings = 1;
unsigned int ZeroDebouncingExtra;

// Variables for smoothing tachometer 1:
unsigned long readings[numReadings];  // The input.
unsigned long readIndex;              // The index of the current reading.
unsigned long total;                  // The running total.
unsigned long average;                // The RPM value after applying the smoothing.

//////////// Sensor 2:

volatile unsigned long LastTimeWeMeasured2;                        // Stores the last time we measured a pulse so we can calculate the period.
volatile unsigned long PeriodBetweenPulses2 = ZeroTimeout + 1000;  // Stores the period between pulses in microseconds.
                                                                   // It has a big number so it doesn't start with 0 which would be interpreted as a high frequency.
volatile unsigned long PeriodAverage2 = ZeroTimeout + 1000;        // Stores the period between pulses in microseconds in total, if we are taking multiple pulses.
                                                                   // It has a big number so it doesn't start with 0 which would be interpreted as a high frequency.
unsigned long FrequencyRaw2;                                       // Calculated frequency, based on the period. This has a lot of extra decimals without the decimal point.
unsigned long FrequencyReal2;                                      // Frequency without decimals.
unsigned long RPM2;                                                // Raw RPM without any processing.
unsigned int PulseCounter2 = 1;                                    // Counts the amount of pulse readings we took so we can average multiple pulses before calculating the period.
unsigned long PeriodSum2;                                          // Stores the summation of all the periods to do the average.
unsigned long LastTimeCycleMeasure2 = LastTimeWeMeasured2;         // Stores the last time we measure a pulse in that cycle.
unsigned long CurrentMicros2 = micros();                           // Stores the micros in that cycle.

unsigned int AmountOfReadings2 = 1;
unsigned int ZeroDebouncingExtra2;

// Variables for smoothing tachometer 2:
unsigned long readings2[numReadings];  // The input.
unsigned long readIndex2;              // The index of the current reading.
unsigned long total2;                  // The running total.
unsigned long average2;                // The RPM value after applying the smoothing.

void setupTachometer() {

  Serial.begin(9600);                                               // Begin serial communication.
  attachInterrupt(digitalPinToInterrupt(2), Pulse_Event, RISING);   // Enable interruption pin 2 when going from LOW to HIGH.
  attachInterrupt(digitalPinToInterrupt(3), Pulse_Event2, RISING);  // Enable interruption pin 3 when going from LOW to HIGH.

  delay(1000);
}

void runTachometer() {

  ////// Sensor 1:
  LastTimeCycleMeasure = LastTimeWeMeasured;  // Store the LastTimeWeMeasured in a variable.
  CurrentMicros = micros();                   // Store the micros() in a variable.

  if (CurrentMicros < LastTimeCycleMeasure) {
    LastTimeCycleMeasure = CurrentMicros;
  }

  FrequencyRaw = 10000000000 / PeriodAverage;  // Calculate the frequency using the period between pulses.

  if (PeriodBetweenPulses > ZeroTimeout - ZeroDebouncingExtra || CurrentMicros - LastTimeCycleMeasure > ZeroTimeout - ZeroDebouncingExtra) {  // If the pulses are too far apart that we reached the timeout for zero:
    FrequencyRaw = 0;                                                                                                                         // Set frequency as 0.
    ZeroDebouncingExtra = 2000;                                                                                                               // Change the threshold a little so it doesn't bounce.
  } else {
    ZeroDebouncingExtra = 0;  // Reset the threshold to the normal value so it doesn't bounce.
  }

  FrequencyReal = FrequencyRaw / 10000;  // Get frequency without decimals.

  RPM = FrequencyRaw / PulsesPerRevolution * 60;  // Frequency divided by amount of pulses per revolution multiply by
                                                  // 60 seconds to get minutes.
  RPM = RPM / 10000;                              // Remove the decimals.

  total = total - readings[readIndex];  // Advance to the next position in the array.
  readings[readIndex] = RPM;            // Takes the value that we are going to smooth.
  total = total + readings[readIndex];  // Add the reading to the total.
  readIndex = readIndex + 1;            // Advance to the next position in the array.

  if (readIndex >= numReadings)  // If we're at the end of the array:
  {
    readIndex = 0;  // Reset array index.
  }

  average = total / numReadings;  // The average value it's the smoothed result.

  ////// Sensor 2:
  LastTimeCycleMeasure2 = LastTimeWeMeasured2;  // Store the LastTimeWeMeasured in a variable.
  CurrentMicros2 = micros();                    // Store the micros() in a variable.

  if (CurrentMicros2 < LastTimeCycleMeasure2) {
    LastTimeCycleMeasure2 = CurrentMicros2;
  }

  FrequencyRaw2 = 10000000000 / PeriodAverage2;  // Calculate the frequency using the period between pulses.

  if (PeriodBetweenPulses2 > ZeroTimeout2 - ZeroDebouncingExtra2 || CurrentMicros2 - LastTimeCycleMeasure2 > ZeroTimeout2 - ZeroDebouncingExtra2) {  // If the pulses are too far apart that we reached the timeout for zero:
    FrequencyRaw2 = 0;                                                                                                                               // Set frequency as 0.
    ZeroDebouncingExtra2 = 2000;                                                                                                                     // Change the threshold a little so it doesn't bounce.
  } else {
    ZeroDebouncingExtra2 = 0;  // Reset the threshold to the normal value so it doesn't bounce.
  }

  FrequencyReal2 = FrequencyRaw2 / 10000;  // Get frequency without decimals.

  RPM2 = FrequencyRaw2 / PulsesPerRevolution2 * 60;  // Frequency divided by amount of pulses per revolution multiply by
                                                     // 60 seconds to get minutes.
  RPM2 = RPM2 / 10000;                               // Remove the decimals.

  total2 = total2 - readings2[readIndex2];  // Advance to the next position in the array.
  readings2[readIndex2] = RPM2;             // Takes the value that we are going to smooth.
  total2 = total2 + readings2[readIndex2];  // Add the reading to the total.
  readIndex2 = readIndex2 + 1;              // Advance to the next position in the array.

  if (readIndex2 >= numReadings2)  // If we're at the end of the array:
  {
    readIndex2 = 0;  // Reset array index.
  }

  average2 = total2 / numReadings2;  // The average value it's the smoothed result.

  // Sensor 1:
  //Serial.print("Period: ");
  //Serial.print(PeriodBetweenPulses);
  //Serial.print("\t");  // TAB space
  //Serial.print("Readings: ");
  //Serial.print(AmountOfReadings);
  //Serial.print("\t");  // TAB space
  //Serial.print("Frequency: ");
  //Serial.print(FrequencyReal);
  //Serial.print("\t");  // TAB space
  //Serial.print("RPM: ");
  //Serial.print(RPM);
  //Serial.print("\t");  // TAB space
  Serial.print("Tachometer: ");
  Serial.print(average);

  // Sensor 2:
  //Serial.print("\t");  // TAB space
  //Serial.print("Period2: ");
  //Serial.print(PeriodBetweenPulses2);
  //Serial.print("\t");  // TAB space
  //Serial.print("Readings2: ");
  //Serial.print(AmountOfReadings2);
  //Serial.print("\t");  // TAB space
  //Serial.print("Frequency2: ");
  //Serial.print(FrequencyReal2);
  //Serial.print("\t");  // TAB space
  //Serial.print("RPM2: ");
  //Serial.print(RPM2);
  Serial.print("\t");  // TAB space
  Serial.print("Tachometer2: ");
  Serial.println(average2);
}

void Pulse_Event() {

  PeriodBetweenPulses = micros() - LastTimeWeMeasured;  // Current "micros" minus the old "micros" when the last pulse happens.
                                                        // This will result with the period (microseconds) between both pulses.
                                                        // The way is made, the overflow of the "micros" is not going to cause any issue.

  LastTimeWeMeasured = micros();  // Stores the current micros so the next time we have a pulse we would have something to compare with.

  if (PulseCounter >= AmountOfReadings)  // If counter for amount of readings reach the set limit:
  {
    PeriodAverage = PeriodSum / AmountOfReadings;  // Calculate the final period dividing the sum of all readings by the
                                                   // amount of readings to get the average.
    PulseCounter = 1;                              // Reset the counter to start over. The reset value is 1 because its the minimum setting allowed (1 reading).
    PeriodSum = PeriodBetweenPulses;               // Reset PeriodSum to start a new averaging operation.


    int RemapedAmountOfReadings = map(PeriodBetweenPulses, 40000, 5000, 1, 10);  // Remap the period range to the reading range.

    RemapedAmountOfReadings = constrain(RemapedAmountOfReadings, 1, 10);  // Constrain the value so it doesn't go below or above the limits.
    AmountOfReadings = RemapedAmountOfReadings;                           // Set amount of readings as the remaped value.
  } else {
    PulseCounter++;                               // Increase the counter for amount of readings by 1.
    PeriodSum = PeriodSum + PeriodBetweenPulses;  // Add the periods so later we can average.
  }
}

void Pulse_Event2() {

  PeriodBetweenPulses2 = micros() - LastTimeWeMeasured2;  // Current "micros" minus the old "micros" when the last pulse happens.
                                                          // This will result with the period (microseconds) between both pulses.
                                                          // The way is made, the overflow of the "micros" is not going to cause any issue.

  LastTimeWeMeasured2 = micros();  // Stores the current micros so the next time we have a pulse we would have something to compare with.

  if (PulseCounter2 >= AmountOfReadings2)  // If counter for amount of readings reach the set limit:
  {
    PeriodAverage2 = PeriodSum2 / AmountOfReadings2;  // Calculate the final period dividing the sum of all readings by the
                                                      // amount of readings to get the average.
    PulseCounter2 = 1;                                // Reset the counter to start over. The reset value is 1 because its the minimum setting allowed (1 reading).
    PeriodSum2 = PeriodBetweenPulses2;                // Reset PeriodSum to start a new averaging operation.

    int RemapedAmountOfReadings2 = map(PeriodBetweenPulses2, 40000, 5000, 1, 10);  // Remap the period range to the reading range.

    RemapedAmountOfReadings2 = constrain(RemapedAmountOfReadings2, 1, 10);  // Constrain the value so it doesn't go below or above the limits.
    AmountOfReadings2 = RemapedAmountOfReadings2;                           // Set amount of readings as the remaped value.
  } else {
    PulseCounter2++;                                 // Increase the counter for amount of readings by 1.
    PeriodSum2 = PeriodSum2 + PeriodBetweenPulses2;  // Add the periods so later we can average.
  }
}