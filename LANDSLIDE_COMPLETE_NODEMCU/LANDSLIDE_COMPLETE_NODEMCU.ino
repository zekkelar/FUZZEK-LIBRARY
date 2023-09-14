#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>
SoftwareSerial mm (5, 4);


#define WIFI_SSID "STANLEY" 
#define WIFI_PASSWORD "zekkelganteng"

int sensor = A0;
int nilai;

WiFiClient client;
HTTPClient http;
ESP8266WiFiMulti WiFiMulti;


void setup(){
  Serial.println("Update");
  Serial.begin(115200);
  mm.begin(115200);
  connect_wifi();
}


void connect_wifi(){
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("Connected");

}
void loop(){
  nilai = analogRead(sensor);
  String sensorstring = mm.readStringUntil('\n');
  sensorstring.trim();
  Serial.println(sensorstring);
  Serial.println("TEST");
  String dht22 = getValue(sensorstring, ' ', 0);
  String humidity = getValue(sensorstring, ' ', 1);
  String raindrop = getValue(sensorstring, ' ', 2);
  String soil = getValue(sensorstring, ' ', 3);
  String gx = getValue(sensorstring, ' ', 4);
  String gy = getValue(sensorstring, ' ', 5);
  String gz = getValue(sensorstring, ' ', 6);
  String ax = getValue(sensorstring, ' ', 7);
  String ay = getValue(sensorstring, ' ', 8);
  String az = getValue(sensorstring, ' ', 9);
  
  if(ax.length()>1){
    String complete1 = "[+][GYRO] GX : "+ax+"| GY : "+ay+"| GZ : "+az;
    String complete2 = "[+][ACCE] AX : "+gx+"| AY : "+gy+"| AZ : "+gz;
    String complete3 = "[SOIL] "+soil;
    String complete4 = "[HUMIDITY] "+humidity;
    String complete5 = "[RAINDROP] "+raindrop;
    String complete6 = "[TEMP] "+dht22;
    String complete7 = "[POTENSIOMETER] "+String(nilai);
    Serial.println(complete1);
    Serial.println(complete2);
    Serial.println(complete3);
    Serial.println(complete4);
    Serial.println(complete5);
    Serial.println(complete6);   
    Serial.println(complete7);
    Serial.println("");
    upload(dht22, humidity, raindrop, String(nilai), soil, ax, ay, az, gx, gy, gz);
  }
  
  delay(300);
  
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

void upload(String dht_temp, String dht_hum, String raindrop, String potensiometer, String soil,
              String gx, String gy, String gz, String ax, String ay, String az)
{
  
  String url = "http://172.20.10.13:5000/fuzzy?id=add";
  String data = "&ch="+raindrop+"&s="+soil+"&g="+ay+"&t="+(dht_temp)+"&p="+potensiometer;
  String url_com = url+data;
  url_com.trim();
  Serial.println(url_com);
   
  if (WiFi.status()==WL_CONNECTED){

    if (http.begin(url_com)){
      int responsecode= http.GET();
      if (responsecode>0){
        String payload = http.getString(); 
        Serial.println("[+] Success 200");
        Serial.println("[+] "+payload);
      }
      else{
        String payload = http.getString(); 
        
        Serial.println("[+] Failed -1");
        Serial.println(payload);
      }

    }
    else {
        Serial.printf("[HTTPS] Unable to connect\n");
    }
  }
  else{
    Serial.println("WiFi Disconnected");
  }


  /*
  http.begin(client, path_raindrop.c_str());
  http.begin(client, path_potensiometer.c_str());
  http.begin(client, path_soil.c_str());
  http.begin(client, path_temperature.c_str());
  */
  
}