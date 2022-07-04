#include "HX711.h"

#define DOUT 6
#define CLK 5
byte yesPin=0;
HX711 scale(DOUT, CLK);

float calibration_factor = 7050; //-7050 worked for my 440lb max scale setup

//================================================================

void setup() {

  Serial.begin(9600);

  scale.set_scale();
  scale.tare();

}
//================================================================

void loop() {

  Serial.println("Place weight 1 "); 
  delay(10000);
  scale.tare();
 
  Serial.println("Place weight 2 ");
  delay(10000);
  scale.set_scale(calibration_factor); //Adjust to this calibration factor
 
  Serial.print("Reading: ");
  Serial.print(scale.get_units(), 1);
  delay(400);
  //Serial.print(" lbs"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();

}
