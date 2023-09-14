//KONEKSI NODEMCU dengan UNO
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
SoftwareSerial mm (D2, D1);


void setup(){
  mm.begin(9600);
  Serial.begin(9600);
}

void loop(){
  String sensorstring = mm.readStringUntil('\n');
  Serial.println("[+] Data dari Arduino UNO : "+sensorstring);
  delay(1000);
}
