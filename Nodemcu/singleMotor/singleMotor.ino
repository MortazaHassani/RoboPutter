#include <Servo.h>

Servo myservo;
int servo = D2;
int ENA = 14;
int IN1 = 12;
int IN2 = 13;
int IN3 = 0;
int IN4 = 2;
int ENB = 15;

int carSpeed = 100;
int multiP = 10;

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
  Serial.println("Setup");
  myservo.attach(servo, 500, 2500);
  MotorFunc();
}

void loop() {

  Serial.println("Enter direction:");
  while (Serial.available() == 0) {}     //wait for data available
  String iteststr = Serial.readString();  //read until timeout
  iteststr.trim();                        // remove any \r \n whitespace at the end of the String
  int space_index = iteststr.indexOf(' ');
  String teststr = iteststr.substring(0, space_index);
  String time_str = iteststr.substring(space_index + 1);
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
  /*
  delay(1000);
  */
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