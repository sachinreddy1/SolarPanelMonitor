/*Libraries*/
#include <DS18B20.h>
#include <MCP3428.h>
#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoJson.h>


/*Constants*/
#define CH_ONE_VOLT_CONVERSION_FACTOR 57
#define CH_TWO_VOLT_CONVERSION_FACTOR 43.2
#define CH_THREE_VOLT_CONVERSION_FACTOR 14.3
#define TEMP_READ_FAIL -777.777
#define CH_READ_FAIL -777.777
#define STATE_ZERO 0
#define STATE_ONE 1
#define STATE_TWO 2
#define STATE_THREE 3
#define CHANNEL_ONE 1
#define CHANNEL_TWO 2
#define CHANNEL_THREE 3
#define CHANNEL_FOUR 4
#define NUM_CHANNELS 4
#define NUM_TEMP_SENSORS 6

/*Helper Functions*/
void setTempThreshold();                //All set Threshold functions have to either be removed or modified for ethernet communication. 
void checkTemp();
bool setRelays(int relayZero, int relayOne);
void setVoltThreshold();
void setCurrentThreshold();
void flushRecieve();                    // Clears the incoming serial buffer. Possibly remove later since this is only for serial. 
float checkChannel(int channel);                    // channels: 1 = Panel A, 2 = Panel B, 3 = Panel C, 4 = Current.
void checkVoltageCurrent();                    

/*Time Interval Variables for Multitasking*/
unsigned long prevTime1 = millis();      // Initialize timing for multitasking. Task 1.
unsigned long prevTime2 = millis();      // Task 2.
long timeIntTempSensors = 0;        // Time Interval for Temperatures Sensors to every 30 seconds. 
long timeIntVoltCurrentSensor  = 0;     // Time Interval for Voltage and Current Sensor. Set to 0 so that the process will always check whenever it is able to.

/*Relay Variabes*/
int relayConfig = 0;                    // Tracks the current state of the relay configuration. State = Relay Out: Interface Out.
                                        // 0 = Panel_B: NC. 1 = Panel_C: Panel_D. 2 = Panel_B: Panel_C. 3 = Panel_A: Panel_D.
const int relay_0 = 7;                  // Relay 0 connected to pin 7.
const int relay_1 = 8;                  // Relay 1 connected to pin 8.
//int userInput1, userInput2;             // Delete later. Used for serial print.

/*Temperature Sensor Variables*/
DS18B20 ds18b20;                        // Temp Sensor Object.
float *tempPtr = NULL;                  // Pointer to array of current temperature values.        
float tempThreshold = 27.0;             // Temperature Threshold.
float userInput = 0.0;                  // User defined input.
float tempArray[NUM_TEMP_SENSORS] = {0.0,0.0,0.0,0.0,0.0,0.0};

/*Voltage and Current Sensor Variables*/
MCP3428 mcp3428;
float channelArray[NUM_CHANNELS] = {0.0,0.0,0.0,0.0};
float voltThreshold = 36.0;              // Voltage Threshold.
float currentThreshold = 0.75;           // Current Threshold.

/*LED Variables*/
const int ledOutputEnable_pin = 6;

 /*Ethernet Variables*/
 EthernetServer server(23);                           //Gets the port and the server.
 byte mac[] = {0x00, 0xDE, 0xAD, 0xBE, 0xEF, 0xEE};
 EthernetClient client;
 const int CAPACITY = 200;                            //Length of the JSON object.

// ----------------------------------------- //

void setup() {
  Serial.begin(9600);
  while(!Serial);
  
  /*Initialize Relay Pins so that the output is disconnected from the electrical load.*/
  Serial.println("Initializing Relays...");
  pinMode(relay_0, OUTPUT);
  pinMode(relay_1, OUTPUT);
  digitalWrite(relay_0, LOW);
  digitalWrite(relay_1, LOW);
  
  /*Initial Test and check of all components*/
  while(!ds18b20.test());
  while(!mcp3428.test());
  setEthernet(); // Write a test function for network connectivity. 
  Serial.println("All components initialized successfully.");
  delay(1000);
 /*Intiailize LEDs. NOTE: Code later*/
  pinMode(ledOutputEnable_pin, OUTPUT);

  /*Initialize sensor parameters*/
//  setTempThreshold();
//  setVoltThreshold();
//  setCurrentThreshold();
//  Serial.println("All Thresholds Set.");
  Serial.println("Beginning System Operations");
  delay(1000);
}

