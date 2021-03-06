int input = A15;
int filteredInput = A14;

//Filter used was 400K ohm (4x100k in series), 104pF
//We might want to consider using a potentiometer in the setup, so we can adjust it more granuarily

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("Input: "); Serial.print(analogRead(input)); Serial.print("  ");
  Serial.print("Filtered: "); Serial.print(analogRead(filteredInput)); Serial.print("  ");
  Serial.println("uT");
}
