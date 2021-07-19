import cv2 as cv
import numpy as np
import logging
import sys

logger = logging.getLogger(__name__)

def orientation_correction(cnt, img_copy):
    try:
        # get center point, width, length and rotation angle of minimal box around contour
        roi = cv.minAreaRect(cnt)
        # get coordinates of corners (P0, P1, P2, P3)
        box = cv.boxPoints(roi)
        src_pts = box.astype("float32")
        # get width of box (between P0 and P1)
        width = int(roi[1][1])
        # get height of box (between P1 and P2)
        height = int(roi[1][0])
        # check if width is larger than height or opposite
        if width >= height:
            # if width > height then P0 is in top left position (0,0)
            dst_pts = np.array([[0,0], [width-1,0], [width-1,height-1], [0,height-1]], dtype="float32")
            # get the rotation-matrix
            M = cv.getPerspectiveTransform(src_pts, dst_pts)
            # multiply img-matix with rotation-matrix to obtain corrected image
            img_rot = cv.warpPerspective(img_copy, M, (width, height))
        elif width < height:
            # if width < height P0 is in bottom left position --> P1 is top left (0,0)
            dst_pts = np.array([[0,width-1], [0,0], [height-1,0], [height-1,width-1]], dtype="float32")
            # get the rotation-matrix
            M = cv.getPerspectiveTransform(src_pts, dst_pts)
            # multiply img-matix with rotation-matrix to obtain corrected image
            img_rot = cv.warpPerspective(img_copy, M, (height, width))
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    return img_rot, box