int air = A0;
const int bawah = 0;
const int atas = 1024;

void setup(){
  pinMode(air,INPUT);
  Serial.begin(9600);
}

void loop(){
  int data_air = analogRead(air);
  int range = map(data_air, bawah, atas, 0, 3);
  Serial.println(data_air);
  delay(500);
}