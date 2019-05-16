#include <SharpIR.h>

#define IN A14
#define FILTERED_IN A15
#define IR A0 // define IR signal pin
#define model 1080 // used 1080 because model GP2Y0A21YK0F is used

#define DIS_LOG_SIZE 5
#define FIL_LOG_SIZE 3

//Filter used was 470K ohm, 104pF
enum Mode {RAW, AVG, MED};
Mode mode = MED;

SharpIR SharpIR(IR, model);
bool debug = false;
bool arduinoLog = false;
int disLog[DIS_LOG_SIZE];
int disLogSort[DIS_LOG_SIZE];
int dis = 0;
int disOut = 0;

int filteredIn = 0;
int filteredThreshold = 5;
int filteredLog[FIL_LOG_SIZE];

bool sendInput = false;
bool inputHandled = false;

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < DIS_LOG_SIZE; i++)
  {
    disLog[i] = 10;
  }

  for (int i = 0; i < FIL_LOG_SIZE; i++)
  {
    disLog[i] = 0;
  }

  Serial.begin(9600);
}

void loop() {
  // Pressure button
  // Read and log the input from the pressure button
  filteredIn = analogRead(FILTERED_IN);
  for (int i = FIL_LOG_SIZE - 1; i >= 0; i--)
  {
    if (i != 0)
    {
      filteredLog[i] = filteredLog[i - 1];
    }
    else
    {
      filteredLog[i] = filteredIn;
    }
  }

  // Check if the current sample is above the threshold
  if (filteredIn > filteredThreshold)
  {
    // Check if the remaining samples are above the threshold
    bool test = true;
    for ( int i = 1; i < FIL_LOG_SIZE; i++)
    {
      if (filteredLog[i] < filteredThreshold)
      {
        test = false;
        break;
      }
    }
    // If all samples are valid, set to send
    if (test)
    {
      sendInput = true;
    }
  }
  else if (filteredIn == 0)
  {
    // If current sample is at zero, reset sending
    sendInput = false;
    inputHandled = false;
  }


  // Distance sensor
  dis = SharpIR.distance();  // this returns the distance to the object you're measuring
  dis = constrain(dis, 10, 80);
  switch (mode) {
    case RAW: // Use raw input from distance sensor
      disOut = dis;
      break;

    case AVG: // Use average of DIS_LOG_SIZE samples
      disOut = 0;
      for (int i = DIS_LOG_SIZE - 1; i >= 0; i--)
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

      disOut /= DIS_LOG_SIZE;
      break;

    case MED: // Use median of DIS_LOG_SIZE samples. Requires sorting!
      for (int i = DIS_LOG_SIZE - 1; i >= 1; i--)
      {
        disLog[i] =  disLog[i - 1];
        disLogSort[i] = disLog[i];
      }
      disLog[0] = dis;
      disLogSort[0] = disLog[0];

      bubbleSort(disLogSort, DIS_LOG_SIZE);
      disOut = median(disLogSort, DIS_LOG_SIZE);

      break;
  }

  // debug mode outputs all information constantly
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
    // If a valid press has been detected, and not yet been sent, send through serial
    if (sendInput && !inputHandled)
    {
      if (arduinoLog) {
        // Send distance
        Serial.print("D: "); Serial.print(disOut); Serial.print(" ");
        // Send button input
        Serial.print("I: "); Serial.print(filteredIn); Serial.print(" ");
        Serial.println("");
      }
      else
      {
        // Send information for python
        Serial.print(disOut); Serial.print(":"); Serial.print(filteredIn);
        Serial.println("");
      }
      // Mark message as sent
      inputHandled = true;
    }
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
