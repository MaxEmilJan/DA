 Pins used for the connection between the Arduino Nano and the Adafruit Neopixel:
 
 D2        -->  Data Input
 
 5V        -->  PWR
 
 GND       -->  GND
 
 Pins used for the I2C-connection between the NVIDIA Jetson and the Arduino:
 
 27 (SDA)  -->  A4 (SDA)
 
 28 (SCL)  -->  A5 (SCL)
 
 GND       -->  GND
 
 Pins used for the connection between the Arduino Nano and the IR-Sensor:
 
 D3        -->  Data Output
 
 5V        -->  +
 
 GND       -->  GND
 
 If no more GND-Ports are available at the Arduino it is also possible to connect the Neopixel or the IR-Sensor to the Jetson GND. Or connect all wires and put them on a shared GND-Port.

Additionally the "Adafruit Neopixel"-library needs to be installed on the arduino and the "smbus"-library is required on the Jetson in order to run the files.

> sudo apt-get install python3-smbus

or if you are using a virtual env

> pip install python3-smbus
