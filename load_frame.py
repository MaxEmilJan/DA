import logging
import sys

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

#img, height, width = load_image("images/Streifen_2,8/3ms_2,8_1.jpg")
#cv.imwrite("test_roi.jpg", img)