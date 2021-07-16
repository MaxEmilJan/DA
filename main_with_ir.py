import smbus
import sys
import logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: \nFile: %(filename)s, Line: %(lineno)d \nMessage: %(message)s')
import numpy as np
import cv2 as cv
import neoapi
#import easyocr
#from load_image import load_image
from load_frame import load_frame
from OCR.vignetting_correction.vignetting_correction import vignetting_correction
from OCR.preprocessing import preprocessing
from OCR.edge_detection import canny_edge_detection
from OCR.orientation_correction import orientation_correction
#from OCR.binning import binning
from OCR.text_recognition import text_recognition
#from OCR.text_recognition_easyocr import text_recognition_gpu


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
        filter_close = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
        filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
        # define OCR config
        OCR_config = r'-c tessedit_char_whitelist=#1234567890 --psm 6'
        # define easyocr reader module
        #reader = easyocr.Reader(['en'], gpu=True)
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
            #startRun1 = time.time()
            # save text of previous run
            text_prev = text
            # reset text so it does not append everything detected
            text = ""
            img_raw = camera.GetImage().GetNPArray()
            # cut the edges and grayscale
            img = load_frame(img_raw)
            # call the function to remove the vignetting
            img_corrected = np.uint8(vignetting_correction(img, vignett_mask))
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
                        text, match = text_recognition(text, img_roi, OCR_config)
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
            
            # print the recognized text
            #logging.warning("recognized text: " + text)
            #logging.warning("Runtime: " + str(round(time.time()-startTime, 4)) + "s")
            
            # print the result
            #img_rgb = cv.cvtColor(img_corrected, cv.COLOR_GRAY2RGB)
            # if a text which matches the pattern was recognized:
            #if text != "":
                # draw green box
            #    box = np.array(box)
            #    cv.drawContours(img_rgb,[box],0,(0,255,0),2)
                # put recognized text in top left corner
            #    cv.putText(img_rgb, text, (25, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0))
            #    cv.imshow("frame", img_rgb)
            #    print(text)
            # if no matching text was recognized:
            #else:
                # put spareholder in top left corner
            #    cv.putText(img_rgb, "----", (25, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,0,255))
            #    cv.imshow("frame", img_rgb)
            # to quit the demonstration press "ESC"
            #if cv.waitKey(1) == 27:
            #    cv.destroyAllWindows()
            #    break
        
        # if IR-Sensor does not detect an obstacle, do nothing
        else:
            pass
    # if no camera is connected, print this
    else:
        print("no camera connected")
    return -1
        

if __name__ == '__main__':
    main()

#cv.imwrite("output_"+number_image+".jpg", img_rgb)
#cv.imshow("Image", img)
#cv.imshow("Image corrected", img_corrected)
#cv.imshow("img_preprocessed", img_preprocessed)
#cv.imshow("Image edges", img_rgb)

#cv.waitKey(0)
#cv.destroyAllWindows()
