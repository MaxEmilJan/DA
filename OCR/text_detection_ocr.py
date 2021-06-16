import cv2 as cv
import pytesseract
import numpy as np
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'/home/max/anaconda3/envs/DA/bin/tesseract'

#focal_length = "5cm"
position_light = "rechts_links"
time_shutter = "12"
number_image = "5"

# loading grayscaled image
img = cv.imread("images/Ring, k=2/" + position_light + "_" + time_shutter + "ms_" + number_image + ".jpg")
# blur the image to reduce noise
img_blur = cv.GaussianBlur(img[...,0], (11,11), 0)
# Canny Edge Detection
img_canny = cv.Canny(img_blur, 150, 200, apertureSize=3, L2gradient=True)
# mellow closing to close edges
filter_close_1 = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
img_close_1 = cv.morphologyEx(img_canny, cv.MORPH_CLOSE, filter_close_1)
# only keep closed edges
img_fill = img_close_1.copy()
h_img, w_img = img_fill.shape[:2]
mask_fill = np.zeros((h_img + 2, w_img + 2), dtype=np.uint8)
cv.floodFill(img_fill, mask_fill, (0,0), 255)
img_fill_inv = cv.bitwise_not(img_fill)
# dilation
filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
img_dil = cv.dilate(img_fill_inv, filter_dil, iterations=1)
# open image to fill holes
filter_close_2 = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
img_close_2 = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, filter_close_2)
# finding contours
contours, _ = cv.findContours(img_close_2, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

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
cv.imshow("Image Canny", img_canny)
cv.imshow("Image Fill", img_fill_inv)
cv.imshow("Image Dilate", img_dil)
cv.waitKey(0)
cv.destroyAllWindows()