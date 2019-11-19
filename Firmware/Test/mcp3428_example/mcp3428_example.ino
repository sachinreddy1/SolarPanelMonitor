#include <MCP3428.h>

MCP3428 mcp3428;
int count;

void setup()
{
  Serial.begin(9600);
  while (!Serial);             // Leonardo: wait for serial monitor
  Serial.println("MCP3428 Test");

  while(!mcp3428.test()){
    Serial.println("ERROR: MCP3428 not found");
    delay(1000);
  }
  Serial.println("SUCCESS: MCP3428 found");
  delay(1000);
}


void loop() {
  Serial.println("ADC Voltages:");
  Serial.print("CH1: ");
  Serial.println(mcp3428.readADC(1), 7);
  Serial.print("CH2: ");
  Serial.println(mcp3428.readADC(2), 7);
  Serial.print("CH3: ");
  Serial.println(mcp3428.readADC(3), 7);
  Serial.print("CH4: ");
  Serial.println(mcp3428.readADC(4), 7);
  Serial.println();
}
