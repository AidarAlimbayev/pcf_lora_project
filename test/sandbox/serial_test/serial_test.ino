
int data;
//data = 45;

void setup(){
  Serial.begin(9600);
}

void loop(){

    data = 55;
    Serial.println(data); // send a byte with the value 45


}
