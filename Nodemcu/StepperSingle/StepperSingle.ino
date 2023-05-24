#include <Stepper.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor
/*
D1 -> N1
D2 -> N2
D3 -> N3
D4 -> N4

Red -> OUT3
Black -> OUT4

Green -> OUT1
Blue -> OUT2
https://docs.arduino.cc/learn/electronics/stepper-motors#stepperonerevolution
*/
// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, D1, D2, D3, D4);

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(400);
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  // step one revolution  in one direction:
  for(int i=0; i<10; i++){
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  }

  delay(500);

  // step one revolution in the other direction:
  Serial.println("counterclockwise");
  myStepper.step(-stepsPerRevolution);
  delay(500);
}