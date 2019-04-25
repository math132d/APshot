char input;

int num = 0, cng = 0;
int minimum = 0, maximum = 100, increment = 20;

void setup() {
  // put your setup code here, to run once:

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // open serial port
  Serial.begin(9600);

  //  //loop to wait for confirmation from the computer
  //  while (true)
  //  {
  //    digitalWrite(LED_BUILTIN, HIGH);
  //    delay(100);
  //    if (Serial.available())
  //    {
  //      input = Serial.read();
  //      break;
  //    }
  //    digitalWrite(LED_BUILTIN, LOW);
  //    delay(100);
  //  }
  //  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available())
  {
    String message = "";
    while (Serial.available())
    {
      input = Serial.read();

      message += input;
    }

    if (message == "R" || message == "r")
    {
      reset();
    }
    else
    {
      Serial.print(message); Serial.print("  ");
      Serial.println("");
    }
  }

  numGen();
  Serial.print("N: "); Serial.print(num); Serial.print("  ");
  Serial.print("C: "); Serial.print(cng); Serial.print("  ");
  Serial.println("");

  delay(100);
}

//this is just a number generator for testing purposes
void numGen()
{
  int newNum = random(num - (increment / 2), num + (increment / 2));
  newNum = constrain(newNum, minimum, maximum);
  cng = newNum - num;
  num = newNum;
}

void reset()
{
  num = 0;
  cng = 0;
}
