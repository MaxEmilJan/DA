#include <Wire.h>
#include <Adafruit_NeoPixel.h>

// set the Arduino-Pin to connect the DATA OUT-Port of the IR-Sensor to
#define PIN_IR         3
// set the Arduino-Pin to connect the DATA IN-Port of the LED Stripe to
#define PIN_LED        2
// set the number of RGB-LEDs you want to adress
#define NUMPIXELS      16
// configure LED Stripe
Adafruit_NeoPixel strip(NUMPIXELS, PIN_LED, NEO_GRB + NEO_KHZ800);

// set the Address for the I2C connection to the Jetson (0x40 as default)
int i2cAddress = 0x40;
// set IR-Sensor state
int state_IR = 0;

void setup() {
  // join I2C Bus with address #0x40
  Wire.begin(i2cAddress);
  Wire.onRequest(requestEvent);
  // init serial output with given baud-rate
  Serial.begin (9600);
  // init Sensorpin
  pinMode (PIN_IR, INPUT);
  // init Stripe
  strip.begin();
}

void loop() {
  // read signal from sensor
  bool val = digitalRead(PIN_IR);
  // if "low" (obstacle detected)
  if (val == LOW) {
    state_IR = 1;
    // turn the LED Stripe ON
    for(int i=0; i<NUMPIXELS-8; i++) {
      // set the bottom stripe to maximum intensity
      strip.setPixelColor(i, strip.Color(255, 255, 255));
    }
    for(int i=8; i<NUMPIXELS; i++) {
      // set the top stripe to medium intensity
      strip.setPixelColor(i, strip.Color(150, 150, 150));
    }
    strip.show();
    }
    else {
      state_IR = 0;
      // turn the LED Stripe OFF
      for(int i=0; i<NUMPIXELS; i++) {
        // set the bottom stripe to maximum intensity
        strip.setPixelColor(i, strip.Color(0, 0, 0));
        strip.show();
    }
    }
}

// this function will be called when the master reads data from bus
void requestEvent() {
  // if "low" (obstacle detected)
  if (state_IR == 1){
    // send 1 to bus
    Wire.write(1);
    }
  else {
    // send 0 to bus
    Wire.write(0);
    }
}
