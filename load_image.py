import cv2 as cv
import logging
import sys

logger = logging.getLogger(__name__)

# function to load an image (will be replaced by the frame from the neoAPI later)
def load_image(name_image):
    try:
        # loading grayscaled image
        img_raw = cv.imread(name_image)[...,0]
        # select ROI and only keep this part
        img_cut = img_raw[300:1075, 150:1790]
        #cv.imwrite("vignetting_correction/test_image.jpg", img_cut)
        logger.info("image loading done")
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    return img_cut

#img = load_image("OCR/1,5ms_k2_7.jpg")
#cv.imwrite("OCR/test_roi.jpg", img)
