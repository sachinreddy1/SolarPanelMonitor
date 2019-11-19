#ifndef MCP3428_h
#define MCP3428_h

#include "Arduino.h"
#include <Wire.h>
#include <math.h>

// I2C address
#define MCP3428_ADDRESS 0x68

// Configuration Options
#define MCP3428_PGA 1    // Internal gain of 1; Options: 1, 2, 4, 8
#define MCP3428_SPS 16   //16-bit resolution; Options: 12, 14, 16
#define MCP3428_MODE 1   // Continuous conversion mode; Options: 0 = One shot mode, 1 = continuous mode.
#define MIN_VOLT_DEFAULT 0
#define MAX_VOLT_DEFAULT 72.9
#define MIN_CURRENT_DEFAULT 0
#define MAX_CURRENT_DEFAULT 5.83

class MCP3428{
  public:
    MCP3428();
    bool test();
    double readADC(uint8_t channel);
    bool setVoltage(float voltageThreshold);
    bool setCurrent(float currentThreshold);
    float getVoltThreshold();
    float getCurrentThreshold();

  private:
    double convertRaw(long raw_adc);
    void setConfig(uint8_t channel);
    bool checkConversion();
    long raw_adc;
    uint8_t i;
    uint8_t testvar;
    uint8_t config;
    uint8_t numBytes;
    uint8_t data[3];
    float voltThreshold;
    float currentThreshold;
};

#endif
