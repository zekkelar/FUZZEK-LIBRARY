
#include <dht.h>

#define DATA_PIN 2 // Definisi Pin untuk DHT22

dht DHT; // Buat DHT object

void setup() {
  
  Serial.begin(9600); 
}
void loop() {
  
  int readData = DHT.read22(DATA_PIN); // baca Data dari sensor
  float t = DHT.temperature; // Ambil nilai Suhu
  float h = DHT.humidity; // Ambil nilai Kelembaban
  
  // Mencetak output ke Serial monitor
  Serial.print("SUHU = ");
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print("    KELEMBABAN = ");
  Serial.print(h);
  
  Serial.println(" % ");
  delay(1000);
  
}
