import sys
import time
import argparse
import logging
import numpy as np
import cv2 as cv
import neoapi
from load_image import load_image
from load_frame import load_frame
from OCR.vignetting_correction.vignetting_correction import vignetting_correction
from OCR.preprocessing import preprocessing
from OCR.edge_detection import canny_edge_detection
from OCR.text_recognition import text_recognition
from OCR.orientation_correction import orientation_correction

# used camera parameters:
    # f = 5cm
    # k = 2
    # t = 1,5ms

def main():
    # command line inputs
    parser = argparse.ArgumentParser(description="Detect the label on a camera.")
    parser.add_argument("mode", choices=["video", "image"], type=str, help="select either video or image mode whether you want to detect text in a live recording or an image")
    parser.add_argument("-n", "--number_image", choices=range(1,39), type=int, default=1, metavar="[1-38]", help="number of image which will be used in image mode")
    parser.add_argument("-l", "--logging", action="store_true", help="set this flag to get additional logging informations printed (algorithm will get slower)")
    args = parser.parse_args()
    
    if args.logging == True:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: \nFile: %(filename)s, Line: %(lineno)d \nMessage: %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s: \nFile: %(filename)s, Line: %(lineno)d \nMessage: %(message)s')
    
    startTime = time.time()
    try:
        logging.info("init...")
        # load vignetting_correction_mask.npy to work with this array
        vignett_mask = np.load("OCR/vignetting_correction/vignetting_correction_mask.npy")
        # create the necessary filters for morphologic operations
        filter_close = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
        filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
        # define OCR config
        OCR_config = r'-c tessedit_char_whitelist=#1234567890 --psm 6'
        # create a string to write the recognized text to
        text = ""
        logging.info("init done")
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    
    if args.mode == "image":
        # get number of image as command line input
        number_image = str(args.number_image)
        name_img = "images/Dataset_Stripe/1,5ms_k2_" + number_image + ".jpg"
        # call the function to load the image
        img = load_image(name_img)
        # call the function to remove the vignetting
        img_corrected = np.uint8(vignetting_correction(img, vignett_mask))
        img_rgb = cv.cvtColor(img_corrected, cv.COLOR_GRAY2RGB)
        # print debug info:
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
                    # text recognition in ROI
                    text, match = text_recognition(text, img_roi, OCR_config)
                    # draw a box and the detected text to the original image, if a match was found
                    if match == True:
                        box = np.int0(box)
                        # draw green box
                        cv.drawContours(img_rgb,[box],0,(0,255,0),2)
                        # put recognized text in top left corner
                        cv.putText(img_rgb, text, (25, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0))
                    else:
                        pass
                else:
                    pass
        else:
            pass
        logging.info("text recognition done")
        # print the recognized text
        logging.warning("recognized text: " + text)
        logging.warning("Runtime: " + str(round(time.time()-startTime, 4)) + "s")
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
        cv.namedWindow("press ESC to close", cv.WINDOW_NORMAL)
        while camera.IsConnected():
            #startRun1 = time.time()
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
                        # text recognition in ROI
                        text, match = text_recognition(text, img_roi, OCR_config)
                        # draw a box and the detected text to the original image, if a match was found
                        if match == True:
                            box = np.int0(box)
                        else:
                            pass
                    else:
                        pass
            else:
                pass
            logging.info("text recognition done")
            # print the recognized text
            logging.warning("recognized text: " + text)
            logging.warning("Runtime: " + str(round(time.time()-startTime, 4)) + "s")
            
            # print the result
            img_rgb = cv.cvtColor(img_corrected, cv.COLOR_GRAY2RGB)
            # if a text which matches the pattern was recognized:
            if text != "":
                # draw green box
                box = np.array(box)
                cv.drawContours(img_rgb,[box],0,(0,255,0),2)
                # put recognized text in top left corner
                cv.putText(img_rgb, text, (25, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0))
                cv.imshow("frame", img_rgb)
                print(text)
            # if no matching text was recognized:
            else:
                # put spareholder in top left corner
                cv.putText(img_rgb, "----", (25, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,0,255))
                cv.imshow("frame", img_rgb)
            # to quit the demonstration press "ESC"
            if cv.waitKey(1) == 27:
                cv.destroyAllWindows()
                break
        else:
            print("no camera connected")
        

if __name__ == '__main__':
    main()

#cv.imwrite("output_"+number_image+".jpg", img_rgb)
#cv.imshow("Image", img)
#cv.imshow("Image corrected", img_corrected)
#cv.imshow("img_preprocessed", img_preprocessed)
#cv.imshow("Image edges", img_rgb)

#cv.waitKey(0)
#cv.destroyAllWindows()