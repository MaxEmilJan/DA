## required

To setup the NVIDIA Jetson Nano for this particular usecase, follow the "Getting Started" introduction by NVIDIA.
After the OS is running and an user was added, you can start to install the required packages.
The following packages and their dependencies are needed:
* neoAPI
* numpy
* opencv
* numba
* easyocr, pytesseract
* smbus
---
1. remove libreoffice and the preinstalled numpy version, since it consumes a lot of memory and is not needed for this application.
~~~
sudo apt-get purge libreoffice*
sudo apt remove python-numpy
sudo apt-get clean
~~~
2. update and upgrade the system (may take about 10 minutes)
~~~
sudo apt-get update && sudo apt-get upgrade
~~~
3. install the newest version of pip
~~~
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm get-pip.py
~~~
4. create and activate a virtualenv with python 3.6
~~~
mkvirtualenv <name_of_your_env> -p3.6
source ./<name_of_your_env>/bin/activate
~~~
from now on the virtualenv should stay activated, since everything is going to get installed in the env

5. install the Baumer NeoAPI by following the official installation guide

6. install PyTorch
~~~
wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.9.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip install Cython
pip install numpy==1.19.4 torch-1.8.0-cp36-cp36m-linux_aarch64.whl
rm torch-1.8.0-cp36-cp36m-linux_aarch64.whl
~~~
7. install easyocr
~~~
pip install easyocr
~~~
8. install opencv (should already be installed with easyocr; check if it is the desired version (4.5.X))
~~~
pip install opencv-python
~~~
9. install smbus
~~~
pip install smbus
~~~
10. install numba dependencies
~~~
wget http://releases.llvm.org/7.0.1/llvm-7.0.1.src.tar.xz
tar -xvf llvm-7.0.1.src.tar.xz
rm llvm-7.0.1.src.tar.xz
cd llvm-7.0.1.src
mkdir llvm_build_dir
cd llvm_build_dir/
cmake ../ -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="ARM;X86;AArch64"
make -j4
sudo make install
cd bin/
echo "export LLVM_CONFIG=\""`pwd`"/llvm-config\"" >> ~/.bashrc
echo "alias llvm='"`pwd`"/llvm-lit'" >> ~/.bashrc
source ~/.bashrc
pip install llvmlite==0.30.0
~~~
11. install numba
~~~
pip install numba==0.46.0
~~~
12. install tesseract
~~~
sudo apt install tesseract-ocr libtesseract-dev
~~~
13. find path to tesseract directory and paste it to the header of `text_recognition_cpu.py`\
(default is /usr/bin/tesseract)
~~~
which tesseract
~~~
14. install pytesseract
~~~
pip install pytesseract
~~~
15. install PyQt5 outside of your virtual env
~~~
sudo apt-get install python3-pyqt5
~~~
16. Make the packages outside of your env accessable inside your env by editing `pyvenv.cfg`.\
This file is located in the directory of your virtual env (should be /home/<name_of_your_env>/pyvenv.cfg).\
There you set `system-site-packages = true` and save the changes.

---
## optional

Furthermore the following packages might be usefull for things like debugging:
* Baumer CameraExplorer (installed by following the official guide)
* nano
~~~
sudo apt-get install nano
~~~
* spyder IDE
~~~
pip install spyder
~~~
