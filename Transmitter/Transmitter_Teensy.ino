#include <Wire.h> //libs
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
#include <stdlib.h>
//#include <Servo.h>

//Adafruit_BMP280 bmp; //Puts BMP280 into I2C communication
//Adafruit_Sensor *bmp_temp = bmp.getTemperatureSensor(); //gets temp
//Adafruit_Sensor *bmp_pressure = bmp.getPressureSensor(); //gets pressure
#define HC12 Serial2
Adafruit_BNO055 bno = Adafruit_BNO055(28); //defines bno as the BNO055 sensor

void createDataString(String& data, float x, float y, float z, float w){
  int sensor1 = x * 1000;
  int sensor2 = y * 1000;
  int sensor3 = z * 1000;
  int sensor4 = w * 1000;
  data = "*" + String(sensor1) + "*" + String(sensor2) + "*" + String(sensor3) + "*" + String(sensor4); 
}

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600); //attempt to establish a serial connection
  HC12.begin(9600);
  if(!bno.begin()){ //attempts to establish connection with BNO055 on 0x28
    Serial.println("fk");
  }else{
    Serial.println("BNO055 SUCESSFULL CONNECTION");
  }

}


void loop() {
  // put your main code here, to run repeatedly:
  
  
  imu::Quaternion quat = bno.getQuat();
  Serial.print("quat : ");
  Serial.print("x:");
  Serial.print(quat.x(), 3);
  Serial.print(" ");
  Serial.print("y:");
  Serial.print(quat.y(), 3);
  Serial.print(" ");
  Serial.print("z:");
  Serial.print(quat.z(), 3);
  Serial.print(" ");
  Serial.print("w:");
  Serial.print(quat.w(), 3);
  Serial.println(" ");
  String val = "";
  createDataString(val, quat.x(),quat.y(), quat.z(), quat.w());
  
  Serial.print("HC12 Valid : ");
  Serial.println(val);
  HC12.print(int(quat.x()*1000));//sends the variables
  HC12.print(",");
  HC12.print(int(quat.y()*1000));
  HC12.print(",");
  HC12.print(int(quat.z()*1000));//if you just need to send 2 variables,simply change this value and the following to 0
  HC12.print(",");
  HC12.print(int(quat.w()*1000));
  HC12.println("");
  
  delay(160);

}