#include <SharpIR.h>

#define IN A14
#define FILTERED_IN A15
#define IR A0 // define IR signal pin
#define model 1080 // used 1080 because model GP2Y0A21YK0F is used

#define LOG_SIZE 5

//Filter used was 400K ohm (4x100k in series), 104pF
//We might want to consider using a potentiometer in the setup, so we can adjust it more granuarily
enum Mode {RAW, AVG, MED};
Mode mode = MED;

SharpIR SharpIR(IR, model);
bool debug = false;
bool averageDis = true;
int disLog[LOG_SIZE];
int disLogSort[LOG_SIZE];

int dis = 0;
int disOut = 0;
int filteredIn = 0;


void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < LOG_SIZE; i++)
  {
    disLog[i] = 10;
  }

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  dis = SharpIR.distance();  // this returns the distance to the object you're measuring
  dis = constrain(dis, 10, 80);
  filteredIn = analogRead(FILTERED_IN);

  switch (mode) {
    case RAW: // Use raw input from distance sensor
      disOut = dis;
      break;

    case AVG: // Use average of LOG_SIZE samples
      disOut = 0;
      for (int i = LOG_SIZE - 1; i >= 0; i--)
      {
        if (i != 0)
        {
          disLog[i] =  disLog[i - 1];
          disOut += disLog[i];
        }
        else
        {
          disLog[i] = dis;
          disOut += disLog[i];
        }
      }


      disOut /= LOG_SIZE;
      break;

    case MED: // Use median of LOG_SIZE samples. Requires sorting!
      for (int i = LOG_SIZE - 1; i >= 1; i--)
      {
        disLog[i] =  disLog[i - 1];
        disLogSort[i] = disLog[i];
      }
      disLog[0] = dis;
      disLogSort[0] = disLog[0];

      bubbleSort(disLogSort, LOG_SIZE);
      disOut = median(disLogSort, LOG_SIZE);

      break;
  }


  if (debug)
  {
    Serial.print("Input: "); Serial.print(analogRead(IN)); Serial.print("  ");
    Serial.print("Filtered: "); Serial.print(filteredIn); Serial.print("  ");

    Serial.print("IR: "); Serial.print(disOut); Serial.print("  ");
    Serial.print("Vin: "); Serial.print(analogRead(A8) / 1024.0f * 5.0f); Serial.print("  ");
    Serial.println("");
  }
  else
  {
    Serial.print("D: "); Serial.print(disOut); Serial.print(" ");
    Serial.print("I: "); Serial.print(filteredIn); Serial.print(" ");
    Serial.println("");
  }

}

void bubbleSort(int a[], int size) {
  for (int i = 0; i < (size - 1); i++) {
    for (int o = 0; o < (size - (i + 1)); o++) {
      if (a[o] > a[o + 1]) {
        int t = a[o];
        a[o] = a[o + 1];
        a[o + 1] = t;
      }
    }
  }
}

int median(int a[], int size)
{
  if ((size & 0x01) == 0)
  {
    return a[size / 2];
  }
  else
  {
    return (a[size / 2] + a[(size / 2) + 1]) / 2;
  }
}
