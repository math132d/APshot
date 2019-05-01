#include <SharpIR.h>

#define IN A14
#define FILTERED_IN A15
#define IR A13 // define IR signal pin
#define model 1080 // used 1080 because model GP2Y0A21YK0F is used

//Filter used was 400K ohm (4x100k in series), 104pF
//We might want to consider using a potentiometer in the setup, so we can adjust it more granuarily

SharpIR SharpIR(IR, model);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long startTime = millis(); // takes the time before the loop on the library begins
  int dis = SharpIR.distance();  // this returns the distance to the object you're measuring
  dis = constrain(dis, 10, 80);

  Serial.print("Input: "); Serial.print(analogRead(IN)); Serial.print("  ");
  Serial.print("Filtered: "); Serial.print(analogRead(FILTERED_IN)); Serial.print("  ");
  Serial.print("IR: "); Serial.print(dis); Serial.print("  ");
  Serial.println("uT");



  unsigned long endTime=millis()-startTime;  // the following gives you the time taken to get the measurement     
}
