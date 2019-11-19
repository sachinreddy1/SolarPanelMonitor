  
/*Libaries*/
#include <MCP3428.h>            /*Voltage and Current Sensor Library*/
#include <OneWire.h>            /*For the temp sensors */
#include <DallasTemperature.h>  /*DS18B20 specific Library*/
#include <SPI.h>                /*For ethernet interface*/
#include <Ethernet.h>           /*For ethernet interface*/
#include <ArduinoJson.h>        /*For ethernet interface*/

#define ONE_WIRE_BUS 9 // Data wire is plugged into port 4 on the Arduino.

/*Variables for the current senor: clean later*/
const int RELAY_0 = 7;
const int RELAY_1 = 8;

/*Variables*/
MCP3428 mcp3428;                        //Voltage and Current Object.

OneWire oneWire(ONE_WIRE_BUS);          // Setup a oneWire instance.
DallasTemperature sensors(&oneWire);    // Pass our oneWire reference to Dallas Temperature. 
int numberOfDevices;                    // Number of temperature devices found.
DeviceAddress tempDeviceAddress;        // Variable to store a found device address.

byte mac[] = {                          //MAC address for the ethernet interface.
  0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0x02
};

IPAddress ip(192, 168, 1, 177);         //Ethernet variables. NOTE: integrate IPAddressprinter that will automatically grab the IP address.
IPAddress myDns(192, 168, 1, 1);        //Ethernet variables.
IPAddress gateway(192, 168, 1, 1);      //Ethernet variables.
IPAddress subnet(255, 255, 0, 0);       //Ethernet variables.
EthernetServer server(23);
boolean gotAMessage = false; 
const int CAPACITY = 200;

/*Initial Setup*/
void setup()
{
  Serial.begin(9600);
  while (!Serial);                      // Wait for serial monitor. 

  /*Setup for the current sensor: add into a function later. Uses the MCP3428 object to read from channel 4*/
  
//  pinMode(RELAY_0, OUTPUT);
//  pinMode(RELAY_1, OUTPUT);
//  digitalWrite(RELAY_0, HIGH);
//  digitalWrite(RELAY_1, LOW);

  //Setup DS18B20
  setupDS18B20();
  //Setup MCP3428
//  setupMCP3428();
  //Setup W5500
//  setupW5500();
}

/*Main*/
void loop() {
  printTemp();
//  printVoltage();
//  printCurrent();


/*Ethernet Begin*/
//  EthernetClient client = server.available();
//
//  if (client) {
//    if (!gotAMessage) {
//      Serial.println("We have a new client");
//      client.println("Hello, client!");
//      gotAMessage = true;
//    }
//
//    // Create JSON Object
//    StaticJsonDocument<CAPACITY> root;
//    root["voltage_1"] = 1.0;
//    root["voltage_2"] = 2.0;
//    root["voltage_3"] = 3.0;
//    root["voltage_4"] = 4.0;
//
//    // Serialize JSON Object to char array
//    char sendValue[CAPACITY];
//    serializeJson(root, sendValue);
//    
//    // Write JSON Object
//    server.write(sendValue);
//    Serial.print(sendValue);
//    delay(3000);
//    
//    Ethernet.maintain();
//  }
/*Ethernet End*/
}

/*Functions*/
//Setup for the DS18B20 sensor.
void setupDS18B20(){
  sensors.begin();                              // Start up the library for temp sensors.
  numberOfDevices = sensors.getDeviceCount();   // Grab a count of devices on the wire
  
  // locate devices on the bus
  Serial.print("Locating devices...");
  Serial.print("Found ");
  Serial.print(numberOfDevices, DEC);
  Serial.println(" devices.");

  // Loop through each device, print out address
  for(int i=0;i<numberOfDevices; i++) {
    // Search the wire for address
    if(sensors.getAddress(tempDeviceAddress, i)) {
      Serial.print("Found device ");
      Serial.print(i, DEC);
      Serial.print(" with address: ");
      printAddress(tempDeviceAddress);
      Serial.println();
    } else {
      Serial.print("Found ghost device at ");
      Serial.print(i, DEC);
      Serial.print(" but could not detect address. Check power and cabling");
    }
  }
}

//Setup for the MCP3428 sensor. 
void setupMCP3428(){
  Serial.println("MCP3428 Test");
  
  while(!mcp3428.test()){
  Serial.println("ERROR: MCP3428 not found");
  delay(1000);
  }
  Serial.println("SUCCESS: MCP3428 found");
  delay(1000);
}

//Setup for the Ethernet Interface
void setupW5500(){
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  Serial.println("Trying to get an IP address using DHCP");
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) {
        delay(1);
      }
    }
    if (Ethernet.linkStatus() == LinkOFF) {
      Serial.println("Ethernet cable is not connected.");
    }
    Ethernet.begin(mac, ip, myDns, gateway, subnet);
  }
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
  
  server.begin();
}
//Get and print temp
void printTemp(){
  sensors.requestTemperatures(); // Send the command to get temperatures
  
  // Loop through each device, print out temperature data
  for(int i=0;i<numberOfDevices; i++) {
    // Search the wire for address
    if(sensors.getAddress(tempDeviceAddress, i)){
    
    // Output the device ID
    Serial.print("Temperature for device: ");
    Serial.println(i,DEC);

    // Print the data
    float tempC = sensors.getTempC(tempDeviceAddress);
    Serial.print("Temp C: ");
    Serial.print(tempC);
    Serial.print(" Temp F: ");
    Serial.println(DallasTemperature::toFahrenheit(tempC)); // Converts tempC to Fahrenheit
    }   
  }
  delay(500);
}

//Print DS18B20 sensor address.
void printAddress(DeviceAddress deviceAddress) {
  for (uint8_t i = 0; i < 8; i++) {
    if (deviceAddress[i] < 16) Serial.print("0");
      Serial.print(deviceAddress[i], HEX);
  }
}
//Print the voltages read from the MCP3428 sensor.
void printVoltage(){
  float channel_A_volt = mcp3428.readADC(1)*57;
  float channel_B_volt = mcp3428.readADC(2)*43.2;
  float channel_C_volt = mcp3428.readADC(3)*14.3;
  
  Serial.println("ADC Voltages:");
  Serial.print("CH_A: ");
  Serial.println(channel_A_volt, 7);
  Serial.print("CH_B: ");
  Serial.println(channel_B_volt, 7);
  Serial.print("CH_C: ");
  Serial.println(channel_C_volt, 7);
  delay(1000);
  }

void printCurrent(){
  float channel_4_current = 5*(mcp3428.readADC(4)*2.5-0.5);
  Serial.println("ADC Current:");
  Serial.print("CH_4: ");
  Serial.println(channel_4_current, 7); 
  delay(5000);
  }
