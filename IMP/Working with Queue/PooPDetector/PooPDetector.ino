#include <SoftwareSerial.h>
/* RX and TX of Arduino to TX RX of ESP8266*/ 
#define RX 10
#define TX 11

/* Wifi Address and Details*/
/*---------------------------------*/
String AP = "Aeres";       
String PASS = "FuCky0u@$$#0le";
/*---------------------------------*/

int countTrueCommand;
int countTimeCommand; 
/* Server Setups, Server is in flask yay! */

/*---------------------------------*/
String HOST = "demo.localxpose.io";
String PORT = "14282";
/*---------------------------------*/

/* Analog PINS */
/*-----------------*/
int VOCSensor = A0;
int LDR = A1;
/*-----------------*/

int circ = 5;
int heat = 6;
int circheat = 9;
boolean found = false; 
float VOC, CO, Temp, Sound;

SoftwareSerial esp8266(RX,TX); //Establishes the Serial Connection

void setup(){
  Serial.begin(9600);
  esp8266.begin(115200);
  pinMode(LDR, INPUT);
  /* Wifi Setup */
  sendCommand("AT",5,"OK");
  sendCommand("AT+CWMODE=1",5,"OK");
  sendCommand("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"",20,"OK");
}
void loop(){
  GetVOC();
  Serial.println(VOC);
  delay(1000);
  int LDRValue = analogRead(LDR);
  Serial.print(" Light sensor = ");
  Serial.print(LDRValue);

  /* Server Query */
  String getData = "GET /update?valGas=";
  getData += String(VOC);
  getData +="&valLDR=";
  getData += String(LDRValue);
  getData += "\r\n\r\n";

  /*--------------------------------*/
  
  sendCommand("AT+CIPMUX=1",5,"OK");
  sendCommand("AT+CIPSTART=0,\"TCP\",\""+ HOST +"\","+ PORT,15,"OK");
  esp8266.println("AT+CIPSEND=0,100");
  //esp8266.println(getData);
  delay(1500);
  countTrueCommand++;
  sendCommand(getData,5,"OK");
  
  if (LDRValue <=700){
  delay(500);
  Serial.println("It's Dark Inside;");
  }
  else{
  delay(500);
  Serial.println("It's Bright Inside;");
  }
}

void GetVOC(){
 digitalWrite(circheat, HIGH);
 float val0 = analogRead(VOCSensor);
 VOC = map(val0, 0, 1023, 0, 100); //in %
}

float getVoltage(int pin){
  return (analogRead(pin)*(5.0/1023.0));
}

float map(float x, float in_min, float in_max, float out_min, float out_max){
 return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
void sendCommand(String command, int maxTime, char readReplay[]){
  Serial.print(countTrueCommand);
  Serial.print(": at command => ");
  Serial.print(command);
  Serial.print(" ");
  
  while(countTimeCommand < (maxTime*1)){
    esp8266.println(command);                //at+cipsend
     if(esp8266.find(readReplay)){
      found = true;
      break;
     }
    countTimeCommand++;
  }
  if(found == true){
    Serial.println("OYI");
    countTrueCommand++;
    countTimeCommand = 0;
  }
  if(found == false){
    Serial.println("Fail");
    countTrueCommand = 0;
    countTimeCommand = 0;
  }
  found = false;
 }
