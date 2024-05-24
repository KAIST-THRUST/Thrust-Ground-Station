#include <SoftwareSerial.h>
SoftwareSerial HC12(2,3);

void setup(){
    Serial.begin(9600);
    HC12.begin(9600);
    Serial.println("HC12 Start\n");
}

int c = 0;

void loop(){
    while (Serial.available()){
        HC12.println(Serial.read());
    }

    while(HC12.available()){
        float sensorData1 = HC12.parseFloat();
        float sensorData2 = HC12.parseFloat();
        float sensorData3 = HC12.parseFloat();
        
        Serial.print(sensorData1);
        Serial.print(",");
        Serial.print(sensorData2);
        Serial.print(",");
        Serial.println(sensorData3);  
        //Serial.println(HC12.read());
    }
    delay(1000);
}
