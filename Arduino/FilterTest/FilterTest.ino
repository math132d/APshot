int input = A15;
int filteredInput = A14;

//Filer user was 400K ohm, 104pF

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
