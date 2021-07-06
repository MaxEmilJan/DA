import cv2 as cv
import pytesseract
import re
import time
# definde the PATH to your tesseract sidepackage
pytesseract.pytesseract.tesseract_cmd = r'/home/max/anaconda3/envs/DA/bin/tesseract'

# function to evaluate the detected edges and areas
def text_recognition(text_img, img_roi, square):
    startTime = time.time()
    # apply thresholding to the ROI
    _, img_roi_thresh = cv.threshold(img_roi, 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # extract the text which is visible in the ROI
    text_roi = pytesseract.image_to_string(img_roi_thresh)
    # add the text to a string if it contains a "#" symbol followed by 4 digits
    text_digit = re.search(r"#(\d{4})", text_roi)
    if text_digit is not None:
        # only add the digits and not the "#"
        text_img = text_img + text_digit.group()[1:5]
        match = True
        #print("fist attempt: match found -" + text_img + "-")
    else:
        #print("first attempt: no match found")
        # if no match was detected, check if the label is upside down and try again
        # get shape of ROI
        height = img_roi_thresh.shape[0]
        width = img_roi_thresh.shape[1]
        # get center of ROI
        center = (width/2, height/2)
        # get rotation matrix
        M = cv.getRotationMatrix2D(center, 180, 1.0)
        # rotate ROI 180 degrees
        img_rot = cv.warpAffine(img_roi_thresh, M, (width, height))
        # repeat text recognition and pattern extraction
        text_roi = pytesseract.image_to_string(img_rot)
        text_digit = re.search(r"#(\d{4})", text_roi)
        if text_digit is not None:
            # only add the digits and not the "#"
            text_img = text_img + text_digit.group()[1:5]
            match = True
            #print("second attempt: match found -" + text_img + "-")
        else:
            match = False
            #print("second attempt: no match found")
    #cv.imshow("ROI", img_roi)
    #cv.imshow("ROI thresh", img_roi_thresh)
    #cv.waitKey(0)
    #cv.destroyAllWindows()
    return text_img, match