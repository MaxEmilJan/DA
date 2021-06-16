#include <Wire.h>
#include <Adafruit_NeoPixel.h>

// set the PIN of your DATA IN Port
#define PIN        2
// set the number of RGB-LEDs you want to adress
#define NUMPIXELS 24
// init your LED ring
Adafruit_NeoPixel ring(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// set the Address for the I2C connection to the Jetson (0x40 as default)
int i2cAddress = 0x40;
int ledState;

void setup()
{
  // join i2c bus with address #0x40
  Wire.begin(i2cAddress);
  // register event
  Wire.onReceive(receiveEvent);           
  Wire.onRequest(sendData);

  pinMode(LED_BUILTIN, OUTPUT);
  ring.begin();
}

void receiveEvent(int bytes) {
  ledState = Wire.read();    // read one character from the I2C
}

void loop()
{
  if(ledState == 0) {
    digitalWrite(LED_BUILTIN, LOW);
    for(int i=0; i<NUMPIXELS; i++) {
      // set the color; dark
      ring.setPixelColor(i, ring.Color(0, 0, 0));
      ring.show();
    }
  }
  if(ledState == 1) {
    digitalWrite(LED_BUILTIN, HIGH);
    for(int i=0; i<NUMPIXELS; i++) {
      if((5 <= i && i < 11) || (17 <= i && i < 23)) {
        // set the color; warm white
        ring.setPixelColor(i, ring.Color(255, 255, 255));
        ring.show(); 
      }
      else {
        ring.setPixelColor(i, ring.Color(0, 0, 0));
        ring.show(); 
      }
    }
  }
  if(ledState == 2) {
    digitalWrite(LED_BUILTIN, HIGH);
    for(int i=0; i<NUMPIXELS; i++) {
      if((0 <= i && i < 5) || (11 <= i && i < 16)) {
        // set the color; warm white
        ring.setPixelColor(i, ring.Color(255, 255, 255));
        ring.show(); 
      }
      else {
        ring.setPixelColor(i, ring.Color(0, 0, 0));
        ring.show(); 
      }
    }
  }
}

void sendData(){
    Wire.write(ledState);
}
