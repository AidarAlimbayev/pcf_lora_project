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
  char array[4] = {0}; // определяем массив из 4 байтов и заполняем его нулями
  // чтение данных с датчика и сохранение их в массиве
  long adc_val = scale.read();
  array[0] = (adc_val >> 24)*0xFF;
  array[1] = (adc_val >> 16)*0xFF;
  array[2] = (adc_val >> 8)*0xFF;
  array[3] = adc_val*0xFF;

  delay(10); // задержка для восстановления датчика
  Serial.println(adc_val);

  
  if (Serial.available() > 0) {
    inByte = Serial.read();
    if (inByte == 2) {
      Serial.write(adc_val); // отправка массива на Raspberry Pi
    }
  }
}


/* Processing sketch to run with this example:

  // This example code is in the public domain.

  import processing.serial.*;

  int bgcolor;           // Background color
  int fgcolor;           // Fill color
  Serial myPort;                       // The serial port
  int[] serialInArray = new int[3];    // Where we'll put what we receive
  int serialCount = 0;                 // A count of how many bytes we receive
  int xpos, ypos;                // Starting position of the ball
  boolean firstContact = false;        // Whether we've heard from the microcontroller

  void setup() {
    size(256, 256);  // Stage size
    noStroke();      // No border on the next thing drawn

    // Set the starting position of the ball (middle of the stage)
    xpos = width / 2;
    ypos = height / 2;

    // Print a list of the serial ports for debugging purposes
    // if using Processing 2.1 or later, use Serial.printArray()
    println(Serial.list());

    // I know that the first port in the serial list on my Mac is always my FTDI
    // adaptor, so I open Serial.list()[0].
    // On Windows machines, this generally opens COM1.
    // Open whatever port is the one you're using.
    String portName = Serial.list()[0];
    myPort = new Serial(this, portName, 9600);
  }

  void draw() {
    background(bgcolor);
    fill(fgcolor);
    // Draw the shape
    ellipse(xpos, ypos, 20, 20);
  }

  void serialEvent(Serial myPort) {
    // read a byte from the serial port:
    int inByte = myPort.read();
    // if this is the first byte received, and it's an A, clear the serial
    // buffer and note that you've had first contact from the microcontroller.
    // Otherwise, add the incoming byte to the array:
    if (firstContact == false) {
      if (inByte == 'A') {
        myPort.clear();          // clear the serial port buffer
        firstContact = true;     // you've had first contact from the microcontroller
        myPort.write('A');       // ask for more
      }
    }
    else {
      // Add the latest byte from the serial port to array:
      serialInArray[serialCount] = inByte;
      serialCount++;

      // If we have 3 bytes:
      if (serialCount > 2 ) {
        xpos = serialInArray[0];
        ypos = serialInArray[1];
        fgcolor = serialInArray[2];

        // print the values (for debugging purposes only):
        println(xpos + "\t" + ypos + "\t" + fgcolor);

        // Send a capital A to request new sensor readings:
        myPort.write('A');
        // Reset serialCount:
        serialCount = 0;
      }
    }
  }

*/
