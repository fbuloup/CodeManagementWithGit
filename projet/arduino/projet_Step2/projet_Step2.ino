bool startLoop = false;
bool restart = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(1000000, SERIAL_8N1);
  while(!startLoop) {
    if(Serial.available()) {
      startLoop = ((char)(Serial.read()) == 'r');
    }
  }
}

void loop() {  
  digitalWrite(LED_BUILTIN, HIGH);
  if(Serial.available()) {
    restart = ((char)(Serial.read()) == 's');
    if(restart) __NVIC_SystemReset();
  }
}