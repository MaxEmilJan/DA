#include <Wire.h>
#include <Adafruit_NeoPixel.h>

// set the PIN of your DATA IN Port
#define PIN        2
// set the number of RGB-LEDs you want to adress
#define NUMPIXELS 16
// init your LED strip
Adafruit_NeoPixel strip(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

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
  strip.begin();
}

void receiveEvent(int bytes) {
  ledState = Wire.read();    // read one character from the I2C
}

void loop()
{
  for(int i=0; i<NUMPIXELS-8; i++) {
    // set the color; dark
    strip.setPixelColor(i, strip.Color(255, 255, 255));
    //strip.show();
  }
  for(int i=8; i<NUMPIXELS; i++) {
    // set the color; dark
    strip.setPixelColor(i, strip.Color(255, 255, 255));
    strip.show();
  }
//  if(ledState == 0) {
//    digitalWrite(LED_BUILTIN, LOW);
//    for(int i=0; i<NUMPIXELS; i++) {
//      // set the color; dark
//      strip.setPixelColor(i, strip.Color(0, 0, 0));
//      strip.show();
//    }
//  }
//  if(ledState == 1) {
//    digitalWrite(LED_BUILTIN, HIGH);
//    for(int i=0; i<NUMPIXELS; i++) {
//      // set the color; warm white
//      strip.setPixelColor(i, strip.Color(255, 255, 255));
//      strip.show();
//    }
//  }
}

void sendData(){
    Wire.write(ledState);
}
