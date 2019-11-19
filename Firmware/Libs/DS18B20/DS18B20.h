/*
  DS18B20.h - Library for the DS18B20 Temperature Sensors.
  Created by Douglas J. Lee, October 30, 2019.
  For ECE 445 Senior Design.
  Project: Smart Interface Box for Solar Panels.
*/

#ifndef DS18B20_h
#define DS18B20_h

#include "Arduino.h"
#include "OneWire.h"
#include "DallasTemperature.h"

#define ONE_WIRE_BUS 9          // Data wire for temperature sensors is plugged into port 4 on the Arduino.
#define MAX_TEMP_DEFAULT 85.0   // Maximum operating temperature of the Solar Panel.
#define MIN_TEMP_DEFAULT -40.0  // Minimum operating temperature of the Solar Panel.
#define MAX_NUM_TEMP_SENSORS 6  // Currently, the board was for up to 5 total temp sensors.

class DS18B20{
  public:
    DS18B20();
    bool setConfig(float temperature_threshold);
    bool test();
    float * getTempC();
    int getNumberOfDevices();
    float getTempLimit();

  private:
    int numberOfDevices;
    float tempLimit;
};




#endif
