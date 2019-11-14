#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoJson.h>

byte mac[] = {
//  0x00, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE
  0x00, 0xDE, 0xAD, 0xBE, 0xEF, 0xEE
};
IPAddress ip(192, 168, 1, 177);
IPAddress myDns(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);

EthernetServer server(23);

const int CAPACITY = 200;

void setup() {
  Serial.begin(9600);

  Serial.println("Trying to get an IP address using DHCP");
  int ethernetVal = Ethernet.begin(mac);
  
  if (ethernetVal == 0) {
    Ethernet.begin(mac, ip, myDns, gateway, subnet);
  }
  
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
  
  server.begin();
}

void loop() {
  EthernetClient client = server.available();

  if (client) {
    // Create JSON Object
    StaticJsonDocument<CAPACITY> root;
    root["V1"] = 1.0;
    root["V2"] = 2.0;
    root["V3"] = 3.0;
    root["V4"] = 4.0;

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