/*
* Implementing multitasking leveraging the millis method. Overall program flow is segmented into Tasks. 
* Priorities of tasks are implemented with the highest priority first.
*/
void loop() {
  unsigned long currTime = millis();
//  Serial.println("Hello, fuck");
  client = server.available();

   
  // Task 1: Check Voltage and Current.
  if(currTime - prevTime1 > timeIntVoltCurrentSensor){
    checkVoltageCurrent();
    prevTime1 = currTime;
  }
  
  // Task 2: Check Temperature.
  if(currTime - prevTime2 > timeIntTempSensors){
    checkTemp();
    prevTime2 = currTime;
  }

  // Task 3: Check for User Inputs?? Replace with inputs recieved from the client side. Maybe a flag? Don't know yet. 
//  if(Serial.available()){
//    userInput1 = Serial.parseInt();
//    flushRecieve();
//    while(!Serial.available());
//    if(Serial.available()){
//      userInput2 = Serial.parseInt();
//      flushRecieve();
//    }
//    while(!setRelays(userInput1, userInput2)){
//      Serial.println("Invalid Relay Configuration");
//      Serial.println("Enter First Realay Config(0 or 1): ");
//      while(!Serial.available());
//      if(Serial.available() > 0){
//        userInput1 = Serial.parseFloat();
//        flushRecieve();
//      }
//      while(!Serial.available());
//      if(Serial.available()){
//        userInput2 = Serial.parseInt();
//        flushRecieve();
//      }
//    }
//    Serial.print("Relay State: ");
//    Serial.println(relayConfig,DEC);
//  }

  if(client){
    int len = client.available();
    if (len > 0) {
      byte buffer[80];
      client.read(buffer, len);

     Ethernet.maintain();
     //Parser:
     StaticJsonDocument<CAPACITY> receiveObj;
     deserializeJson(receiveObj, buffer);
     voltThreshold = receiveObj["V"];
     currentThreshold = receiveObj["C"];
     tempThreshold = receiveObj["T"];
     if (relayConfig != receiveObj["S"]){
      if (userSetRelays(receiveObj["S"])) {
        relayConfig = receiveObj["S"];
      }
     }
    }
  
    Ethernet.maintain();
  }
  Ethernet.maintain();
}

void setEthernet(){  
  Serial.println("Trying to get an IP address using DHCP");
  int ethernetVal = Ethernet.begin(mac);

  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
  
  server.begin();
}

// ----------------------------------------- //

//void setTempThreshold(){
//  Serial.print("Enter MAX temperature threshold (-45.0 to 85.0): \n");
//  while(!Serial.available());
//  if(Serial.available() > 0){
//    userInput = Serial.parseFloat();
//    flushRecieve(); 
//    while(!ds18b20.setConfig(userInput)){
//      Serial.println("Invalid Temperature Threshold");
//      Serial.println("Enter MAX temperature threshold (-45.0 to 85.0): ");
//      while(!Serial.available());
//      if(Serial.available() > 0){
//        userInput = Serial.parseFloat();
//        flushRecieve(); 
//      }
//    }
//  }
//  tempThreshold = ds18b20.getTempLimit();
//  Serial.print("Set MAX Temperature for Temperature Sensors to: ");
//  Serial.println(tempThreshold, DEC);
//  delay(1000);
//}

