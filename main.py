import numpy as np
import cv2 as cv
from load_image import load_image
from OCR.vignetting_correction.vignetting_correction import vignetting_correction
from OCR.preprocessing import preprocessing
from OCR.edge_detection import canny_edge_detection
from OCR.text_recognition import text_recognition
from OCR.orientation_correction import orientation_correction

# used camera parameters:
    # f = 5cm
    # k = 2
    # t = 1,5ms
  
# select a test image (1 to 10)
number_image = "1"
name_img = "images/Dataset_Stripe/1,5ms_k2_" + number_image + ".jpg"

# load vignetting_correction_mask.npy to work with this array
vignett_mask = np.load("OCR/vignetting_correction/vignetting_correction_mask.npy")
# create the necessary filters for morphologic operations
filter_close = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
# create a string to write the recognized text to
text = ""

# call the function to load the image
img = load_image(name_img)
# call the function to remove the vignetting
img_corrected = vignetting_correction(img, vignett_mask)
img_rgb = cv.cvtColor(img_corrected, cv.COLOR_GRAY2RGB)
# call the function to preprocess the image
img_preprocessed = preprocessing(img_corrected)
# call the function to detect edges
img_edges, _ = canny_edge_detection(img_preprocessed, filter_close, filter_dil)
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
            # draw green box
            cv.drawContours(img_rgb,[box],0,(0,255,0),2)
            # put recognized text in top left corner
            cv.putText(img_rgb, text, (25, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0))
        else:
            pass
    else:
        pass

# print the recognized text
print(text)
print("Done")

#cv.imshow("Image", img)
#cv.imshow("Image corrected", img_corrected)
#cv.imshow("img_preprocessed", img_preprocessed)
cv.imshow("Image edges", img_rgb)
cv.waitKey(0)
cv.destroyAllWindows()