/*
BERISIKAN beberapa module disini
dan juga ada koneksi dengan nodemcu
List module yang digunakan:
Arduino:
1. Soil [Moisture]
2. Humidity + Temperature
3. Raindrop
4. Gyroscope
*/
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <dht.h>


// Timer variables
unsigned long lastTime = 0;  
unsigned long lastTimeTemperature = 0;
unsigned long lastTimeAcc = 0;
unsigned long gyroDelay = 10;
unsigned long temperatureDelay = 1000;
unsigned long accelerometerDelay = 200;

// Create a sensor object
Adafruit_MPU6050 mpu;

sensors_event_t a, g, temp;

float gyroX, gyroY, gyroZ;
float accX, accY, accZ;
float temperature;

//Gyroscope sensor deviation
float gyroXerror = 0.07;
float gyroYerror = 0.03;
float gyroZerror = 0.01;


//SENSOR DHT INISIALISASI
#include <dht.h>
#define DATA_PIN 4 // Definisi Pin untuk DHT22
dht DHT; // Buat DHT object


//SENSOR SOIL
#define sensorPin A0


//SENSOR RAINDROP
int air = A1;
const int bawah = 0;
const int atas = 1024;


//KONEKSI NODEMCU dengan UNO
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
SoftwareSerial mm (3, 2);

// Init MPU6050
void initMPU(){
  while(true){
    if (!mpu.begin()) {
      Serial.println("Failed to find MPU6050 chip");
    }
    break;
  }
  
  Serial.println("MPU6050 Found!");
}


String giro(){
  mpu.getEvent(&a, &g, &temp);

  
  float gyroX_temp = g.gyro.x;
  if(abs(gyroX_temp) > gyroXerror)  {
    gyroX += gyroX_temp/50.00;
  }
  
  float gyroY_temp = g.gyro.y;
  if(abs(gyroY_temp) > gyroYerror) {
    gyroY += gyroY_temp/70.00;
  }

  float gyroZ_temp = g.gyro.z;
  if(abs(gyroZ_temp) > gyroZerror) {
    gyroZ += gyroZ_temp/90.00;
  }

  String total = "X : "+String(gyroX)+" | Y : "+String(gyroY)+" | Z : "+String(gyroZ);
  return String(gyroX)+" "+String(gyroY)+" "+String(gyroZ);
}

String acc() {
  mpu.getEvent(&a, &g, &temp);
  accX = a.acceleration.x;
  accY = a.acceleration.y;
  accZ = a.acceleration.z;
  int pitch = -(atan2(accX, sqrt(accY*accY + accZ*accZ))*180.0)/M_PI;
  String total = "X : "+String(accX)+" | Y : "+String(accY)+" | Z : "+String(accZ);
  //Serial.println(total);
  return String(accX)+" "+String(accY)+" "+String(accZ);
}

String getTemperature(){
  mpu.getEvent(&a, &g, &temp);
  temperature = temp.temperature;
  return String(temperature);
}

void setup() {
  Serial.begin(115200);
  mm.begin(115200);
  initMPU();
}

String read_humidity(){
  int readData = DHT.read22(DATA_PIN); // baca Data dari sensor
  float h = DHT.humidity; // Ambil nilai Kelembaban
  return String(h);
}

String read_temperature(){
  int readData = DHT.read22(DATA_PIN); // baca Data dari sensor
  float t = DHT.temperature; // Ambil nilai Suhu  
  String complete = String(t);
  return complete;
}


String read_soil(){						
	int val = analogRead(sensorPin);	
	return String(val);
}


String read_raindrop(){
  int data_air = analogRead(air);
  int range = map(data_air, bawah, atas, 0, 3);
  return (String(data_air));
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;
 
  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  } 
 
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void loop() {  
  if ((millis() - lastTime) > gyroDelay) {
    String dht22_ = read_temperature();
    String humidity = read_humidity();
    String soil_ = read_soil();
    String raindrop_ = read_raindrop();
    String output = "[+] Temp : "+dht22_+"|Humidity: "+humidity+"|Raindrop: "+raindrop_+"|Soil : "+soil_;
    String ax = getValue(acc(), ' ', 0);
    String ay = getValue(acc(), ' ', 1);
    String az = getValue(acc(), ' ', 2);
    String gx = getValue(giro(), ' ', 0);
    String gy = getValue(giro(), ' ', 1);
    String gz = getValue(giro(), ' ', 2);
    String accelerator=  "[+] AX : "+ax+"|AY : "+ay+"|AZ : "+az;
    String gyroscope = "[+] Gx : "+gx+"|GY : "+gy+"|GZ : "+gz;


    Serial.println(output);
    Serial.println(accelerator);
    Serial.println(gyroscope);
    lastTime = millis();
    String kontinental = dht22_+" "+humidity+" "+raindrop_+" "+soil_+" "+acc()+" "+giro();
    kontinental.trim();
    Serial.println("[+] "+kontinental);
    Serial.println("");
    mm.println(kontinental);
    
  }
  delay(1000);

}

