#include "HX711.h"

HX711 scale(A1, A0);                          
HX711 scale1(A2, A3); 
float calibration_factor = 0.4;          // калибровка!
float units;
float ounces;
float calibration_factor1 = 0.4;          // калибровка!
float units1;
float ounces1;
float all;
void setup() {
  
  Serial.begin(9600); 
  scale.set_scale();
  scale.tare();                              //Сбрасываем на 0
  scale.set_scale(calibration_factor); 
   scale1.set_scale();
  scale1.tare();                              //Сбрасываем на 0
  scale1.set_scale(calibration_factor1); //Применяем калибровку
}

void loop() { 
  delay(1000);

  Serial.print("Reading: ");
  
  for(int i = 0;i < 10; i ++) units =+ scale.get_units(), 10;   // усредняем показания считав 10 раз 
  units / 10;                                                   // делим на 10
   
  ounces = units * 0.035274;                                    // переводим унции в граммы              
  Serial.print(ounces);                                          // отправляем в монитор порта
  Serial.print(" grams");  
  Serial.println(); 
  Serial.print("Reading1: ");
  
  for(int i = 0;i < 10; i ++) units1 =+ scale1.get_units(), 10;   // усредняем показания считав 10 раз 
  units1 / 10;                                                   // делим на 10
   
  ounces1 = units1 * 0.035274;                                    // переводим унции в граммы              
  Serial.print(ounces1);                                          // отправляем в монитор порта
  Serial.print(" grams");  
  Serial.println(); 
  all =   ounces +   ounces1;
   Serial.print(all); 
   Serial.print("all:"); 
}
