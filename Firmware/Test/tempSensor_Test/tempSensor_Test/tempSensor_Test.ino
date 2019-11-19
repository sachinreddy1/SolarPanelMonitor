#include <DS18B20.h>

DS18B20 ds18b20;
float *p; //ptr to the temparture data array. 
//float p;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial);

  Serial.println("Temp Sensor Test");
  while(!ds18b20.test()){
    Serial.println("Error: Something went wrong");
    delay(1000);
  }
  Serial.println("Success: Good to go");
  delay(1000);



  // Test threshold settings.
  float testlimit = ds18b20.getTempLimit();
  Serial.print("Default Temp Threshold: ");
  Serial.println(testlimit, DEC);
  delay(1000);
  
  if(ds18b20.setConfig(0.0)){
    testlimit = ds18b20.getTempLimit();
  }
  else{
    Serial.println("Provided Temp Threshold is out of range (-45 to 85)");
  }
  Serial.print("User Set Temp Threshold: ");
  Serial.println(testlimit, DEC);
  delay(1000);

  Serial.println("Enter MAX Temp: ");
  while(!Serial.available());
  if(Serial.available()){
    float userInput = Serial.parseFloat();
    Serial.println(userInput,DEC);
    ds18b20.setConfig(userInput);
    if(!ds18b20.setConfig(userInput)){
      Serial.println("Provided Temp Threshold is out of range (-45 to 85)");
    }
    else{
     testlimit = ds18b20.getTempLimit();
    }
    Serial.println(testlimit, DEC);
  }
  Serial.print("User Set Temp Threshold: ");
  Serial.println(testlimit, DEC);
  delay(1000);

  
}

void loop() {
  // put your main code here, to run repeatedly:
  int num = ds18b20.getNumberOfDevices();
  Serial.print("Number of Devices: ");
  Serial.println(num, DEC);
  p = ds18b20.getTempC();
  for(int i = 0; i<ds18b20.getNumberOfDevices();i++){
    Serial.print("Device: ");
    Serial.println(i, DEC);
    Serial.print("Temp C: ");
    Serial.println(*(p+i));
//    Serial.println(p, DEC);
    delay(1000);
  }
  
}
