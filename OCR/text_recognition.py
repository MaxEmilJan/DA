import cv2 as cv
import numpy as np
import pytesseract
import re
# definde the PATH to your tesseract sidepackage
pytesseract.pytesseract.tesseract_cmd = r'/home/max/anaconda3/envs/DA/bin/tesseract'

# function to evaluate the detected edges and areas
def text_recognition(text_img, img_raw, img_edges):
    # finding contours
    contours, _ = cv.findContours(img_edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    number_contour = 0
    # make a copy of the original image to cut out the ROI and perform the text recognition with it
    img_copy = img_raw.copy()
    
    # this copy is only needed if you want to display the detected ROIs within the original image
    img_box = img_raw.copy()
    
    # evaulate every ROI found
    for cnt in contours:
        number_contour = number_contour + 1
        # get size and position of ROI
        x, y, w, h = cv.boundingRect(cnt)
        # get area of ROI
        area = cv.contourArea(cnt)
        # filter all found contours which are too small to contain characters
        if area >= 5000:
            # cut ROI out of original image
            img_roi = np.uint8(img_copy[y:y+h, x:x+w])
        
            # this can be used to plot an additional image where every ROI is marked with a green box
            # to display this: cv.imshow("Image BoundingBox", img_box)
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            cv.drawContours(img_box,[box], 0, (0,255,0), 2)
            cv.putText(img_box, str(number_contour), (x,y-10), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
        
            # apply thresholding to the ROI
            _, img_roi_thresh = cv.threshold(img_roi, 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            # extract the text which is visible in the ROI
            text_roi = pytesseract.image_to_string(img_roi_thresh)
            # add the text to a string if it contains a "#" symbol followed by 4 digits
            # if "#" in text_roi:
            #     text_img = text_img + text_roi + "\n"
            # else:
            #     pass
            text_digit = re.search(r"#(\d{4})", text_roi)
            if text_digit is not None:
                text_img = text_img + text_digit.group()[1:5]
            else:
                pass
            #cv.imshow("ROI", img_roi)
            #cv.imshow("ROI thresh", img_roi_thresh)
            #cv.waitKey(0)
            #cv.destroyAllWindows()
        else:
            pass
        ## print the result
        #print(str(number_contour) + ": " + str(text_img))
    #cv.imshow("Image BoundingBox", img_box)
    #cv.waitKey(0)
    #cv.destroyAllWindows()
    return text_img, img_box