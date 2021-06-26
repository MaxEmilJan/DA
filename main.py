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
    # t = 12ms
  
# select a test image (1 to 10)
number_image = "6"
name_img = "images/Streifen_2,8/3ms_2,8_" + number_image + ".jpg"

# load vignetting_correction_mask.npy to work with this array
vignett_mask = np.load("OCR/vignetting_correction/vignetting_correction_mask.npy")
# create a string to write the recognized text to
text = ""

# call the function to load the image
img, height, width = load_image(name_img)
# call the function to remove the vignetting
img_corrected = vignetting_correction(img, vignett_mask)
# call the function to preprocess the image
img_preprocessed = preprocessing(img_corrected)
# call the function to detect edges
img_edges = canny_edge_detection(img_preprocessed)
# find contours
contours, _ = cv.findContours(img_edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# loop through all the detected edges
for i in contours:
    # get area of ROI
    area = cv.contourArea(i)
    # filter all found contours which are too small to contain characters
    if area >= 5000:
        # deskew ROI
        img_roi, square = orientation_correction(i, img_corrected)
        # text recognition in ROI
        text = text_recognition(text, img_roi, square)
    else:
        pass

# print the recognized text
print(text)
print("Done")

#cv.imshow("Image", img)
#cv.imshow("Image corrected", img_corrected)
#cv.imshow("Image preprocessed", img_preprocessed)
#cv.imshow("Image edges", img_edges)
#cv.imshow("Image ROIs", img_box)
#cv.waitKey(0)
#cv.destroyAllWindows()