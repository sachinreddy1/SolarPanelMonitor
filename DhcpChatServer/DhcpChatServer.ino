#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoJson.h>

byte mac[] = {
//  0x00, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE
  0x00, 0xDE, 0xAD, 0xBE, 0xEF, 0xEE
};

EthernetServer server(23);
const int CAPACITY = 200;

int relayConfig = 0;
int manualSwitch = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Trying to get an IP address using DHCP");
  int ethernetVal = Ethernet.begin(mac);
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
  server.begin();
}

void loop() {
  EthernetClient client = server.available();

  if (client) {
    // Create JSON Object
    StaticJsonDocument<CAPACITY> sendObj;
    sendObj["V1"] = 1.0;
    sendObj["V2"] = 2.0;
    sendObj["V3"] = 3.0;
    sendObj["C1"] = 4.0;
    sendObj["T1"] = 0.0;
    sendObj["T2"] = 1.0;
    sendObj["T3"] = 2.0;
    sendObj["T4"] = 3.0;
    sendObj["T5"] = 4.0;
    sendObj["T6"] = 5.0;
    sendObj["S"] = relayConfig;
    sendObj["X"] = manualSwitch;

    // Serialize JSON Object to char array
    char sendValue[CAPACITY];
    serializeJson(sendObj, sendValue);
    
    // Write JSON Object
    server.write(sendValue);
    Serial.print(sendValue);
    Serial.print("\n");

    // --------------------------------------- //
    
    // Read JSON object
    int len = client.available();
    if (len > 0) {
      byte buffer[80];
      client.read(buffer, len);

      // Parse the JSON object
      StaticJsonDocument<CAPACITY> receiveObj;
      deserializeJson(receiveObj, buffer);
      
      // Storing JSON values individually
      float voltageVal = receiveObj["V"];
      float currentVal = receiveObj["C"];
      float temperatureVal = receiveObj["T"];
      relayConfig = receiveObj["S"];
      manualSwitch = receiveObj["M"];

      // Printing values individually
      Serial.print("Voltage Threshold: ");
      Serial.println(voltageVal);
      Serial.print("Current Threshold: ");
      Serial.println(currentVal);
      Serial.print("Temperature Threshold: ");
      Serial.println(temperatureVal);
      Serial.print("Switch Configuration: ");
      Serial.println(relayConfig);
      Serial.print("Manual Switch: ");
      Serial.println(manualSwitch);
    }
    
    // Wait 3 seconds
    delay(3000);
    
    Ethernet.maintain();
  }
}
