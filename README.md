<h1>rent-a-cam<h1>
  <h2>Description<h2>
"rent-a-cam" is a smart camera recognition system which was developed to run mainly on a NVIDIA Jetson Nano with an USB camera. It detects the labels which are printed on every camera. So in its core it is a text recognition algorithm which performs the needed preprocessing. Afterwards the optical character recognition is apllied. Finally the algorithm searches the recognised text for a specific pattern ("#" followed by four digits) and extracts the four digits, if contained.
    
To use the rent-a-cam system, just place a labeled camera inside the box. An IR-Sensor will detect the object and will signal it to an Arduino Nano. The Arduino will turn on the RGB-LEDs and also send a signal to the Jetson Nano to start the algorithm. The Jetson and the Arduino are communicating via I2C bus. As soon as the camera was detected and the label was recognised, it will be visible on the GUI. 
    
  <h2>Installation<h2>
To get the system up and running, follow the installation_guide.md
     
  <h2>Samples<h2>
read img....
