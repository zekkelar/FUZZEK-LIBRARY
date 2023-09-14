#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

#define WIFI_SSID "STANLEY" 
#define WIFI_PASSWORD "taikuda123"

WiFiClient client;
HTTPClient http;


void setup(){
  Serial.begin(9600);
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
  String url = "http://172.20.10.13:5000";
  if (WiFi.status()==WL_CONNECTED){
    if (http.begin(url.c_str())){
      int responsecode= http.GET();
      if (responsecode>0){
        Serial.println("[+] Success 200");
        String payload = http.getString();
        Serial.println(payload);
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
    Serial.printf("[WIFI] Unable to connect\n");
  }
  delay(1000);
}