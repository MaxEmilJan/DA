To setup the NVIDIA Jetson Nano for this particular usecase, follow the "Getting Started" introduction by NVIDIA.
After the OS is running and an user was added, you can start to install the required packages.
The following packages and their dependencies are needed:
* neoAPI
* numpy
* opencv
* numba
* easyocr, pytesseract
* smbus

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
4. install virtualenv and virtualenvwrapper
~~~
sudo pip install virtualenv virtualenvwrapper
~~~
5. create and activate a virtualenv with python 3.6
~~~
mkvirtualenv <name_of_your_env> -p3.6
workon <name_of_your_env>
~~~
6. install the Baumer NeoAPI to your environment by following the official installation guide

7. install PyTorch while in your env
~~~
wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.9.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip install Cython
pip install numpy torch-1.8.0-cp36-cp36m-linux_aarch64.whl
rm torch-1.8.0-cp36-cp36m-linux_aarch64.whl
~~~
8. Since the previous step also installed numpy 1.19.5 we have to remove it and replace it with numpy 1.19.4 (1.19.5 does not work in a virtual env)
~~~
pip uninstall numpy
pip install numpy==1.19.4
~~~
9. install easyocr in your env
~~~
pip install easyocr
~~~
10. install opencv in your env
~~~
pip install opencv-python
~~~
13. install smbus
~~~
pip install smbus
~~~
14. install numba dependencies
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
15. install numba
~~~
pip install numba==0.46.0
~~~

Furthermore the following packages might be usefull for things like debugging:
1. Baumer CameraExplorer (install by following the official guide)
2. nano
~~~
sudo apt-get install nano
