#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 6;
const int LOADCELL_SCK_PIN = 5;

HX711 scale;

        // incoming serial byte

void setup() {
  // start serial port at 9600 bps:
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN, 128);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  pinMode(2, INPUT);   // digital sensor is on digital pin 2

}

void loop() {
  int inByte = 0; 
  // if we get a valid byte, read analog ins:
  long adc_val = scale.read();
        //float w = 70.0 * ((float)reading - 63000.0)/238000.0;
  char array[] = {};
  array[0] = (adc_val >> 24)*0xFF;
  array[1] = (adc_val >> 16)*0xFF;
  array[2] = (adc_val >> 8)*0xFF;
  array[3] = adc_val*0xFF;
        
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    if (inByte == 2) {
        Serial.write(array,4);
        
        // delay 10ms to let the ADC recover:
        //delay(10);
        
    //    Serial.write(120.0);
    //    Serial.write(135.0);
    //    Serial.write(140.0);
    }
  }
}
