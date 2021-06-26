import cv2 as cv
import pytesseract
import re
#from edge_detection import canny_edge_detection
# definde the PATH to your tesseract sidepackage
pytesseract.pytesseract.tesseract_cmd = r'/home/max/anaconda3/envs/DA/bin/tesseract'

# function to evaluate the detected edges and areas
def text_recognition(text_img, img_roi, square):
    # apply thresholding to the ROI
    _, img_roi_thresh = cv.threshold(img_roi, 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # extract the text which is visible in the ROI
    text_roi = pytesseract.image_to_string(img_roi_thresh)
    print(text_roi)
    # add the text to a string if it contains a "#" symbol followed by 4 digits
    text_digit = re.search(r"#(\d{4})", text_roi)
    if text_digit is not None:
        # only add the digits and not the "#"
        text_img = text_img + text_digit.group()[1:5]
    else:
        pass
    #cv.imshow("ROI", img_roi)
    #cv.imshow("ROI thresh", img_roi_thresh)
    #cv.waitKey(0)
    #cv.destroyAllWindows()
    return text_img #, img_box