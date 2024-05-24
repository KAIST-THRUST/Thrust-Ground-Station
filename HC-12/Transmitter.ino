#include "DFRobot_BNO055/DFRobot_BNO055.cpp"
#include "Wire.h"
#include <SoftwareSerial.h>
#include <stdlib.h>

SoftwareSerial HC12(3, 4);

typedef DFRobot_BNO055_IIC    BNO;    // ******** use abbreviations instead of full names ********

BNO   bno(&Wire, 0x28);    // input TwoWire interface and IIC address

void createDataString(char* value, float yaw, float pitch, float roll, float w){
  int sensor1 = yaw * 1000;
  int sensor2 = pitch * 1000;
  int sensor3 = roll * 1000;
  int sensor4 = w * 1000;
  char sensorbuf1[5];
  char sensorbuf2[5];
  char sensorbuf3[5];
  char sensorbuf4[5];
  itoa(sensor1, sensorbuf1, 10);
  itoa(sensor2, sensorbuf2, 10);
  itoa(sensor3, sensorbuf3, 10);
  itoa(sensor4, sensorbuf4, 10);
  //char strdata[1];
  char strdata[1];
  strdata[0] = '*';
  strcat(strdata,sensorbuf1);
  strcat(strdata,"*");
  strcat(strdata,sensorbuf2);
  strcat(strdata,"*");
  strcat(strdata,sensorbuf3);
  strcat(strdata,"*");
  strcat(strdata,sensorbuf4);
  strcpy(value,strdata);

  //data = "*" + String(sensor1) + "*" + String(sensor2) + "*" + String(sensor3) + "*" + String(sensor4); 
}

// show last sensor operate status
void printLastOperateStatus(BNO::eStatus_t eStatus)
{
  switch(eStatus) {
  case BNO::eStatusOK:    Serial.println("everything ok"); break;
  case BNO::eStatusErr:   Serial.println("unknow error"); break;
  case BNO::eStatusErrDeviceNotDetect:    Serial.println("device not detected"); break;
  case BNO::eStatusErrDeviceReadyTimeOut: Serial.println("device ready time out"); break;
  case BNO::eStatusErrDeviceStatus:       Serial.println("device internal status error"); break;
  default: Serial.println("unknow status"); break;
  }
}

void setup()
{
  Serial.begin(9600);
  bno.reset();
  while(bno.begin() != BNO::eStatusOK) {
    Serial.println("bno begin faild");
    printLastOperateStatus(bno.lastOperateStatus);
    delay(2000);
  }
  HC12.begin(9600);
  Serial.println("bno begin success");
}

String val = "";

void loop()
{
  BNO::sQuaAnalog_t   sQua;
  sQua = bno.getQua();
  
  Serial.print("x:");
  Serial.print(sQua.x, 3);
  Serial.print(" ");
  Serial.print("y:");
  Serial.print(sQua.y, 3);
  Serial.print(" ");
  Serial.print("z:");
  Serial.print(sQua.z, 3);
  Serial.println(" ");
  
  char value[40];
  createDataString(value, sQua.x,sQua.y,sQua.z,sQua.w);
  
  Serial.println(value);
  
  //Serial.println(val);
  HC12.print(value);
  //HC12.flush();
  val = "";
  //Serial.flush();
  delay(160);
}