/**
 *
 * HX711 library for Arduino - example file
 * https://github.com/bogde/HX711
 *
 * MIT License
 * (c) 2018 Bogdan Necula
 *
**/
#include "HX711.h"


// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 6;
const int LOADCELL_SCK_PIN = 5;
int weight = 0;

HX711 scale;

void setup() {
  Serial.begin(9600);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.read();			// print a raw reading from the ADC
  scale.read_average(20);  	// print the average of 20 readings from the ADC
  Serial.println(scale.get_units(5), 1);	// print the average of 5 readings from the ADC minus tare weight (not set) divided
  scale.set_scale(-3047.f);
  scale.tare();				        // reset the scale to 0
  scale.read();                 // print a raw reading from the ADC
  scale.read_average(20);
  scale.get_value(5);

  Serial.println(scale.get_units(5), 1);        // print the average of 5 readings from the ADC minus tare weight, divided
						// by the SCALE parameter set with set_scale

  //Serial.println("Readings:");
}

void loop() {
  weight = scale.get_units(10);

  if (weight < 0){
    Serial.println(0);
  } else {
    Serial.println(weight);
  }

  //scale.power_down();			        // put the ADC in sleep mode
  delay(1000);
  //scale.power_up();
}