//void setVoltThreshold(){
//  Serial.print("Enter MAX Voltage threshold (0 to 72.9): ");
//  while(!Serial.available());
//  if(Serial.available() > 0){
//    userInput = Serial.parseFloat();
//    flushRecieve(); 
//    while(!mcp3428.setVoltage(userInput)){
//      Serial.println("Invalid Voltage Threshold");
//      Serial.println("Enter MAX Voltage threshold (0 to 72.9): ");
//      while(!Serial.available());
//      if(Serial.available() > 0){
//        userInput = Serial.parseFloat();
//        flushRecieve(); 
//      }
//    }
//  }
//  voltThreshold = mcp3428.getVoltThreshold();
//  Serial.print("Set Voltage Threshold to: ");
//  Serial.println(voltThreshold, DEC);
//  delay(1000);
//}

//void setCurrentThreshold(){
//  Serial.print("Enter MAX Current threshold (0 to 5.83): ");
//  while(!Serial.available());
//  if(Serial.available() > 0){
//    userInput = Serial.parseFloat();
//    flushRecieve(); 
//    while(!mcp3428.setCurrent(userInput)){
//      Serial.println("Invalid Current Threshold");
//      Serial.println("Enter MAX Current threshold (0 to 5.83): ");
//      while(!Serial.available());
//      if(Serial.available() > 0){
//        userInput = Serial.parseFloat();
//        flushRecieve(); 
//      }
//    }
//  }
//  currentThreshold = mcp3428.getCurrentThreshold();
//  Serial.print("Set Current Threshold to: ");
//  Serial.println(currentThreshold, DEC);
//  delay(1000);
//}

// ----------------------------------------- //

void flushRecieve(){
  while(Serial.available()){
    Serial.read();
  }
}

float getChannel(int channel){
  float ret_val = CH_READ_FAIL;
  
  switch(channel){
    case CHANNEL_ONE:
      ret_val = mcp3428.readADC(CHANNEL_ONE) * CH_ONE_VOLT_CONVERSION_FACTOR;
      break;
    case CHANNEL_TWO:
      ret_val = mcp3428.readADC(CHANNEL_TWO) * CH_TWO_VOLT_CONVERSION_FACTOR;
      break;
    case CHANNEL_THREE:
      ret_val = mcp3428.readADC(CHANNEL_THREE) * CH_THREE_VOLT_CONVERSION_FACTOR;
      break;
    case CHANNEL_FOUR:
      ret_val = 5 * (mcp3428.readADC(CHANNEL_FOUR) * 2.5 - 0.5);
      break;
    default:
      break;
  }
  return ret_val;
  
}

// ----------------------------------------- //

void checkVoltageCurrent(){

  for(int channel = 1; channel<=NUM_CHANNELS; channel++){
    if(!mcp3428.test()){ //Always have to check when entering a for loop.
    setRelays(LOW,LOW);
    Serial.println("Warning: voltage and test communication failure");
    }
    channelArray[channel-1] = getChannel(channel);
    if(channel<4){
      if(channelArray[channel-1] > voltThreshold){
        setRelays(LOW,LOW);
        Serial.println(mcp3428.getVoltThreshold());
        Serial.println(channelArray[channel-1]);
        Serial.println("Warning: Overvoltage");
      }
    }
    else{
      if(channelArray[channel-1] > currentThreshold){
        setRelays(LOW,LOW);
        Serial.println(mcp3428.getCurrentThreshold());
        Serial.println(channelArray[channel-1]);
        Serial.println("Warning: Overcurrent");
      }
    }
  }
  
//  for(int channel =1; channel<=NUM_CHANNELS; channel++){
//    Serial.print("Channel: ");
//    Serial.print(channel, DEC);
//    Serial.print(" Value: ");
//    Serial.println(channelArray[channel-1], DEC);
//  }
//  delay(1000);

  if (client) {
    // Create JSON Object
    StaticJsonDocument<CAPACITY> sendObj;
    sendObj["V1"] = channelArray[CHANNEL_ONE-1];
    sendObj["V2"] = channelArray[CHANNEL_TWO-1];
    sendObj["V3"] = channelArray[CHANNEL_THREE-1];
    sendObj["C1"] = channelArray[CHANNEL_FOUR-1];
    sendObj["T1"] = tempArray[0];
    sendObj["T2"] = tempArray[1];
    sendObj["T3"] = tempArray[2];
    sendObj["T4"] = tempArray[3];
    sendObj["T5"] = tempArray[4];
    sendObj["T6"] = tempArray[5];
    
    // Serialize JSON Object to char array
    char sendValue[CAPACITY];
    serializeJson(sendObj, sendValue);
    
    // Write JSON Object
    server.write(sendValue);
    Serial.print(sendValue);
    Serial.print("\n");
    Ethernet.maintain();
  }
}

