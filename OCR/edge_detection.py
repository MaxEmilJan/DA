import cv2 as cv
import numpy as np

# function to detect closed edges in the image by applying the canny edge detection methode
def canny_edge_detection(img_preprocessed):
    # basic canny edge detection
    img_preprocessed = np.uint8(img_preprocessed)
    img_canny = cv.Canny(img_preprocessed, 150, 200, apertureSize=3, L2gradient=True)
    # mellow closing the image to close edges with small gaps
    filter_close_1 = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    img_close_1 = cv.morphologyEx(img_canny, cv.MORPH_CLOSE, filter_close_1)
    # only keep closed edges
    img_fill = img_close_1.copy()
    h_img, w_img = img_fill.shape[:2]
    mask_fill = np.zeros((h_img + 2, w_img + 2), dtype=np.uint8)
    cv.floodFill(img_fill, mask_fill, (0,0), 255)
    img_fill_inv = cv.bitwise_not(img_fill)
    # OPTIONAL open image to remove very small parts
    #filter_open = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
    #img_open = cv.morphologyEx(img_fill_inv, cv.MORPH_OPEN, filter_open)
    # dilation (thicken the edges)
    filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))
    img_dil = cv.dilate(img_fill_inv, filter_dil, iterations=1)
    # close image to fill holes inside the edges
    filter_close_2 = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
    img_close_2 = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, filter_close_2)
    return img_close_2