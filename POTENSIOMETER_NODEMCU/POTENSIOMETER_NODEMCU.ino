int sensor = A0;
int nilai;


void setup(){
  Serial.begin(9600);
}

void loop(){
  nilai = analogRead(sensor);
  Serial.print("Sensor: ");
  Serial.println(nilai);
  delay(1000);
}