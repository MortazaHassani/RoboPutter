#include <Servo.h>
#include <ESP8266WiFi.h> 
#include "Adafruit_MQTT.h" 
#include "Adafruit_MQTT_Client.h" 
/************************* WiFi Access Point *********************************/ 
#define WLAN_SSID       "Board_Wlan" 
#define WLAN_PASS       "Board_Wlan**$7" 
#define MQTT_SERVER      "192.168.137.4" // static ip address
#define MQTT_PORT         1883                    
#define MQTT_USERNAME    "golf" 
#define MQTT_PASSWORD         "golf123" 
/************************* Pins Configuration *********************************/ 
Servo myservo;
int servo = D2;
int ENA = 14;
int IN1 = 12;
int IN2 = 13;
int IN3 = 0;
int IN4 = 2;
int ENB = 15;
int LED = D0;
/************************* Environment Constants *********************************/ 
int carSpeed = 150;
int multiP = 10;
uint32_t x=0; 
/************ Global State ******************/ 
// Create an ESP8266 WiFiClient class to connect to the MQTT server. 
WiFiClient client; 
// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details. 
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD); 
/****************************** Feeds ***************************************/ 
// Setup a feed called 'pi_con' for publishing. 
// Notice MQTT paths for AIO follow the form: <username>/feeds/<feedname> 
Adafruit_MQTT_Publish pi_con = Adafruit_MQTT_Publish(&mqtt, MQTT_USERNAME "/pi"); 
// Setup a feed called 'esp8266_con' for subscribing to changes. 
Adafruit_MQTT_Subscribe esp8266_con = Adafruit_MQTT_Subscribe(&mqtt, MQTT_USERNAME "/esp8266"); 
/*************************** Sketch Code ************************************/ 
void MotorFunc(){
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT); 
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT); 
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void setup() {
  Serial.begin(115200); 
  Serial.println("ESP8266 ON");
  pinMode(LED, OUTPUT);
  myservo.attach(servo, 500, 2500);
  MotorFunc();
  delay(30);
   Serial.println(F("RPi-ESP-MQTT")); 
 // Connect to WiFi access point. 
 Serial.println(); Serial.println(); 
 Serial.print("Connecting to "); 
 Serial.println(WLAN_SSID); 
 WiFi.begin(WLAN_SSID, WLAN_PASS); 
 while (WiFi.status() != WL_CONNECTED) { 
   delay(500); 
   Serial.print("."); 
 } 
 Serial.println(); 
 Serial.println("WiFi connected"); 
 Serial.println("IP address: "); Serial.println(WiFi.localIP()); 
 // Setup MQTT subscription for esp8266_led feed. 
 mqtt.subscribe(&esp8266_con); 
}

void loop() {
  // Ensure the connection to the MQTT server is alive (this will make the first 
  // connection and automatically reconnect when disconnected).  See the MQTT_connect 
  MQTT_connect(); 
  // this is our 'wait for incoming subscription packets' busy subloop 
  // try to spend your time here 
  // Here its read the subscription 
  Adafruit_MQTT_Subscribe *subscription; 
  while (subscription = mqtt.readSubscription()) {
    if (subscription == &esp8266_con) { 
      char *message = (char *)esp8266_con.lastread; 
      String message_str(message);
      Serial.print(F("Got: ")); 
      Serial.println(message_str);
      message_str.trim();                        // remove any \r \n whitespace at the end of the String
      int space_index = message_str.indexOf(' ');
      String teststr = message_str.substring(0, space_index);
      String time_str = message_str.substring(space_index + 1);
      float time_sec = time_str.toFloat();
      if (teststr == "forward") {
        Serial.println("forward");
        forward(time_sec);
      } 
      else if(teststr == "backward"){
        Serial.println("backward");
        backward(time_sec);
      }
      else if(teststr == "left"){
        left(time_sec);

      }
      else if(teststr == "right"){
        right(time_sec);
      }
      else if(teststr == "kick"){
        kick(time_sec);
      }
      else {
        stop();
      }
    }
  }
}


// Function to connect and reconnect as necessary to the MQTT server. 
void MQTT_connect() { 
 int8_t ret; 
 // Stop if already connected. 
 if (mqtt.connected()) { 
  //  digitalWrite(LED_PIN, HIGH); 
   return; 
 } 

 Serial.print("Connecting to MQTT... "); 
 uint8_t retries = 3; 
 while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected 
      Serial.println(mqtt.connectErrorString(ret)); 
      Serial.println("Retrying MQTT connection in 5 seconds..."); 
      mqtt.disconnect(); 
      digitalWrite(LED, LOW); 
      delay(3000);  // wait 3 seconds 
      retries--; 
      if (retries == 0) { 
        // basically die and wait for WDT to reset me 
        while (1); 
      } 
 } 
 if ((ret = mqtt.connect()) == 0){
 Serial.println("MQTT Connected!");
 digitalWrite(LED, HIGH); 
 } 
} 


void kick(float time_sec){
  int pos = time_sec;
  Serial.println("Kick");
  myservo.write(pos);
  delay(2000);
}

void forward(float time_sec){
  Serial.println("Going forward");
  unsigned long start_time = millis();
  while((millis() - start_time) < (time_sec * multiP)){
  analogWrite(ENA, carSpeed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  analogWrite(ENB, carSpeed);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  }
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void backward(float time_sec){
  Serial.println("Going backward");
  unsigned long start_time = millis();
  while((millis() - start_time) < (time_sec * multiP)){
  analogWrite(ENA, carSpeed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  analogWrite(ENB, carSpeed);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  }
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void stop(){
  Serial.println("stop");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
void left(float time_sec){
  Serial.println("Turning left");
  unsigned long start_time = millis();
  while((millis() - start_time) < (time_sec * multiP)){
  analogWrite(ENA, carSpeed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  analogWrite(ENB, carSpeed); // Stop the right motor
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  }
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void right(float time_sec){
  Serial.println("Turning right");
  unsigned long start_time = millis();
  while((millis() - start_time) < (time_sec * multiP)){
  analogWrite(ENA, carSpeed); // Stop the left motor
  digitalWrite(IN1, HIGH); // LOW 2
  digitalWrite(IN2, LOW); //HIGH 1

  analogWrite(ENB, carSpeed);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  }
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}