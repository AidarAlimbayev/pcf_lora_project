#include "HX711.h"

const int LOADCELL_DOUT_PIN = 6;
const int LOADCELL_SCK_PIN = 5;

HX711 scale;

void setup() {
  Serial.begin(9600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.read();			
  scale.read_average(20);  
  scale.set_scale(2923.f);
  scale.tare();				        
  scale.read();                
  scale.read_average(20);
  scale.get_value(5);
}

void loop() {
  Serial.println(scale.get_units(10), 0);
  delay(1000);
}
