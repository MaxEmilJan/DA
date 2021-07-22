import sys
import time
import argparse
import logging
import numpy as np
import cv2 as cv
import neoapi
from easyocr import Reader
from load_image import load_image
from load_frame import load_frame
from vignetting_correction.vignetting_correction import vignetting_correction
from ocr.preprocessing import preprocessing
from ocr.edge_detection import canny_edge_detection
from ocr.orientation_correction import orientation_correction
from ocr.binning import binning
from ocr.text_recognition_easyocr import text_recognition_gpu


# used camera parameters:
    # f = 5cm
    # k = 2
    # t = 1,5ms

def main():
    # command line inputs
    parser = argparse.ArgumentParser(description="Detect the label on a camera.")
    parser.add_argument("mode", choices=["video", "image"], type=str, help="select either video or image mode whether you want to detect text in a live recording or an image")
    parser.add_argument("-n", "--number_image", choices=range(1,39), type=int, default=1, metavar="[1-38]", help="number of image which will be used in image mode") 
    #parser.add_argument("-f", "--file", help="add the path to the image you want to perform text recognition on")
    parser.add_argument("-l", "--logging", action="store_true", help="set this flag to get additional logging informations printed (algorithm will get slower)")
    args = parser.parse_args()
    
    if args.logging == True:
        logging.basicConfig(level=logging.INFO, format='File: %(filename)s, Line: %(lineno)d \nMessage: %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='File: %(filename)s, Line: %(lineno)d \nMessage: %(message)s')
    
    try:
        logging.warning("init...")
        # load vignetting_correction_mask.npy to work with this array
        vignett_mask = np.load("vignetting_correction/vignetting_correction_mask.npy")
        # create the necessary filters for morphologic operations
        filter_close = cv.getStructuringElement(cv.MORPH_RECT, (4,4))
        filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
        # define easyocr reader module
        logging.warning("loading gpu module...")
        reader = easyocr.Reader(['en'], gpu=True)
        # create a string to write the recognized text to
        text = ""
        logging.warning("init done")
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    
    if args.mode == "image":
        # get number of image as command line input
        number_image = str(args.number_image)
        name_img = "images/Dataset_Stripe/1,5ms_k2_" + number_image + ".jpg"
        #name_img = str(args.file)
        # call the function to load the image
        img = load_image(name_img)
        # call the function to remove the vignetting
        img_corrected = np.uint8(vignetting_correction(img, vignett_mask))
        img_rgb = cv.cvtColor(img_corrected, cv.COLOR_GRAY2RGB)
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
                    img_roi_bin = np.uint8(binning(img_roi, ((img_roi.shape[0]//2), (img_roi.shape[1]//2))))
                    # text recognition in ROI (easyocr)
                    text, match = text_recognition_gpu(text, img_roi_bin, reader)
                    # draw a box and the detected text to the original image, if a match was found
                    if match == True:
                        box = np.int0(box)
                        # draw green box
                        cv.drawContours(img_rgb,[box],0,(0,255,0),2)
                        # put recognized text in top left corner
                        cv.putText(img_rgb, text, (25, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0))
                    else:
                        box = np.int0(box)
                        # draw red box
                        cv.drawContours(img_rgb,[box],0,(0,0,255),2)
                else:
                    pass
        else:
            pass
        logging.info("text recognition done")
        # print the recognized text
        logging.warning("recognized text: " + text)
        cv.imshow("press ESC to close", img_rgb)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    elif args.mode == "video":
        try:
            logging.info("init camera ...")
            # init camera
            camera = neoapi.Cam()
            camera.Connect()
            # a mono cam is used so it is enough to only load a mono channel image
            camera.f.PixelFormat.SetString('Mono8')
            # exposure time set to 1,5 ms
            camera.f.ExposureTime.Set(15000)
            # framerate set to max. 10 FPS
            camera.f.AcquisitionFrameRateEnable.value = True
            camera.f.AcquisitionFrameRate.value = 10
            logging.info("init camera done")
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        
        #start recording routine
        while camera.IsConnected():
            startTime = time.time()
            # create a string to write the recognized text to
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
                        img_roi_bin = np.uint8(binning(img_roi, ((img_roi.shape[0]//2), (img_roi.shape[1]//2))))
                        # text recognition in ROI (easyocr)
                        text, match = text_recognition_gpu(text, img_roi_bin, reader)
                    else:
                        pass
            else:
                pass
            logging.info("text recognition done")
            # print the recognized text
            logging.warning("recognized text: " + text)
            logging.info("Runtime: " + str(round(time.time()-startTime, 4)) + "s")
            # plot the result
            img_rgb = cv.cvtColor(img_corrected, cv.COLOR_GRAY2RGB)
            # if a text which matches the pattern got recognized
            if text != "":
                # draw green box around text
                box = np.int0(np.array(box))
                cv.drawContours(img_rgb, [box], 0, (0,255,0), 2)
                # print recognized text in upper left corner
                cv.putText(img_rgb, text, (25,100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0))
                cv.imshow("press ESC to end", img_rgb)
            else:
                # print spareholder to upper left corner
                cv.putText(img_rgb, "----", (25,100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,0,255))
                cv.imshow("press ESC to end", img_rgb)

            # to quit the demonstration press "ESC"
            if cv.waitKey(1) == 27:
                cv.destroyAllWindows()
                break
        else:
            print("no camera connected")
        

if __name__ == '__main__':
    main()
