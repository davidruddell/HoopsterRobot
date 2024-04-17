#include "DFRobot_WT61PC.h"

// Use Serial1 for communication
DFRobot_WT61PC sensor(&Serial1);

void setup()
{
  // Use Serial for debugging
  Serial.begin(115200);
  // Use Serial1 for communication
  Serial1.begin(9600);
  // Revise the data output frequency of sensor
  sensor.modifyFrequency(FREQUENCY_200HZ);
}

void loop()
{
  if (sensor.available()) {
    //angle information of X, Y, Z 
    //Serial.print("Angle\tX: "); Serial.print(sensor.Angle.X); 
    Serial.print("\tY: "); Serial.print(sensor.Angle.Y); 
    //Serial.print("\tZ: "); Serial.println(sensor.Angle.Z);
  }
}