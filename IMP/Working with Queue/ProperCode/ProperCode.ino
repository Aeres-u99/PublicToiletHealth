#include <SoftwareSerial.h>

/* RX and TX of Arduino to TX RX of ESP8266*/ 
#define RX 10
#define TX 11

// for person counter
#define trigPin1 4
#define echoPin1 2
#define trigPin2 5
#define echoPin2 3
#define trigPin3 7
#define echoPin3 6

//For the Relay
#define RELAY1  8    
#define RELAY2  9    
  
/* Wifi Address and Details*/
/*---------------------------------*/
String AP = "M7";       
String PASS = "qwertyuipo";
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

//for ultrasonic sensor (person counter)
int counter = 0;
int counter1 = 0;
int lf = 0;
int rf = 0;
int LDRValue, WL;
long duration, distance, RightSensor,LeftSensor;
float distance1,distance2,distance3;
int peopleinside=0;

unsigned long startMillis,currentMillis,startMillis_2,currentMillis_2;
SoftwareSerial esp8266(RX,TX); //Establishes the Serial Connection

void setup(){
  Serial.begin(9600);
  esp8266.begin(115200);
  pinMode(LDR, INPUT);
  /* Wifi Setup */
  sendCommand("AT",25,"OK");
  sendCommand("AT+CWMODE=1",25,"OK");
  sendCommand("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"",20,"OK"); 
  
  /* Ultrasonic Setup */
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);
  
  startMillis = millis(); 
  pinMode(RELAY1, OUTPUT); 
  pinMode(RELAY2, OUTPUT); 
 
}

void loop()
{
  SendData();
  Do_Stuffs();
  GetPC();      // To get person counter values (Integrated with RELAY2 for switching ON exhaust fan)                                
}

void Do_Stuffs(){
  currentMillis_2 = millis();
  if( currentMillis_2-startMillis_2 >=10000){
     GetVOC();                      // To get gas sensor values     (Integrated with RELAY2 for switching ON exhaust fan)
     LDRValue = GetLDR();           // To get LDR values            (Integrated with RELAY1 for switching ON LED Light)
     GetWL();                       // To get Water level                      
  }
}

void SendData(){
  currentMillis = millis();
  if( currentMillis-startMillis >= 300000){
  /* Server Query */
  String getData = "GET /update?valGas=";
  getData += String(VOC);
  getData +="&valLDR=";
  getData += String(LDRValue);
  getData +="&valPC=";
  getData +=String(counter);
  getData +="&valWL=";
  getData +=String(WL);
  getData += "\r\n\r\n";
  /*--------------------------------*/
  sendCommand("AT+CIPMUX=1",5,"OK");
  sendCommand("AT+CIPSTART=0,\"TCP\",\""+ HOST +"\","+ PORT,15,"OK");
  esp8266.println("AT+CIPSEND=0,140"); 
  countTrueCommand++;
  sendCommand(getData,5,"OK");
  Serial.println(getData);
  startMillis = currentMillis;
  }
}

int GetLDR()
{
  int LDRValue = (analogRead(LDR)/10);
  Serial.print("--> Light Luminosity = ");
  Serial.println(LDRValue);  
  if ((LDRValue <=70) && (LDRValue >=30))
  {
  digitalWrite(RELAY1,1);          // Turns Relay Off
  Serial.println("--> Light OFF");
  Serial.println("Sufficient Light Inside;");
  }
  else if (LDRValue <=30)
  {
  digitalWrite(RELAY1,1);          // Turns Relay Off
  Serial.println("--> Light OFF");
  Serial.println("Enough Light Inside;");
  }
  else
  {
  digitalWrite(RELAY1,0);           // Turns ON Relay 1 (LED Light)
  Serial.println("--> Light ON");
  Serial.println("No Light Inside;");
  }
  return LDRValue;
}

void GetVOC() 
{
 digitalWrite(circheat, HIGH);
 float val0 = analogRead(VOCSensor);
 VOC = map(val0, 0, 1023, 0, 100);
 Serial.print("--> Gas Sensor Readinds :  ");
 Serial.println(VOC);
 
 if(VOC > 30)
 {
 digitalWrite(RELAY2,0);                               // Turns ON RELAY 2 (Exhaust Fan)
 Serial.println("--> Exhaust Fan is Turned ON ");
 }
 else if( VOC < 30 )
 {
 digitalWrite(RELAY2,1);                                  // Turns OFF RELAY 2 (Exhaust fan)
 Serial.println("--> Exhaust fan is turned OFF ");
 }
}

void GetPC()
{
  distance1 = SonarSensor(trigPin1, echoPin1);
  distance2 = SonarSensor(trigPin2, echoPin2);
  
  if(distance2<150){
  lf=1;
  lfin();
  } 
  
  else if(distance1<150){
  rf=1;
  rfout();
  }
   
}

void lfin()
{ 
  delay(250);
  distance1=SonarSensor(trigPin1, echoPin1);

  if(distance1<150){
  rf=1;
  }
  else
  {
    loop();
  }
  if((lf==1)&&(rf==1 ))
  {
  Serial.println("--> Out  ");
  Serial.print("Number of People Entered :  ");
  Serial.println(counter);
  
  counter1+=1;
  //Serial.print("Number of People Left :  ");
  //Serial.println(counter1);
 
  
  peopleinside=peopleinside-1;
  Serial.print("Number of people Inside :  ");
  Serial.println(peopleinside);
  Serial.println(" ");
  
  lf=0;
  rf=0;
 
   loop();
}
}

void rfout()
{
delay(250);
distance2 = SonarSensor(trigPin2, echoPin2);

  if(distance2<150){
  lf=1;
  }
  else
  {
    loop();
  }
  if(rf==1 && lf==1 )
  {
   Serial.println("--> In ");
   counter+=1;
   Serial.print("Number of People Entered :  ");
   Serial.println(counter);  
   //Serial.print("Number of People Left :  ");
   //Serial.println(counter1);
  

   peopleinside=peopleinside+1;
   Serial.print("Number of people Inside :  ");
   Serial.println(peopleinside);
   Serial.println(" ");

   lf=0;
   rf=0;

  
   
   loop();
  }
}

void GetWL() 
{
distance3=SonarSensor( trigPin3, echoPin3 );

 WL=100-distance3;
  if (WL <= 20){
  Serial.println("Water Level is Less than 20% ");
  }
  else if (WL <= 70){
  Serial.println("Water Level Adequate : 70%");
  }
  else if(WL <= 90){
  Serial.println("Water Level Full : 100%");
  }
}

float getVoltage(int pin){
  return (analogRead(pin)*(5.0/1023.0));
}

float map(float x, float in_min, float in_max, float out_min, float out_max){
 return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float SonarSensor(int trigPin,int echoPin)
{
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    pinMode(echoPin, INPUT);
    duration = pulseIn(echoPin, HIGH);
    distance = (duration/2) / 29.1;
   
    return distance;
}

void sendCommand(String command, int maxTime, char readReplay[])
{
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
