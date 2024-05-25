#include <SoftwareSerial.h>
#include <Wire.h>
SoftwareSerial HC12(10,11);

void setup(){
    Serial.begin(9600);
    HC12.begin(9600);
    delay(2000);
    Serial.println("HC12 Start\n");
}

int c = 0;
const char delimiter = ',';
int boundLow;
int boundHigh;
int boundLow2;
int boundHigh2;
float sensorData1 = 0;
float sensorData2 = 0;
float sensorData3 = 0;
float sensorData4 = 0;

void loop(){
    // while (Serial.available()){
    //     HC12.println(Serial.read());
    // }
    //Serial.println("HC12.available");

    while(HC12.available()){
      String input = HC12.readStringUntil('\n');


      //Serial.println(input);

      boundLow = input.indexOf(delimiter);
      //Serial.println(boundLow);
      sensorData1 = (input.substring(0,boundLow).toFloat()/1000);

      boundHigh = input.indexOf(delimiter,boundLow+1);
      sensorData2 = (input.substring(boundLow+1,boundHigh).toFloat()/1000);

      boundLow2 = input.indexOf(delimiter,boundHigh+1);
      sensorData3 = (input.substring(boundHigh+1,boundLow2).toFloat()/1000);

      boundHigh2 = input.indexOf(delimiter,boundLow2+1);
      sensorData4 = (input.substring(boundLow2+1,boundHigh2).toFloat()/1000);



      Serial.print(sensorData1);
      Serial.print(",");
      Serial.print(sensorData2);
      Serial.print(",");
      Serial.print(sensorData3);
      Serial.print(",");
      Serial.println(sensorData4);


    }
    delay(160);
}