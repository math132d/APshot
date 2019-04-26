void setup() {
  Serial.begin(115200);
}

void loop() {
  a = random(100, 1000);
  Serial.print(a);
  delay(1024);
}
