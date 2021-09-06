import logging
import sys
import cv2 as cv

logger = logging.getLogger(__name__)

# function to load and reshape a frame
def load_frame(img_raw):
    try:
        # loading grayscaled image
        img_gs = img_raw[...,0]
        # select ROI and only keep this part
        img_cut = img_gs[300:1075, 150:1790]
        logger.info("frame loading done")
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    return img_cut

if __name__=='__main__':
    img = cv.imread("images/Dataset_Stripe/1,5ms_k2_26.jpg")
    img = load_frame(img)
    cv.imwrite("beispiel8.jpg", img)
