#include <SoftwareSerial.h>
/* RX and TX of Arduino to TX RX of ESP8266*/ 
#define RX 10
#define TX 11
// for person counter
#define trigPin1 4
#define echoPin1 2
#define trigPin2 5
#define echoPin2 3
//For the Relay
#define RELAY1  7        
/* Wifi Address and Details*/
/*---------------------------------*/
String AP = "Shankar";       
String PASS = "dob2802skv";
/*---------------------------------*/

int countTrueCommand;
int countTimeCommand; 
/* Server Setups, Server is in flask yay! */

/*---------------------------------*/
String HOST = "192.168.1.102";
String PORT = "5000";
/*---------------------------------*/

/* Analog PINS */
/*-----------------*/
int VOCSensor = A0;
int LDR = A1;
/*-----------------*/

int circ = 5;
int heat = 10000;
int circheat = 9;
boolean found = false; 
float VOC, CO, Temp, Sound;

//for ultrasonic sensor 
int counter = 0;
int lf = 0;
int rf = 0;
int LDRValue;
long duration, distance, RightSensor,LeftSensor;
float distance1,distance2;
int peopleinside=0;

unsigned long startMillis,currentMillis;
SoftwareSerial esp8266(RX,TX); //Establishes the Serial Connection

void setup(){
  Serial.begin(9600);
  esp8266.begin(115200);
  pinMode(LDR, INPUT);
  /* Wifi Setup */
  //sendCommand("AT",25,"OK");
  //sendCommand("AT+CWMODE=1",25,"OK");
  //sendCommand("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"",20,"OK"); 
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  startMillis = millis();
  Serial.print("SM:");
  pinMode(RELAY1, OUTPUT); 
  Serial.println(startMillis);
}
void loop(){
  GetVOC();
  GetPC();
  LDRValue = GetLDR();
  SendData();
}
void SendData(){
  currentMillis = millis();
  Serial.print("CM:");
  Serial.println(currentMillis);
  if( currentMillis-startMillis >= 300000){
  /* Server Query */
  String getData = "GET /update?valGas=";
  getData += String(VOC);
  getData +="&valLDR=";
  getData += String(LDRValue);
  getData +="&valPC=";
  getData +=String(counter);
  getData += "\r\n\r\n";
  /*--------------------------------*/
  sendCommand("AT+CIPMUX=1",5,"OK");
  sendCommand("AT+CIPSTART=0,\"TCP\",\""+ HOST +"\","+ PORT,15,"OK");
  esp8266.println("AT+CIPSEND=0,120"); 
  countTrueCommand++;
  sendCommand(getData,5,"OK");
 
  Serial.println(getData);
  startMillis = currentMillis;
  }
}
int GetLDR(){
  int LDRValue = analogRead(LDR);
  Serial.print(" Light sensor = ");
  Serial.print(LDRValue);  
  if (LDRValue <=700){
  digitalWrite(RELAY1,1);          // Turns Relay Off
  Serial.println("Light OFF");
  Serial.println("It's Bright Inside;");
  }
  else{
  Serial.println("It's Dark Inside;");
  digitalWrite(RELAY1,0);           // Turns ON Relays 1
  Serial.println("Light ON");
  }
  return LDRValue;
}
void GetVOC(){
 digitalWrite(circheat, HIGH);
 float val0 = analogRead(VOCSensor);
 VOC = map(val0, 0, 1023, 0, 100);
 Serial.println(VOC);//in %
}
void GetPC(){
  distance1 = SonarSensor(trigPin1, echoPin1);
  distance2 = SonarSensor(trigPin2, echoPin2);
  if(distance1<70){
  rf=1;
  rfout();
  }
  if(distance2<70){
  lf=1;
  lfin();
  }  
}
void lfin(){ 
  delay(250);
  distance1=SonarSensor(trigPin1, echoPin1);
  if(distance1<70){
  rf=1;
  }
  else
  {
    GetPC();
  }
  if((lf==1)&&(rf==1 )){
  counter=counter+1;
  Serial.println("left number of people visited");
  Serial.println(counter);
  Serial.println("number of people inside");
  peopleinside=peopleinside+1;
  Serial.println(peopleinside);
  lf=0;
  rf=0;
  GetPC();
}
}
void rfout(){
delay(250);
distance2 = SonarSensor(trigPin2, echoPin2);
  if(distance2<70){
  lf=1;
  }
  else
  {
    GetPC();
  }
  if(lf==1 && rf==1 )
  {
   counter=counter+1;
   Serial.println("Person counter:");
   Serial.println(counter);  
   lf=0;
   rf=0;
   Serial.println("number of people inside");
   peopleinside=peopleinside-1;
   Serial.println(peopleinside);
   GetPC();
  }
}
float getVoltage(int pin){
  return (analogRead(pin)*(5.0/1023.0));
}
float map(float x, float in_min, float in_max, float out_min, float out_max){
 return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
float SonarSensor(int trigPin,int echoPin){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = (duration/2) / 29.1;
    Serial.println(distance);
    return distance;
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
