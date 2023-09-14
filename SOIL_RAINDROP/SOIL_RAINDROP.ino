//SENSOR RAINDROP
int air = A1;
const int bawah = 0;
const int atas = 1024;

//SENSOR SOIL
#define sensorPin A0


void setup(){
  pinMode(air,INPUT);
  Serial.begin(9600);
}


int read_raindrop(){
  int data_air = analogRead(air);
  int range = map(data_air, bawah, atas, 0, 3);
  return (data_air);
}

int read_soil(){						
	int val = analogRead(sensorPin);	
	return (val);
}

void loop(){
  int soil_ = read_soil();
  int raindrop_ = read_raindrop();
  String complete = (soil_+"|"+raindrop_);
  delay(1000);
  Serial.println(raindrop_);

}
