This Repository contains all files and scrips, which are required for this text recognition project to work.
The core algorithm is run on an NVIDIA Jetson Nano. For the computer vision part, a USB-camera is connected to the Jetson.
The Jetson communicates with an Arduino Nano via I2C, which is controlling the Illumination (Adafruit Neopixel RGB Stripe) and reads the output of an IR-Sensor.
As soon as the sensor detects an obstacle, the Arduino turns on the lighting and signals the Jetson nano to run the text recognition.

To get the system up and running, follow the installation_guide.md
