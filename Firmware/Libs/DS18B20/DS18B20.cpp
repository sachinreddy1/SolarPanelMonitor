/*
  DS18B20.h - Library for the DS18B20 Temperature Sensors.
  Created by Douglas J. Lee, October 30, 2019.
  For ECE 445 Senior Design.
  Project: Smart Interface Box for Solar Panels.
*/
#include "DS18B20.h"
#include "Arduino.h"
#include "OneWire.h"
#include "DallasTemperature.h"

/*File Level Global Variables*/

OneWire oneWire(ONE_WIRE_BUS);          // Setup a oneWire instance.
DallasTemperature sensors(&oneWire);    // Pass our oneWire reference to Dallas Temperature.
DeviceAddress tempDeviceAddress;        // Variable to store a found device address.


/*Constructor*/
DS18B20::DS18B20(){
  sensors.begin();
  numberOfDevices = sensors.getDeviceCount();
  tempLimit = MAX_TEMP_DEFAULT; // Solar panel MAX limit default.
}

/*
 *Function: setConfig - allows user to set the max operating temperature based on the design parameters
                        based on the Solar Panel operating temperature range.
 *Inputs: temperature_threshold
 *Outputs: Boolean
*/
bool DS18B20::setConfig(float tempLimit){
  if(tempLimit < MIN_TEMP_DEFAULT || tempLimit > MAX_TEMP_DEFAULT){
    return false;
  }
  else{
    this->tempLimit = tempLimit;
    return true;
  }
}

/*
 *Function: test - Tests to see if temp sensors are connected and valid.
 *Inputs: None
 *Outputs: Boolean
*/
bool DS18B20::test(){
  /*Validate the number of sensors*/
  if(numberOfDevices>MAX_NUM_TEMP_SENSORS || numberOfDevices < 0){
    return false;
  }
  numberOfDevices = sensors.getDeviceCount();
  /*Validate the address of each sensor*/
  for(int i=0;i<numberOfDevices; i++) {
    // Search the wire for address
    if(!sensors.getAddress(tempDeviceAddress, i)) {
      return false;
    }
  }
  return true;
}

/*
 *Function: getTempC - gets the temperature, in celsius, of each temp sensor.
 *Inputs: None
 *Outputs: array of floats containing temperature of each temp sensor.
*/
float * DS18B20::getTempC(){
  static float tempC[MAX_NUM_TEMP_SENSORS];  // Array for temperature data.
  // static float tempC = 0.0;
  sensors.requestTemperatures();        // Send request to sensors.
  numberOfDevices = sensors.getDeviceCount();
  // Loop through each device, print out temperature data
  for(int i=0;i<numberOfDevices; i++) {
    // Search the wire for address
    if(sensors.getAddress(tempDeviceAddress, i)){
      tempC[i] = sensors.getTempC(tempDeviceAddress);
    }
    else{
      tempC[i] = -777.777;             // Device error.
    }
  }
  return tempC;
}

/*
 *Function: getNumberOfDevices - gets the number of temp sensors.
 *Inputs: None
 *Outputs: Number of temp sensors detected.
*/
int DS18B20::getNumberOfDevices(){
  numberOfDevices = sensors.getDeviceCount();
  return numberOfDevices;
}

/*
 *Function: getTempLimit- gets the current temperature set threshold.
 *Inputs: None
 *Outputs: temprature threshold set value.
*/
float DS18B20::getTempLimit(){
  return tempLimit;
}
