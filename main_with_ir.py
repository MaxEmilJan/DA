import smbus
import sys
import logging
logging.basicConfig(level=logging.WARNING, format='File: %(filename)s, Line: %(lineno)d \nMessage: %(message)s')
import numpy as np
import cv2 as cv
import neoapi
import easyocr
from load_frame import load_frame
from ocr.vignetting_correction.vignetting_correction import vignetting_correction
from ocr.preprocessing import preprocessing
from ocr.edge_detection import canny_edge_detection
from ocr.orientation_correction import orientation_correction
#from ocr.binning import binning
from ocr.text_recognition_gpu import text_recognition_gpu


# used camera parameters:
    # f = 5cm
    # k = 2
    # t = 1,5ms

def main():
    try:
        logging.warning("init...")
        # ---- I2C ----
        # Jetson Nano I2C Bus 0 (SDA Pin 27, SCL Pin 28)
        bus = smbus.SMBus(0)
        # address (must be the same as in the arduino script)
        address = 0x40
        # ---- OCR ----
        # load vignetting_correction_mask.npy to work with this array
        vignett_mask = np.load("OCR/vignetting_correction/vignetting_correction_mask.npy")
        # create the necessary filters for morphologic operations
        filter_close = cv.getStructuringElement(cv.MORPH_RECT, (4,4))
        filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
        # define easyocr reader module
        reader = easyocr.Reader(['en'], gpu=True)
        # create a string to write the recognized text to
        text = ""
        # create a counter variable to count the amount of equal text recognitions in a row
        cnt = 0
        logging.warning("init done")
    except Exception as e:
        logging.error(e)
        sys.exit(1)
        
    try:
        logging.warning("init camera ...")
        # init camera
        camera = neoapi.Cam()
        camera.Connect()
        # a mono cam is used so it is enough to only load a mono channel image
        camera.f.PixelFormat.SetString('Mono8')
        # exposure time set to 1,5 ms
        camera.f.ExposureTime.Set(15000)
        # framerate set to max. 10 FPS
        camera.f.AcquisitionFrameRateEnable.value = True
        camera.f.AcquisitionFrameRate.value = 2
        logging.warning("init camera done")
    except Exception as e:
        logging.error(e)
        sys.exit(1)
            
    #start recording routine
    #cv.namedWindow("press ESC to close", cv.WINDOW_NORMAL)
    logging.warning("ready")
    while camera.IsConnected():
        signal = bus.read_byte(address)
        # if the IR-Sensor detects an obstacle, run the algorithm
        if signal == 1:
            logging.info("running...")
            # save text of previous run
            text_prev = text
            # reset text so it does not append everything detected
            text = ""
            img_raw = camera.GetImage().GetNPArray()
            # cut the edges and grayscale
            img = load_frame(img_raw)
            # call the function to remove the vignetting
            img_corrected = np.uint0(vignetting_correction(img, vignett_mask))
            # call the function to preprocess the image
            img_preprocessed = preprocessing(img_corrected)
            # call the function to detect edges
            img_edges, flag_contours = canny_edge_detection(img_preprocessed, filter_close, filter_dil)
            if flag_contours == True:
                # find contours
                contours, _ = cv.findContours(img_edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                # loop through all the detected edges
                for i in contours:
                    # get area of ROI
                    area = cv.contourArea(i)
                    # filter all found contours which are too small to contain characters
                    if area >= 25000:
                        # deskew ROI
                        img_roi, box = orientation_correction(i, img_corrected)
                        # 2x2 binning the ROI to speed up the OCR
                        #img_roi_bin = np.uint8(binning(img_roi, ((img_roi.shape[0]//2), (img_roi.shape[1]//2))))
                        # text recognition in ROI
                        text, match = text_recognition_gpu(text, img_roi, reader)
                        # draw a box and the detected text to the original image, if a match was found
                        if match == True:
                            box = np.int0(box)
                            # count the amount of equal texts recognized in a row
                            if text == text_prev:
                                cnt += 1
                            # dont reset the counter if no text was recognized, only when another fitting text got recognized
                            elif text_prev == "":
                                pass
                            # if another text which fits the pattern gets recognized, reset the counter
                            else:
                                cnt = 0
                        # if no match was found, do nothing
                        else:
                            pass
                    # if the ROI is too small, do nothing
                    else:
                        pass
            # if no contours were detected, do nothing
            else:
                pass
            # check the contour
            # if the same four digits were recognized in a row, then make it the final result
            if cnt == 4:
                logging.info("text recognition done")
                logging.warning("result: "+str(text))
                cnt = 0
            # if not, continue the recognition
            else:
                pass
        
        # if IR-Sensor does not detect an obstacle, do nothing
        else:
            pass
    # if no camera is connected, print this
    else:
        print("no camera connected")
    return -1
        

if __name__ == '__main__':
    main()
