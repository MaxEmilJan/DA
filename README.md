This Repository contains all files and scrips, which are required for this text recognition project to work.
The core algorithm is run on an NVIDIA Jetson Nano. For the computer vision part, a USB-camera is connected to the Jetson.
The Jetson communicates with an Arduino Nano via I2C, which is controlling the Illumination (Adafruit Neopixel RGB Ring).

It is best to create a virtual python environment. This can be done by the following commands:

if the package "virtualenv" is not installed yet (otherwise skip this):

> pip install virtualenv

create your virtual environment with Python 3.6:

> virtualenv -p 3.6 "name_of_your_virtual_env" 

activate your environment to work within it:

> source ./"path_to_your_environment"/bin/activate

install the Baumer neoAPI to your environment by following the official guide. 
Also install numpy to your environment:

> pip install numpy

install opencv to your environment:

> pip install opencv-python

install pytesseract to your environment:

> ...

install smbus outside your environment:

> sudo apt-get install python3-smbus
