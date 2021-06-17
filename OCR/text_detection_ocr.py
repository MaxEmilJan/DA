import cv2 as cv
import pytesseract
import numpy as np
from PIL import Image
# definde the PATH to your tesseract sidepackage
pytesseract.pytesseract.tesseract_cmd = r'/home/max/anaconda3/envs/DA/bin/tesseract'

# function to evaluate the detected edges and areas
# def text_detection(img_edges):
#     # finding contours
#     contours, _ = cv.findContours(img_edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
#     number_contour = 0


# finding contours
contours, _ = cv.findContours(img_edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
number_contour = 0

img_box = img.copy()
img_roi = img.copy()

for cnt in contours:
    number_contour = number_contour + 1
    x, y, w, h = cv.boundingRect(cnt)
    area = cv.contourArea(cnt)
    # drawing rectangle box around ROI
    rect = cv.minAreaRect(cnt)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    img_cut = img_roi[y:y+h, x:x+w]
    cv.drawContours(img_cut, [cnt], 0, 255, -1)
    cv.drawContours(img_box,[box], 0, (0,255,0), 2)
    cv.putText(img_box, str(number_contour), (x,y-10), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))

    # thresh the ROI
    _, img_roi_thresh = cv.threshold(img_cut[...,0], 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # extract text
    text = pytesseract.image_to_string(img_roi_thresh)
    print(str(number_contour) + ": " + str(text))
    cv.imshow("ROI fill", img_cut)
    cv.imshow("ROI thresh", img_roi_thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()

# show images
cv.imshow("Image BoundingBoxes", img_box)
cv.imshow("Image Canny", img_edges)
# cv.imshow("Image Fill", img_fill_inv)
# cv.imshow("Image Dilate", img_dil)
cv.waitKey(0)
cv.destroyAllWindows()