void checkTemp(){
  tempPtr = ds18b20.getTempC();
  for(int i = 0; i<ds18b20.getNumberOfDevices();i++){
    tempArray[i] = *(tempPtr+i);
    if(*(tempPtr+i) <= TEMP_READ_FAIL || *(tempPtr+i) >= tempThreshold){
      setRelays(LOW, LOW);
      if(*(tempPtr+i) <= TEMP_READ_FAIL){
        setRelays(LOW,LOW);
        Serial.println("Warning: Check Temperature Sensors");
      }
      else{
        setRelays(LOW,LOW);
        Serial.println("Warning: Solar Panel Temperature is Critical");
      }
    }
//    else{
//      Serial.print("Device: ");
//      Serial.println(i, DEC);
//      Serial.print("Temp C: ");
//      Serial.println(*(tempPtr+i));
//      delay(1000);
//    }
 }
   if (client) {
     // Create JSON Object
     StaticJsonDocument<CAPACITY> sendObj;
     sendObj["V1"] = channelArray[CHANNEL_ONE-1];
     sendObj["V2"] = channelArray[CHANNEL_TWO-1];
     sendObj["V3"] = channelArray[CHANNEL_THREE-1];
     sendObj["C1"] = channelArray[CHANNEL_FOUR-1];
     sendObj["T1"] = tempArray[0];
     sendObj["T2"] = tempArray[1];
     sendObj["T3"] = tempArray[2];
     sendObj["T4"] = tempArray[3];
     sendObj["T5"] = tempArray[4];
     sendObj["T6"] = tempArray[5];
    
     // Serialize JSON Object to char array
     char sendValue[CAPACITY];
     serializeJson(sendObj, sendValue);
      
     // Write JSON Object
     server.write(sendValue);
     Serial.print(sendValue);
     Serial.print("\n");
     Ethernet.maintain();
  }
}

// ----------------------------------------- //

bool setRelays(int relayZero, int relayOne){
  bool ret = true;
  // Check relay configuration state. 
  if( relayZero == 0 && relayOne == 0){relayConfig = STATE_ZERO;}
  else if( relayZero == 0 && relayOne == 1){relayConfig = STATE_ONE;}
  else if( relayZero == 1 && relayOne == 0){relayConfig = STATE_TWO;}
  else if( relayZero == 1 && relayOne == 1){relayConfig = STATE_THREE;}
  else{ 
    //Invalid relay configuration. Disconnect for safety.
    digitalWrite(relay_0, LOW);
    digitalWrite(relay_1, LOW);
    relayConfig = STATE_ZERO;
    ret = false;
  }
  // Set the relays.
  if(ret){
  digitalWrite(relay_0, relayZero);
  digitalWrite(relay_1, relayOne);
  }
  return ret;
}

bool userSetRelays(int relayState){
  bool ret = true; 
  switch(relayState){
    case STATE_ZERO:
      ret =  setRelays(0, 0);
      break;
    case STATE_ONE:
      ret =  setRelays(0, 1);
      break;
    case STATE_TWO:
      ret =  setRelays(1, 0);
      break;
    case STATE_THREE:
      ret =  setRelays(1, 1);
      break;
    default:
      digitalWrite(relay_0, LOW);
      digitalWrite(relay_1, LOW);
      ret = false;
      break;
  }
  return ret;
}
