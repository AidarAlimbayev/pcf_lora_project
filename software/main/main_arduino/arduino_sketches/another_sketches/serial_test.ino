

void setup(){
  Serial.begin(9600);
}

void loop(){
    Serial.write(45); // send a byte with the value 45
    Serial.write(55);
    Serial.write(65);
    Serial.write(90);
    Serial.write(320);
}