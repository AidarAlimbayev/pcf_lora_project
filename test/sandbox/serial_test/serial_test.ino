
int data;
//data = 45;

void setup(){
  Serial.begin(9600);
}

void loop(){
    Serial.println(300); // send a byte with the value 45
    delay(500);
    Serial.println(350);
    delay(500);
    Serial.println(380);
    delay(500);
    Serial.println(400);
    delay(500);
    Serial.println(0);
    delay(500);
}
