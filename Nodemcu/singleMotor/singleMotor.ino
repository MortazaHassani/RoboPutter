int ENA = 14;
int IN1 = 12;
int IN2 = 13;
int IN3 = 0;
int IN4 = 2;
int ENB = 15;

void setup() {
  Serial.begin(115200); 
  Serial.println("Setup");
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

void loop() {

  Serial.println("Enter direction:");
  while (Serial.available() == 0) {}     //wait for data available
  String teststr = Serial.readString();  //read until timeout
  teststr.trim();                        // remove any \r \n whitespace at the end of the String
  if (teststr == "forward") {
    Serial.println("forward");
    forward();
  } 
  else if(teststr == "backward"){
    Serial.println("backward");
    backward();
  }
  else {
    stop();
  }
  /*
  setDirection();
  delay(1000);
  changeSpeed();
  delay(1000);
  */
}
void forward(){
  Serial.println("Going forward");
  analogWrite(ENA, 255);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  analogWrite(ENB, 255);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

}
void backward(){
  Serial.println("Going backward");
  analogWrite(ENA, 255);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  analogWrite(ENB, 255);
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