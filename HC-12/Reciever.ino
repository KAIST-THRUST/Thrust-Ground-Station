#include <SoftwareSerial.h>
SoftwareSerial HC12(10,11);

void setup(){
    Serial.begin(9600);
    HC12.begin(9600);
    delay(2000);
    Serial.println("HC12 Start\n");
}

int c = 0;

void loop(){
    // while (Serial.available()){
    //     HC12.println(Serial.read());
    // }
    float sensorData1 = 0;
    float sensorData2 = 0;
    float sensorData3 = 0;
    float sensorData4 = 0;
    while(HC12.available()){
        sensorData1 = HC12.parseInt();   
        sensorData2 = HC12.parseInt(); 
        sensorData3 = HC12.parseInt();
        sensorData4 = HC12.parseInt();

        Serial.print(sensorData1 / 1000);
        Serial.print(",");
        Serial.print(sensorData2 / 1000);
        Serial.print(",");       
        Serial.print(sensorData3 / 1000);  
        Serial.print(",");       
        Serial.println(sensorData4 / 1000);  
        Serial.flush();
    }
    delay(160);
}