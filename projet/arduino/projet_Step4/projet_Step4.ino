bool startLoop = false;
bool restart = false;
bool firstLoop = true;
unsigned long initTime, time;
char serialMessage[64];

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
  if(firstLoop) {
    digitalWrite(LED_BUILTIN, HIGH);
    firstLoop = false;
    initTime = micros();
    time = 0;
  } else time = micros() - initTime;
  if(Serial.available()) {
    restart = ((char)(Serial.read()) == 's');
    if(restart) __NVIC_SystemReset();
  }
  sprintf(serialMessage, "%lu", time);
	Serial.println(serialMessage);
	Serial.flush();
}