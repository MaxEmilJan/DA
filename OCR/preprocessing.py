import cv2 as cv
import logging
import sys

logger = logging.getLogger(__name__)

# function to preprocess the image
def preprocessing(img):
    try:
        # blur the image to reduce noise (low pass filter)
        img_blur = cv.GaussianBlur(img, (11,11), 0)
        logger.info("preprocessing done")
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    return img_blur

#img_corrected = cv.imread("vignetting_correction/test_corrected.jpg")[...,0]
#img_blur = preprocessing(img_corrected)
#cv.imwrite("vignetting_correction/test_blur.jpg", img_blur)