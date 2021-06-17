import numpy as np
import cv2 as cv
from load_image import load_image
from OCR.vignetting_correction.vignetting_correction import vignetting_correction
from OCR.preprocessing import preprocessing
from OCR.edge_detection import canny_edge_detection
from OCR.text_recognition import text_recognition

# used camera parameters:
    # f = 5cm
    # k = 2
    # t = 12ms
  
# select a test image
position_light = "unten"
time_shutter = "12"
number_image = "1"
name_img = "images/Streifen, k=2/" + position_light + "_" + time_shutter + "ms_" + number_image + ".jpg"

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
# call the function to recognize and return the contained text
text, img_box = text_recognition(text, img_corrected, img_edges)

# print the recognized text
print(text)
print("Done")

#cv.imshow("Image", img)
cv.imshow("Image corrected", img_corrected)
#cv.imshow("Image preprocessed", img_preprocessed)
cv.imshow("Image edges", img_edges)
cv.imshow("Image ROIs", img_box)
cv.waitKey(0)
cv.destroyAllWindows()