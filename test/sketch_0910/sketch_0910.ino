/*
 Setup your scale and start the sketch WITHOUT a weight on the scale
 Once readings are displayed place the weight on the scale
 Press +/- or a/z to adjust the calibration_factor until the output readings match the known weight
 Arduino pin 6 -> HX711 CLK
 Arduino pin 5 -> HX711 DOUT
 Arduino pin 5V -> HX711 VCC
 Arduino pin GND -> HX711 GND 
*/

#include "HX711.h"

HX711 scale;   // DT, CLK

float calibration_factor = 0.1; // this calibration factor is adjusted according to my load cell
float units;
float ounces;

int marker = 0;

void setup_scale()
{
  if (marker == 0)
    {
      Serial.begin(9600);
      scale.begin(A1, A0);
      scale.set_scale();
      scale.tare();  //Reset the scale to 0
      long zero_factor = scale.read_average(); //Get a baseline reading
      scale.set_scale(calibration_factor); //Adjust to this calibration factor
      marker == 1;
    }
}

void setup() {
  
  setup_scale();
}

void loop() {
delay (1000);

  units = scale.get_units(), 10;
  if (units < 0)
  {
    units = 0.00;
  }
  
  ounces = units * 0.035274;
  Serial.println(ounces);

}
