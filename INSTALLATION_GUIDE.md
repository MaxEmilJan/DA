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
pip3 install --upgrade setuptools
~~~
4. create and activate a virtualenv with python 3.6
~~~
mkvirtualenv <name_of_your_env> -p3.6
source ./<name_of_your_env>/bin/activate
~~~
from now on the virtualenv should stay activated, since everything is going to get installed in the env

5. download the Baumer NeoAPI
- open internet explorer
- paste in url 'https://www.baumer.com/us/en/product-overview/industrial-cameras-image-processing/software/baumer-neoapi/c/42528'
- download the correct package for your OS und unpack it
- install it by followning the official installation guide

6. install PyTorch
~~~
wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.9.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip install Cython
pip install numpy==1.19.4 torch-1.9.0-cp36-cp36m-linux_aarch64.whl
rm torch-1.9.0-cp36-cp36m-linux_aarch64.whl
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
sudo apt install spyder3
~~~

---
## pip list

| Package | Version |
| :-- | --: |
|apturl                            |0.5.2|
|asn1crypto                        |0.24.0|
|backports.entry-points-selectable |1.1.0|
|beautifulsoup4                    |4.6.0|
|blinker                           |1.4|
|Brlapi                            |0.6.6|
|certifi                           |2018.1.18|
|chardet                           |3.0.4|
|click                             |6.7|
|colorama                          |0.4.4|
|cryptography                      |2.1.4|
|cupshelpers                       |1.0|
|cycler                            |0.10.0|
|Cython                            |0.29.24|
|dataclasses                       |0.8|
|decorator                         |4.4.2|
|defer                             |1.0.6|
|distlib                           |0.3.2|
|distro-info                       |0.18ubuntu0.18.04.1|
|easyocr                           |1.4|
|feedparser                        |5.2.1|
|filelock                          |3.0.12|
|graphsurgeon                      |0.4.5|
|html5lib                          |0.999999999|
|httplib2                          |0.9.2|
|idna                              |2.6|
|imageio                           |2.9.0|
|importlib-metadata                |4.6.1|
|importlib-resources               |5.2.0|
|Jetson.GPIO                       |2.0.16|
|keyring                           |10.6.0|
|keyrings.alt                      |3.0|
|kiwisolver                        |1.3.1|
|language-selector                 |0.1|
|launchpadlib                      |1.10.6|
|lazr.restfulclient                |0.13.5|
|lazr.uri                          |1.0.3|
|llvmlite                          |0.30.0|
|louis                             |3.5.0|
|lxml                              |4.2.1|
|macaroonbakery                    |1.1.3|
|Mako                              |1.0.7|
|MarkupSafe                        |1.0|
|matplotlib                        |3.3.4|
|neoapi                            |1.1.1|
|networkx                          |2.5.1|
|numba                             |0.46.0|
|numpy                             |1.19.4|
|oauth                             |1.0.1|
|oauthlib                          |2.0.6|
|onboard                           |1.4.1|
|opencv-python                     |4.5.3.56|
|packaging                         |21.0|
|pandas                            |0.22.0|
|pbr                               |5.6.0|
|Pillow                            |8.3.1|
|pip                               |21.2.4|
|platformdirs                      |2.0.2|
|protobuf                          |3.0.0|
|pycairo                           |1.16.2|
|pycrypto                          |2.6.1|
|pycups                            |1.9.73|
|PyGObject                         |3.26.1|
|PyJWT                             |1.5.3|
|pymacaroons                       |0.13.0|
|PyNaCl                            |1.1.2|
|pyparsing                         |2.4.7|
|pyRFC3339                         |1.0|
|pytesseract                       |0.3.8|
|python-apt                        |1.6.5+ubuntu0.6|
|python-bidi                       |0.4.2|
|python-dateutil                   |2.8.2|
|python-debian                     |0.1.32|
|pytz                              |2018.3|
|PyWavelets                        |1.1.1|
|pyxattr                           |0.6.0|
|pyxdg                             |0.25|
|PyYAML                            |5.4.1|
|requests                          |2.18.4|
|requests-unixsocket               |0.1.5|
|scikit-image                      |0.17.2|
|scipy                             |1.5.4|
|SecretStorage                     |2.3.1|
|setuptools                        |57.1.0|
|simplejson                        |3.13.2|
|sip                               |6.1.1|
|six                               |1.16.0|
|smbus                             |1.1.post2|
|ssh-import-id                     |5.7|
|stevedore                         |3.3.0|
|system-service                    |0.3|
|systemd-python                    |234|
|tensorrt                          |7.1.3.0|
|tifffile                          |2020.9.3|
|toml                              |0.10.2|
|torch                             |1.8.0|
|torchvision                       |0.10.0|
|typing-extensions                 |3.10.0.0|
|ubuntu-drivers-common             |0.0.0|
|uff                               |0.6.9|
|unity-scope-calculator            |0.1|
|unity-scope-chromiumbookmarks     |0.1|
|unity-scope-colourlovers          |0.1|
|unity-scope-devhelp               |0.1|
|unity-scope-firefoxbookmarks      |0.1|
|unity-scope-manpages              |0.1|
|unity-scope-openclipart           |0.1|
|unity-scope-texdoc                |0.1|
|unity-scope-tomboy                |0.1|
|unity-scope-virtualbox            |0.1|
|unity-scope-yelp                  |0.1|
|unity-scope-zotero                |0.1|
|urllib3                           |1.22|
|urwid                             |2.0.1|
|virtualenv                        |20.6.0|
|virtualenv-clone                  |0.5.5|
|virtualenvwrapper                 |4.8.4|
|wadllib                           |1.3.2|
|webencodings                      |0.5|
|wheel                             |0.36.2|
|xkit                              |0.0.0|
|youtube_dl                        |2018.3.14|
|zipp                              |3.5.0|
|zope.interface                    |4.3.2|
