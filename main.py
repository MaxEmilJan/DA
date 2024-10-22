import sys
import logging
logging.basicConfig(level=logging.WARNING, format='File: %(filename)s, Line: %(lineno)d \nMessage: %(message)s')
import numpy as np
import cv2 as cv
import neoapi
import easyocr
import smbus

from load_frame import load_frame
from vignetting_correction.vignetting_correction import vignetting_correction
from ocr.preprocessing import gaussian_blur
from ocr.edge_detection import canny_edge_detection
from ocr.orientation_correction import orientation_correction
from ocr.binning import binning
from ocr.text_recognition_gpu import text_recognition_gpu

from PyQt5.QtCore import QRect, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView, QWidget
from PyQt5.QtGui import QFont, QPixmap, QImage

# used camera parameters:
    # f = 5cm
    # k = 2
    # t = 15ms


# Thread do the video recording an image processing
class VideoThread(QThread):
    # create the signal which passes the processed frame
    change_pixmap_signal = pyqtSignal(np.ndarray)
    # create the signal which passes the detected camera ID
    change_camID_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        # create an empty string to write the recognized text to
        self.text = ""
        # create a counter variable
        self.cnt = 0
        # initialize the camera through the Baumer neoAPI
        try:
            logging.warning("init camera ...")
            # init camera
            self.camera = neoapi.Cam()
            self.camera.Connect()
            # a mono cam is used so it is enough to only load a mono channel image
            self.camera.f.PixelFormat.SetString('Mono8')
            # exposure time set to 1,5 ms
            self.camera.f.ExposureTime.Set(15000)
            # framerate set to max. 10 FPS
            self.camera.f.AcquisitionFrameRateEnable.value = True
            self.camera.f.AcquisitionFrameRate.value = 10
            logging.warning("init done")
        except Exception as e:
            logging.error(e)
            sys.exit(1)

    def run(self):
        logging.warning("VideoThread running")
        # capture from web cam
        while self._run_flag:
            signal = bus.read_byte(address)
            # if the IR-Sensor detects an obstacle, run the image processing
            #if signal == 1:
            # save text of previous run
            text_prev = self.text
            # reset text so it does not append everything detected
            self.text = ""
            # get the frame from the camera
            cv_img = self.camera.GetImage().GetNPArray()
            # cut the edges and grayscale
            cv_img = load_frame(cv_img)
            # call the function to remove the vignetting
            cv_img_corrected = np.uint8(vignetting_correction(cv_img, vignett_mask))
            img_rgb = cv.cvtColor(cv_img_corrected, cv.COLOR_GRAY2RGB)
            # call the function to preprocess the image
            cv_img = gaussian_blur(cv_img_corrected)
            # call the function to detect edges
            cv_img, flag_contours = canny_edge_detection(cv_img, filter_close, filter_dil)
            if flag_contours == True:
                # find contours
                contours, _ = cv.findContours(cv_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                # loop through all the detected edges
                for i in contours:
                    # get area of ROI
                    area = cv.contourArea(i)
                    # filter all found contours which are too small to contain characters
                    if area >= 25000:
                        # deskew ROI
                        cv_img, box = orientation_correction(i, cv_img_corrected)
                        # 2x2 binning the ROI to speed up the OCR
                        cv_img = np.uint8(binning(cv_img, ((cv_img.shape[0]//2), (cv_img.shape[1]//2))))
                        # text recognition with easyocr
                        self.text, match = text_recognition_gpu(self.text, cv_img, reader)
                        # if a match is found, evaluate its continuity
                        if match == True:
                            box_match = box
                            # count the amount of equal texts recognized in a row
                            if self.text == text_prev:
                                self.cnt += 1
                            # if another text which fits the pattern gets recognized, reset the counter
                            else:
                                self.cnt = 0
                        # if no match was found, do nothing
                        else:
                            pass
                    # if the ROI is too small, do nothing
                    else:
                        pass
            # if no contours were detected, do nothing
            else:
                pass
            # print the results
            # if a text which matches the pattern was recognized
            if self.text != "":
                # draw green box around matching ROI and print text in upper left corner
                cv.putText(img_rgb,self.text,(25, 100),cv.FONT_HERSHEY_SIMPLEX,3,(0,255,0),2)
                cv.drawContours(img_rgb,np.int32([box_match]),0,(0,255,0),3)
            # if no match was found
            else:
                # put spareholder in top left corner
                cv.putText(img_rgb,"----",(25,100),cv.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2)
                self.change_camID_signal.emit("----")
            # check the counter
            # if the same four digits were recognized in a row, then make it the final result and set the counter back to 0
            if self.cnt == 3:
                logging.info("text recognition done")
                logging.warning("result: "+str(self.text))
                self.change_camID_signal.emit(self.text)
                self.cnt = 0
            # if not, continue the recognition
            else:
                pass
            # pass the result to the Gui class
            self.change_pixmap_signal.emit(img_rgb)
            # if IR-Sensor does not detect an obstacle, show the "idle" image
            #else:
            #    # show the idle image 
            #    img_rgb = np.zeros((775,1640))
            #    self.change_pixmap_signal.emit(img_rgb)
        # if no camera is connected, print this
        else:
            logging.error("no camera connected")
            img_rgb = np.zeros((775,1640))
            cv.putText(img_rgb,"no camera connected",(100,100),cv.FONT_HERSHEY_SIMPLEX,3,(255,255,255),2)
            self.change_pixmap_signal.emit(img_rgb)

    # this methode is executed when the GUI gets closed
    def stop(self):
        # Sets run flag to False and waits for thread to finish
        logging.warning("waiting for the video thread to finish")
        self._run_flag = False
        self.wait()
        logging.warning("video thread closed and camera released")
        

# this class created the GUI
class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('rent a cam')
        self.setGeometry(0, 0, 900, 550)
        # create the labels
        # titel
        self.label_titel = QLabel(self)
        self.label_titel.setGeometry(QRect(25, 5, 171, 51))
        self.label_titel.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_titel.setObjectName("label_titel")
        self.label_titel.setText("rent a cam")
        # subtitel
        self.label_cam = QLabel(self)
        self.label_cam.setGeometry(QRect(25, 390, 171, 51))
        self.label_cam.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_cam.setObjectName("label_cam")
        self.label_cam.setText("Camera ID:")
        # shows recognized number of the detected camera
        self.label_camnumber = QLabel(self)
        self.label_camnumber.setGeometry(QRect(235, 390, 91, 51))
        self.label_camnumber.setFont(QFont("Arial", 30, QFont.Bold))
        self.label_camnumber.setObjectName("label_camnumber")
        self.label_camnumber.setText("----")
        # subtitel
        self.label_list = QLabel(self)
        self.label_list.setGeometry(QRect(800, 5, 100, 51))
        self.label_list.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_list.setObjectName("label_list")
        self.label_list.setText("User:")
        # statusbar
        self.label_status = QLabel(self)
        self.label_status.setGeometry(QRect(25, 540, 905, 25))
        self.label_status.setAlignment(Qt.AlignRight)
        self.label_status.setFont(QFont("Arial", 15, QFont.Bold))
        self.label_status.setObjectName("label_status")
        self.label_status.setText("idle")
        # buttons to rent, return, repeat or cancel (30,100,30),(100,30,30),(150,85,0),(30,30,30)
        self.button_rent = QPushButton(self)
        self.button_rent.setEnabled(False)
        self.button_rent.setGeometry(QRect(25, 440, 335, 90))
        self.button_rent.setStyleSheet("background-color: rgb(30, 30, 30); font: 20pt \"Noto Sans\";")
        self.button_rent.setObjectName("button_rent")
        self.button_rent.setText("rent")
        self.button_rent.clicked.connect(self.rentclicked_event)
        self.button_return = QPushButton(self)
        self.button_return.setEnabled(False)
        self.button_return.setGeometry(QRect(380, 440, 335, 90))
        self.button_return.setStyleSheet("background-color: rgb(30, 30, 30); font: 20pt \"Noto Sans\";")
        self.button_return.setObjectName("button_return")
        self.button_return.setText("return")
        self.button_return.clicked.connect(self.returnclicked_event)
        # screen to display the output image of main.py
        self.screen = QLabel(self)
        self.screen.setObjectName("screen")
        self.screen.setGeometry(25, 50, 690, 326)
        # list to choose user
        self.list = QListWidget(self)
        self.list.setGeometry(QRect(800, 50, 130, 480))
        self.list.setSortingEnabled(True)
        self.list.setDragEnabled(False)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setObjectName("list")
        item1 = QListWidgetItem()
        font = QFont()
        font.setPointSize(20)
        item1.setFont(font)
        item1.setText("---select---")
        self.list.addItem(item1)
        item2 = QListWidgetItem()
        item2.setFont(font)
        item2.setText("asb")
        self.list.addItem(item2)
        item3 = QListWidgetItem()
        item3.setFont(font)
        item3.setText("mbec")
        self.list.addItem(item3)
        item4 = QListWidgetItem()
        item4.setFont(font)
        item4.setText("trc")
        self.list.addItem(item4)
        item5 = QListWidgetItem()
        item5.setFont(font)
        item5.setText("srec")
        self.list.addItem(item5)
        item6 = QListWidgetItem()
        item6.setFont(font)
        item6.setText("lli")
        self.list.addItem(item6)
        item7 = QListWidgetItem()
        item7.setFont(font)
        item7.setText("jdan")
        self.list.addItem(item7)
        item8 = QListWidgetItem()
        item8.setFont(font)
        item8.setText("hkat")
        self.list.addItem(item8)
        item9 = QListWidgetItem()
        item9.setFont(font)
        item9.setText("sdan")
        self.list.addItem(item9)
        item10 = QListWidgetItem()
        item10.setFont(font)
        item10.setText("pkar")
        self.list.addItem(item10)
        item11 = QListWidgetItem()
        item11.setFont(font)
        item11.setText("jdi")
        self.list.addItem(item11)
        self.list.setCurrentItem(item1)
        self.list.itemClicked.connect(self.listClicked_event)
        
        # create the video capture thread
        self.thread = VideoThread()
        # connect its first signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # connect its second signal to the update_camID slot
        self.thread.change_camID_signal.connect(self.update_camID)
        # start the thread
        self.thread.start()
        
    # this methode closes the video thread, when the GUI gets closed
    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
        
    # this methode loads the processed frame from the video thread, so it is available to the GUI class to display it
    @pyqtSlot(np.ndarray)
    def update_image(self, img_rgb):
        # convert the opencv image to a QPixmap format to display it
        qt_img = self.convert_cv_qt(img_rgb)
        # Updates the screen with the new image
        self.screen.setPixmap(qt_img)
    
    # this methode converts the processed opencv frame to a format which is displayable by pyqt5
    def convert_cv_qt(self, img_rgb):
        # Convert from an opencv image to QPixmap
        convert_to_Qt_format = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], QImage.Format_RGB888).rgbSwapped()
        # scale the image
        p = convert_to_Qt_format.scaled(690, 326, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    # this methode updates the label which shows the detected camera ID
    @pyqtSlot(str)
    def update_camID(self, cam_ID):
        # Updates the label with the detected ID
        self.label_camnumber.setText(cam_ID)
        if cam_ID != "----" and self.list.currentRow() != 0:
            self.button_rent.setStyleSheet("background-color: rgb(50, 120, 50); font: 20pt \"Noto Sans\";")
            self.button_rent.setEnabled(True)
            self.button_return.setStyleSheet("background-color: rgb(120, 50, 50); font: 20pt \"Noto Sans\";")
            self.button_return.setEnabled(True)
        else:
            self.button_rent.setStyleSheet("background-color: rgb(30, 30, 30); font: 20pt \"Noto Sans\";")
            self.button_rent.setEnabled(False)
            self.button_return.setStyleSheet("background-color: rgb(30, 30, 30); font: 20pt \"Noto Sans\";")
            self.button_return.setEnabled(False)
            self.label_status.setStyleSheet("color: rgb(0, 0, 0);")
            self.label_status.setText("idle")

    # the event handling functions which the buttons are connected to
    def listClicked_event(self):
        # currently just a placeholder function
        # connection to the Baumer databank should get implemented here
        pass
        
    def rentclicked_event(self):
        # if a camera was detected and the "rent" button is pushed, do this
        if self.label_camnumber.text() != "----" and self.list.selectedItems()[0].text() != "---select---":
            # the detected camera ID and the User is printed
            self.label_status.setStyleSheet("color: rgb(30, 100, 30);")
            self.label_status.setText("Camera " + self.label_camnumber.text() + " rented by " + self.list.selectedItems()[0].text() + ".")
            # the connection to the Baumer databank should get implemented here
        # if no user was selected
        else:
            # print a warning
            self.label_status.setStyleSheet("color: rgb(100, 30, 30);")
            self.label_status.setText("Please select your user shortcut first!")
            
        
    def returnclicked_event(self):
        # if a camera was detected and the "return" button is pushed, do this
        if self.label_camnumber.text() != "----" and self.list.selectedItems()[0].text() != "---select---":
            # the detected camera ID and the User is printed
            self.label_status.setStyleSheet("color: rgb(30, 100, 30);")
            self.label_status.setText("Camera " + self.label_camnumber.text() + " returned by " + self.list.selectedItems()[0].text() + ".")
            # the connection to the Baumer databank should get implemented here
        # if no user was selected
        else:
            # print a warning
            self.label_status.setStyleSheet("color: rgb(100, 30, 30);")
            self.label_status.setText("Please select your user shortcut first!")

if __name__ == '__main__':
    try:
        logging.warning("initializing I2C bus...")
        # ---- I2C ----
        # Jetson Nano I2C Bus 0 (SDA Pin 27, SCL Pin 28)
        bus = smbus.SMBus(0)
        # address (must be the same as in the arduino script)
        address = 0x40
        # ---- OCR ----
        logging.warning("creating image filters... [openCV]")
        # load vignetting_correction_mask.npy to work with this array
        vignett_mask = np.load("vignetting_correction/vignetting_correction_mask.npy")
        # create the necessary filters for morphologic operations
        filter_close = cv.getStructuringElement(cv.MORPH_RECT, (4,4))
        filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
        # preload numbas just in time compiler
        logging.warning("loading just-in-time-compiler... [numba]")
        img_init = cv.imread("images/img_init.jpg")[...,0]
        vignetting_correction(img_init, vignett_mask)
        # define easyocr reader module
        logging.warning("loading gpu module for ocr... [easyocr]")
        reader = easyocr.Reader(['en'], gpu=True)
        reader.recognize(img_init, detail=0)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
        
    logging.warning("starting GUI")
    app = QApplication(sys.argv)
    window = Gui()
    window.showMaximized()
    sys.exit(app.exec())
