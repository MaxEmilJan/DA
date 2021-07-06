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

4. install the Baumer NeoAPI to your environment by following the official installation guide

5. install numpy (version 1.19.4)
> pip3 install numpy==1.19.4

6. install opencv dependencies
> dependencies=(build-essential
              cmake
              pkg-config
              libavcodec-dev
              libavformat-dev
              libswscale-dev
              libv4l-dev
              libxvidcore-dev
              libavresample-dev
              python3-dev
              libtbb2
              libtbb-dev
              libtiff-dev
              libjpeg-dev
              libpng-dev
              libtiff-dev
              libdc1394-22-dev
              libgtk-3-dev
              libcanberra-gtk3-module
              libatlas-base-dev
              gfortran
              wget
              unzip)

> sudo apt install -y ${dependencies[@]}

8. download opencv 
> wget https://github.com/opencv/opencv/archive/4.5.2.zip -O opencv-4.5.2.zip

> wget https://github.com/opencv/opencv_contrib/archive/4.5.2.zip -O opencv_contrib-4.5.2.zip

> unzip opencv-4.5.2.zip

> unzip opencv_contrib-4.5.2.zip

> mkdir opencv-4.5.2/build

> cd opencv-4.5.2/build

9. configure the building setting as follows
> cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D WITH_CUDA=ON \
      -D CUDA_ARCH_PTX="" \
      -D CUDA_ARCH_BIN="5.3,6.2,7.2" \
      -D WITH_CUBLAS=ON \
      -D WITH_LIBV4L=ON \
      -D BUILD_opencv_python3=ON \
      -D BUILD_opencv_python2=OFF \
      -D BUILD_opencv_java=OFF \
      -D WITH_GSTREAMER=OFF \
      -D WITH_GTK=ON \
      -D BUILD_TESTS=OFF \
      -D BUILD_PERF_TESTS=OFF \
      -D BUILD_EXAMPLES=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.5.2/modules \
      ..

10. build opencv with CUDA support (can take some hours)
> make -j4

> sudo make install

11. install pytesseract
> pip3 install pytesseract --user

12. install smbus
> sudo apt-get install python3-smbus

13. install numba dependencies
> wget http://releases.llvm.org/7.0.1/llvm-7.0.1.src.tar.xz

> tar -xvf llvm-7.0.1.src.tar.xz

> cd llvm-7.0.1.src

> mkdir llvm_build_dir

> cd llvm_build_dir/

> cmake ../ -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="ARM;X86;AArch64"

> make -j4

> sudo make install

> cd bin/

> echo "export LLVM_CONFIG=\""`pwd`"/llvm-config\"" >> ~/.bashrc

> echo "alias llvm='"`pwd`"/llvm-lit'" >> ~/.bashrc

> source ~/.bashrc

> pip install llvmlite==0.30.0

14. install numba
> pip install numba==0.46.0
