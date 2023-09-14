
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>



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


void getGyroReadings(){
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
  Serial.println(total);
}

void getAccReadings() {
  mpu.getEvent(&a, &g, &temp);
  // Get current acceleration values
  accX = a.acceleration.x;
  accY = a.acceleration.y;
  accZ = a.acceleration.z;
  int pitch = -(atan2(accX, sqrt(accY*accY + accZ*accZ))*180.0)/M_PI;
  String total = "X : "+String(accX)+" | Y : "+String(accY)+" | Z : "+String(accZ);
  Serial.println(total);
}

String getTemperature(){
  mpu.getEvent(&a, &g, &temp);
  temperature = temp.temperature;
  return String(temperature);
}

void setup() {
  Serial.begin(9600);
  initMPU();
}

void loop() {
  
  if ((millis() - lastTime) > gyroDelay) {
    // Send Events to the Web Server with the Sensor Readings
    getAccReadings();
    getGyroReadings();
    lastTime = millis();
  }
  delay(1000);
  //getAccReadings();
  
}
