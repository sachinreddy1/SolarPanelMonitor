#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoJson.h>

byte mac[] = {
  0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0x02
};
IPAddress ip(192, 168, 1, 177);
IPAddress myDns(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);

EthernetServer server(23);
boolean gotAMessage = false; 

const int CAPACITY = 200;

void setup() {

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

void loop() {
  EthernetClient client = server.available();

  if (client) {
    if (!gotAMessage) {
      Serial.println("We have a new client");
      client.println("Hello, client!");
      gotAMessage = true;
    }

    // Create JSON Object
    StaticJsonDocument<CAPACITY> root;
    root["voltage_1"] = 1.0;
    root["voltage_2"] = 2.0;
    root["voltage_3"] = 3.0;
    root["voltage_4"] = 4.0;

    // Serialize JSON Object to char array
    char sendValue[CAPACITY];
    serializeJson(root, sendValue);
    
    // Write JSON Object
    server.write(sendValue);
    Serial.print(sendValue);
    Serial.print("\n");
    
    // Read JSON object
    int len = client.available();
    if (len > 0) {
      byte buffer[80];
      client.read(buffer, len);
      Serial.write(buffer, len);
    }
    
    // Wait 3 seconds
    delay(3000);
    
    Ethernet.maintain();
  }
}
