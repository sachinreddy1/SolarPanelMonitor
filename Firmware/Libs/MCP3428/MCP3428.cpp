/*
 * Edit History:
 * 11/12/2019 -- Added in the threshold variables and associated functions. -dlee242.
 */
#include "MCP3428.h"
#include "Arduino.h"
#include <Wire.h>
#include <math.h>

// Class constructor. I2C adddress is non-configurable and set to 0x68.
MCP3428::MCP3428(){
  Wire.begin();
  this->voltThreshold = MAX_VOLT_DEFAULT;
  this->currentThreshold = MAX_CURRENT_DEFAULT;
}

// Test to see that device acknowledges on attempted communication.
bool MCP3428::test(){
  Wire.beginTransmission(MCP3428_ADDRESS);
  return(Wire.endTransmission() == 0);
}

// Set and write the configuration byte to the device.
void MCP3428::setConfig(uint8_t channel){
  // Set RDY bit;
  config = 1;
  config = config << 2;
  // Set channel bits;
  config |= (channel - 1);
  config = config << 1;
  // Set mode bits;
  config |= MCP3428_MODE;
  config = config << 2;
  // Set resolution bits;
  config |= int((MCP3428_SPS - 12)/2);
  config = config << 2;
  // Set mode bits;
  config |= int(log(MCP3428_PGA)/log(2));

  // Write configuration bit to MCP3428
  Wire.beginTransmission(MCP3428_ADDRESS);
  Wire.write(config);
  Wire.endTransmission();
}

// Check that the conversion is ready.
bool MCP3428::checkConversion(){
  i = 0;
  numBytes = 3;
  Wire.requestFrom(MCP3428_ADDRESS, numBytes);

  while(Wire.available()){
      data[i++] = Wire.read();
      testvar = data[numBytes - 1] >> 7;
  }
  return testvar;
}

// Convert raw data into actual voltage levels;
double MCP3428::convertRaw(long raw_adc){
  //convertedRaw = (double) raw_adc;
  return (double(raw_adc) / 32767.0) * 2.048;
}

// Read the ADC channel.
double MCP3428::readADC(uint8_t channel){
  raw_adc = 0;

  setConfig(channel);

  while(checkConversion() == 1);

  switch (MCP3428_SPS){
    case 12:
      raw_adc = data[0];
      raw_adc &= 0b00001111;
      raw_adc = raw_adc << 8;
      raw_adc |= data[1];

      if(raw_adc > 2047){
        raw_adc = raw_adc - 4096;
      }
      break;

    case 14:
      raw_adc = data[0];
      raw_adc &= 0b00111111;
      raw_adc = raw_adc << 8;
      raw_adc |= data[1];

      if(raw_adc > 8191){
        raw_adc = raw_adc - 16384;
      }
      break;

    case 16:
      raw_adc = data[0];
      raw_adc = raw_adc << 8;
      raw_adc |= data[1];

      if(raw_adc > 32767){
        raw_adc = raw_adc - 65536;
      }
      break;
    }
    //return raw_adc;
    return convertRaw(raw_adc);
}

/*Function: Sets the Maximum Voltage Threshold
* Input: voltageThreshold
* Output: Boolean
*/
bool MCP3428::setVoltage(float voltThreshold){
  if( voltThreshold < MIN_VOLT_DEFAULT || voltThreshold > MAX_VOLT_DEFAULT){
    return false;
  }
  else{
    this->voltThreshold = voltThreshold;
    return true;
  }
}

/*Function: Sets the Maximum Current Threshold
* Input:currentThreshold
* Output: Boolean
*/
bool MCP3428::setCurrent(float currentThreshold){
  if( currentThreshold < MIN_CURRENT_DEFAULT || currentThreshold > MAX_CURRENT_DEFAULT){
    return false;
  }
  else{
    this->currentThreshold = currentThreshold;
    return true;
  }
}

float MCP3428::getVoltThreshold(){
  return this->voltThreshold;
}

float MCP3428::getCurrentThreshold(){
  return this->currentThreshold;
}
