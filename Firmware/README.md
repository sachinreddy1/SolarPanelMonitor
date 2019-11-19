# Solar Panel Interface Box Firmware

This repository contains the necessary firmware for the Solar Panel Interface Box.

# Setup

 1. Copy the MCP3428 folder into your arduino hardware library
(e.g. C:\Program Files (x86)\Arduino\hardware\arduino\avr.) 
- This will allow the Arduino IDE to find the .h files necessary to compile and 
load the board. 
2. The OneWire.h and the DallasTemperature.h must be downloaded through the Arduino IDE.
- This will allow the DS18B20 temperatures sensors to operate over one digital I/O port.  
3. The ArduinoJson.h must be downloaded through the Arduino IDE.
- This will allow arduino to comminicate to a server/database using json objects.