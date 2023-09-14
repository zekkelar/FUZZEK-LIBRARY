//KONEKSI NODEMCU dengan UNO
#include <SoftwareSerial.h>
SoftwareSerial mm (3, 2);
#include <ArduinoJson.h>


void setup(){
  mm.begin(9600);
  Serial.begin(9600);
}

void loop(){
  mm.println("Ini data Dari UNO");
  delay(1000);
}
