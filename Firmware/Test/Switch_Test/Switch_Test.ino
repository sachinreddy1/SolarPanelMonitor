/* Manual Switch Configuration Test for Smart Box Interface for Solar Panels
 * ECE 445 Senior Design 
 * Created 29 October 2019
 * By Douglas J. Lee
 */


const int SwitchPin_1 = 2;
const int SwitchPin_2 = 3;
const int SwitchPin_3 = 4; 
const int SwitchPin_4 = 5;


int Switch1 = 0;
int Switch2 = 0; 
int Switch3 = 0; 
int Switch4 = 0; 
 


void setup() {
  // Start serial communication.
  Serial.begin(9600);
  //Setup Pins.
  pinMode(SwitchPin_1, INPUT);
  pinMode(SwitchPin_2, INPUT);
  pinMode(SwitchPin_3, INPUT);
  pinMode(SwitchPin_4, INPUT);
  
}

void loop() {
  Switch1 = digitalRead(SwitchPin_1);
  printPins(Switch1, SwitchPin_1);
  Switch2 = digitalRead(SwitchPin_2);
  printPins(Switch2, SwitchPin_2);
  Switch3 = digitalRead(SwitchPin_3);
  printPins(Switch3, SwitchPin_3);
  Switch4 = digitalRead(SwitchPin_4);
  printPins(Switch4, SwitchPin_4);

  Serial.println("***********************************");
  delay(1000);

}

void printPins(int OutputVal,int Pin){
  Serial.print("Switch Pin: " );
  Serial.print(Pin);
  Serial.print("\t output = ");
  Serial.println(OutputVal);
  delay(200);
}
