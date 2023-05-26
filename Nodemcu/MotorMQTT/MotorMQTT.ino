
#include <ESP8266WiFi.h> 
#include "Adafruit_MQTT.h" 
#include "Adafruit_MQTT_Client.h" 
/************************* WiFi Access Point *********************************/ 
#define WLAN_SSID       "Board_Wlan" 
#define WLAN_PASS       "Board_Wlan**$7" 
#define MQTT_SERVER      "192.168.137.212" // static ip address
#define MQTT_PORT         1883                    
#define MQTT_USERNAME    "golf" 
#define MQTT_PASSWORD         "golf123" 
#define LED_PIN     D1                // Pin connected to the LED. GPIO 2 (D4) 
#define BUTTON_PIN  D2               // Pin connected to the button. GPIO 15 (D8) 
int ENA = 14;
int IN1 = 12;
int IN2 = 13;
int IN3 = 0;
int IN4 = 2;
int ENB = 15;

/************ Global State ******************/ 
// Create an ESP8266 WiFiClient class to connect to the MQTT server. 
WiFiClient client; 
// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details. 
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD); 
/****************************** Feeds ***************************************/ 
// Setup a feed called 'pi_led' for publishing. 
// Notice MQTT paths for AIO follow the form: <username>/feeds/<feedname> 
Adafruit_MQTT_Publish pi_led = Adafruit_MQTT_Publish(&mqtt, MQTT_USERNAME "/leds/pi"); 
// Setup a feed called 'esp8266_led' for subscribing to changes. 
Adafruit_MQTT_Subscribe esp8266_led = Adafruit_MQTT_Subscribe(&mqtt, MQTT_USERNAME "/leds/esp8266"); 
/*************************** Sketch Code ************************************/ 



void MQTT_connect(); 
void setup() { 
 Serial.begin(115200); 
 delay(10); 
 MotorFunc();
 pinMode(LED_PIN, OUTPUT); 
 digitalWrite(LED_PIN, LOW); 
 // Setup button as an input with internal pull-up. 
pinMode(BUTTON_PIN, INPUT_PULLUP); 
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
 mqtt.subscribe(&esp8266_led); 
} 
uint32_t x=0; 
void loop() { 
  // Check if the button has been pressed by looking for a change from high to 
 // low signal (with a small delay to debounce). 
 int button_first = digitalRead(BUTTON_PIN); 
 // Ensure the connection to the MQTT server is alive (this will make the first 
 // connection and automatically reconnect when disconnected).  See the MQTT_connect 
 MQTT_connect(); 
 // this is our 'wait for incoming subscription packets' busy subloop 
 // try to spend your time here 
 // Here its read the subscription 
 Adafruit_MQTT_Subscribe *subscription; 
 while (subscription = mqtt.readSubscription()) { 
   if (subscription == &esp8266_led) { 
     char *message = (char *)esp8266_led.lastread; 
     Serial.print(F("Got: ")); 
     Serial.println(message); 
     if (strcmp(message, "forward") == 0) {
        forward(80);
      } else if (strcmp(message, "backward") == 0) {
        backward(80);
      } else if (strcmp(message, "stop") == 0) {
        stop();
      }
     /*
        // Check if the message was ON, OFF, or TOGGLE. 
     if (strncmp(message, "ON", 2) == 0) { 
       // Turn the LED on. 
       digitalWrite(LED_PIN, HIGH); 
     } 
     else if (strncmp(message, "OFF", 3) == 0) { 
       // Turn the LED off. 
       digitalWrite(LED_PIN, LOW); 
     } 
     else if (strncmp(message, "TOGGLE", 6) == 0) { 
       // Toggle the LED. 
       digitalWrite(LED_PIN, !digitalRead(LED_PIN)); 
      */

      } 

   } 
  

 //delay(20); 
 int button_second = digitalRead(BUTTON_PIN); 
 if ((button_first == HIGH) && (button_second == LOW)) { 
   // Button was pressed! 
   Serial.println("Button pressed!"); 
   pi_led.publish((char*)"TOGGLE"); 
 } 
} 

// Function to connect and reconnect as necessary to the MQTT server. 
void MQTT_connect() { 
 int8_t ret; 
 // Stop if already connected. 
 if (mqtt.connected()) { 
   digitalWrite(LED_PIN, HIGH); 
   return; 
 } 

 Serial.print("Connecting to MQTT... "); 
 uint8_t retries = 3; 
 while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected 
      Serial.println(mqtt.connectErrorString(ret)); 
      Serial.println("Retrying MQTT connection in 5 seconds..."); 
      mqtt.disconnect(); 
      digitalWrite(LED_PIN, LOW); 
      delay(3000);  // wait 3 seconds 
      retries--; 
      if (retries == 0) { 
        // basically die and wait for WDT to reset me 
        while (1); 
      } 
 } 
 if ((ret = mqtt.connect()) == 0){
 Serial.println("MQTT Connected!");
 digitalWrite(LED_PIN, HIGH); 
 } 
} 

// Here start L298N Motors Functions


void forward(int speed){
  Serial.println("Going forward");
  analogWrite(ENA, speed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  analogWrite(ENB, speed);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

}
void backward(int speed){
  Serial.println("Going backward");
  analogWrite(ENA, speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  analogWrite(ENB, speed);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

}
void stop(){
  Serial.println("stop");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
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
