import cv2 as cv
import pytesseract
import re
import logging 
import sys
# definde the PATH to your tesseract sidepackage
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

logger = logging.getLogger(__name__)

# function to evaluate the detected edges and areas
def text_recognition_cpu(text_img, img_roi, custom_config):
    try:
        # apply thresholding to the ROI
        _, img_roi_thresh = cv.threshold(img_roi, 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        # extract the text which is visible in the ROI
        text_roi = pytesseract.image_to_string(img_roi_thresh, config=custom_config)
        # add the text to a string if it contains a "#" symbol followed by 4 digits
        text_digit = re.search(r"#(\d{4})", text_roi)
        if text_digit is not None:
            # only add the digits and not the "#"
            text_img = text_img + text_digit.group()[1:5]
            match = True
        else:
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
            text_roi = pytesseract.image_to_string(img_rot, config=custom_config)
            text_digit = re.search(r"#(\d{4})", text_roi)
            if text_digit is not None:
                # only add the digits and not the "#"
                text_img = text_img + text_digit.group()[1:5]
                match = True
            else:
                match = False
        #cv.imshow("ROI", img_roi)
        #cv.imshow("ROI thresh", img_roi_thresh)
        #cv.waitKey(0)
        #cv.destroyAllWindows()
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    return text_img, match
