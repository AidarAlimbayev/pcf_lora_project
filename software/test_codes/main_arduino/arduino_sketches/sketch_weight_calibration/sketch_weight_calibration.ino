

#include <HX711.h>

#define DOUT 6
#define CLK 5

float calibration_factor = 1500.85;

HX711 scale;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 calibration");
  Serial.println("Press + to increase");
  Serial.println("Press - to decrease");
  scale.set_scale();
  scale.tare();
}

void loop() {
  scale.set_scale(calibration_factor);
  Serial.print("Reading: ");
  Serial.print(scale.get_units()*0.453592);
  Serial.print(" Kg");
  Serial.print(" calibration_factor ");
  Serial.print(calibration_factor);
  Serial.println();

  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+')
      calibration_factor += 100;
    else if (temp == '-')
      calibration_factor -= 100;
  }
}
