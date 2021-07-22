# rent a cam
## Description
"rent-a-cam" is a smart camera recognition system which was developed to run mainly on a NVIDIA Jetson Nano with an USB camera. It detects the labels which are printed on every camera. So in its core it is a text recognition algorithm which performs the needed preprocessing. Afterwards the optical character recognition is applied. Finally the algorithm searches the recognized text for a specific pattern ("#" followed by four digits) and extracts the four digits, if contained.
    
To use the rent-a-cam system, just place a labeled camera inside the box. An IR-Sensor will detect the object and will signal it to an Arduino Nano. The Arduino will turn on the RGB-LEDs and also send a signal to the Jetson Nano to start the algorithm. The Jetson and the Arduino are communicating via I2C bus. As soon as the camera was detected and the label was recognized, it will be visible on the GUI. 
    
## Installation
To get the system up and running, follow the installation_guide.md
     
## Getting Started
After everything was installed, the installation can be validated by running the program and performing text recognition on one of the sample images. They can be found in the path:
~~~
images/DataSet_Stripe/
~~~
Activate the virtual environment by typing:
~~~
workon <name_of_your_env>
~~~
or without virtualenvwrapper:
~~~
source ./<path_to_your_env>/bin/activate
~~~
As soon as the virtualenv is active, just run the main.py file with the following flags:
~~~
python main.py image -n <number_of_the_image>
~~~
If no number is given, the algorithm will load the first image by default. It is also possible to load an image from another folder. Therefore the path must be given as an input
~~~
python main.py image -f <path_to_image>
~~~
But beware that the algorithm will expect an image with the size 1920x1080 and cut it in the process to 1640x775. So loading a smaller image will throw an error, if the load_image.py function and the vignetting_correction_mask.npy were not adjusted before. Loading a larger image will just cut out the upper left part of the image and continue processing only this area.

If an USB-camera is available, the video mode can also be tested. Just type the following command:
~~~
python main.py video
~~~
The algorithm was carefully programmed to work under specific lighting conditions. So if anything gets changed, the algorithm might not be as accurate and should get reconfigured. Most likely it will come down to reliably detecting the desired contours and ignore others (e.g. contours which are not closed, contours which have too many child contours, ...). To adjust this, it will be helpful to take a look at the edge_detection.py file and get into the documentation of OpenCVs image filtering functions, canny edge detection function as well as their findContours function.

If additional information is needed during runtime (e.g. for the purpose of debugging) another flag is available:
~~~
python main.py image -l
python main.py video -l
~~~
The help function is also available:
~~~
python main.py -h
~~~

Maybe the final project will include the main program with Arduino and IR-sensor communication and a separate debugging script with only the core algorithm.
