#include <Wire.h> //libs
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
#include <stdlib.h>
//#include <Servo.h>
#include <SD.h>
#include <SPI.h>

//Adafruit_BMP280 bmp; //Puts BMP280 into I2C communication
//Adafruit_Sensor *bmp_temp = bmp.getTemperatureSensor(); //gets temp
//Adafruit_Sensor *bmp_pressure = bmp.getPressureSensor(); //gets pressure
#define HC12 Serial2
Adafruit_BNO055 bno = Adafruit_BNO055(28); //defines bno as the BNO055 sensor

File myFile;

// change this to match your SD shield or module;
// Arduino Ethernet shield: pin 4
// Adafruit SD shields and modules: pin 10
// Sparkfun SD shield: pin 8
// Teensy audio board: pin 10
// Teensy 3.5 & 3.6 & 4.1 on-board: BUILTIN_SDCARD
// Wiz820+SD board: pin 4
// Teensy 2.0: pin 0
// Teensy++ 2.0: pin 20
const int chipSelect = BUILTIN_SDCARD;

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

  Serial.print("Initializing SD card...");

  if (!SD.begin(chipSelect)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");

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
  
  //Serial.print("HC12 Valid : ");
  //Serial.println(val);
  //HC12.wirte(int(quat.x()*1000));
  //HC12.print(int(quat.x()*1000));
  //HC12.print(int(quat.y()*1000));
  //HC12.print(int(quat.z()*1000));
  //HC12.print(int(quat.w()*1000));
  HC12.print(int(quat.x()*1000));//sends the variables
  HC12.print(",");
  HC12.print(int(quat.y()*1000));
  HC12.print(",");
  HC12.print(int(quat.z()*1000));//if you just need to send 2 variables,simply change this value and the following to 0
  HC12.print(",");
  HC12.print(int(quat.w()*1000));
  HC12.println("");
  unsigned long start_time = millis();
  myFile = SD.open("teensy.txt", FILE_WRITE);
  
  // if the file opened okay, write to it:
  if (myFile) {

    myFile.print("x:");
    myFile.print(quat.x(), 3);
    myFile.print(" ");
    myFile.print("y:");
    myFile.print(quat.y(), 3);
    myFile.print(" ");
    myFile.print("z:");
    myFile.print(quat.z(), 3);
    myFile.print(" ");
    myFile.print("w:");
    myFile.print(quat.w(), 3);
    myFile.println(" ");

    myFile.close();
    unsigned long end_time = millis();
    Serial.print("start : ");
    Serial.print(start_time);
    Serial.print("end time : ");
    Serial.print(end_time);
    Serial.print("total : ");
    Serial.println(end_time - start_time);
    //Serial.println("done.");
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
  }
  
  delay(160);

}