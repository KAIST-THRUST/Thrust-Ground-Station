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
        Serial.println(HC12.read());
    }
    delay(1000);
}