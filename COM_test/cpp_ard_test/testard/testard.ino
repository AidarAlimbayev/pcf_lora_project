

char buffer[256];

void setup() {
  Serial.begin(9600);
  

}

void loop() {
 if(Serial.available() > 0){
  Serial.readBytes(buffer, 256);
  Serial.println(buffer);
  delay(5000);
 }

}
