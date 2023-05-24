int ENA = D2;
int IN1 = D3;
int IN2 = D4;

void setup() {
  Serial.begin(115200); 
  Serial.println("Setup");
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT); 
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void loop() {
  setDirection();
  delay(1000);
  changeSpeed();
  delay(1000);
}

void setDirection() {
  Serial.println("Set Direction!");
  analogWrite(ENA, 255);

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  delay(5000);
  
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  delay(5000);
  
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void changeSpeed() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  
  for (int i = 0; i < 256; i++) {
    analogWrite(ENA, i);
    delay(20);
    Serial.println("<");
  }
  
  for (int i = 255; i >= 0; --i) {
    analogWrite(ENA, i);
    delay(20);
    Serial.println(">");
  }
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}