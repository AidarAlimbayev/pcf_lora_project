/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

//Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

Servo servo_1;
Servo servo_2;
Servo servo_3;
Servo servo_4;
Servo servo_5;
Servo servo_6;
Servo servo_7;
Servo servo_8;


int pos = 0;    // variable to store the servo position

void setup() {
  //myservo.attach(13);  // attaches the servo on pin 9 to the servo object
  servo_1.attach(11);
  servo_2.attach(10);
  servo_3.attach(9);
  servo_4.attach(8);
  servo_5.attach(7);
  servo_6.attach(6);
  servo_7.attach(5);
  servo_8.attach(4);
  
}

void loop() {
  for (pos = 0; pos <= 90; pos += 1) { // goes from 0 degrees to 90 degrees
    // in steps of 1 degree
    //myservo.write(pos);              // tell servo to go to position in variable 'pos'
    servo_1.write(pos);
    servo_2.write(90 - pos);
    servo_3.write(pos);
    servo_4.write(90 - pos);
    servo_5.write(pos);
    servo_6.write(90 - pos);
    servo_7.write(pos);
    servo_8.write(90 - pos);
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  for (pos = 90; pos >= 0; pos -= 1) { // goes from 90 degrees to 0 degrees
    //myservo.write(pos); // tell servo to go to position in variable 'pos'    1_servo.write(pos);
    servo_1.write(90 - pos);
    servo_2.write(pos);
    servo_3.write(90 - pos);
    servo_4.write(pos);
    servo_5.write(90 - pos);
    servo_6.write(pos);
    servo_7.write(90 - pos);   
    servo_8.write(pos);
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
}
