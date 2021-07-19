<h1>rent-a-cam<h1>
  <h2>Description<h2>
    "rent-a-cam" is a smart camera recognition system which was developed to run mainly on a NVIDIA Jetson Nano. It detects the labels which are printed on every       camera. So in its core it is a text recognition algorithm which performs the needed preprocessing. Afterwards the optical character recognition is apllied.         Finally the algorithm searches the recognised text for a specific pattern ("#" followed by four digits) and extracts the four digits, if contained.
    
    This Repository contains all the files and scrips, which are required for this project to work.
    The core algorithm is run on an NVIDIA Jetson Nano. For the computer vision part, a USB-camera is connected to the Jetson.
    The Jetson communicates with an Arduino Nano via I2C, which is controlling the Illumination (Adafruit Neopixel RGB Stripe) and reads the output of an IR-Sensor.
    As soon as the sensor detects an obstacle, the Arduino turns on the lighting and signals the Jetson nano to run the text recognition.

   <h2>Installation<h2>
     To get the system up and running, follow the installation_guide.md
     
   <h2>Samples<h2>
     read img....
