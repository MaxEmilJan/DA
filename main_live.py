import neoapi
import numpy as np
import cv2 as cv
from load_image_live import load_image
from OCR.vignetting_correction.vignetting_correction import vignetting_correction
from OCR.preprocessing import preprocessing
from OCR.edge_detection import canny_edge_detection
from OCR.text_recognition import text_recognition
from OCR.orientation_correction import orientation_correction

# used camera parameters:
    # f = 5,5cm
    # k = 2
    # t = 1,5ms

# load vignetting_correction_mask.npy to work with this array
vignett_mask = np.load("OCR/vignetting_correction/vignetting_correction_mask.npy")
# create the necessary filters for morphologic operations
filter_close = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
# create a string to write the recognized text to
text = ""

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

# start recording routine
cv.namedWindow("frame", cv.WINDOW_NORMAL)
while camera.IsConnected():
    # create a string to write the recognized text to
    text = ""
    img_raw = camera.GetImage().GetNPArray()
    # cut the edges and grayscale
    img = load_image(img_raw)
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
                img_roi, square, box = orientation_correction(i, img_corrected)
                # text recognition in ROI
                text, match = text_recognition(text, img_roi, square)
                # draw a box and the detected text to the original image, if a match was found
                if match == True:
                    box = np.int0(box)
                else:
                    pass
            else:
                pass
    else:
        pass
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
        #print(text)
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