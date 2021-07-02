To setup the NVIDIA Jetson Nano for this particular usecase, follow the "Getting Started" introduction by NVIDIA.
After the OS is running and an user was added, you can start to install the required packages.

1. remove libreoffice, since it consumes a lot of memory and is not needed for this application.
> sudo apt-get purge libreoffice*
> sudo apt-get clean

2. update and upgrade the system (may take about 10 minutes)
> sudo apt-get update && sudo apt-get upgrade

3. install the newest version of pip
> wget https://bootstrap.pypa.io/get-pip.py
> sudo python3 get-pip.py
> rm get-pip.py

4. install virtualenv
> sudo pip install virtualenv

5. create virtual environment with python 3.6 (will be created in the current working directory)
> virtualenv -p 3.6 "<name_of_your_env>"

6. activate the environment
> source <path_to_your_environment>/bin/activate

7. install the Baumer NeoAPI to your environment by following the official installation guide

8. install numpy to your environment (version 1.19.4)
> pip install numpy==1.19.4

9. install opencv to your environment
> ____

10. install pytasseract to your environment
> ____

11. install smbus outside your environment
> deactivate
> sudo apt-get install python3-smbus

12. uninstall preinstalled systemwide numpy 1.13
> sudo pip uninstall numpy

