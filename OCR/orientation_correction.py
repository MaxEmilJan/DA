import cv2 as cv
import numpy as np

def orientation_correction(cnt, img_copy):
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
    if width > height:
        # if width > height then P0 is in top left position (0,0)
        dst_pts = np.array([[0,0], [width-1,0], [width-1,height-1], [0,height-1]], dtype="float32")
        # get the rotation-matrix
        M = cv.getPerspectiveTransform(src_pts, dst_pts)
        # multiply img-matix with rotation-matrix to obtain corrected image
        img_rot = cv.warpPerspective(img_copy, M, (width, height))
        square = False
    elif width < height:
        # if width < height P0 is in bottom left position --> P1 is top left (0,0)
        dst_pts = np.array([[0,width-1], [0,0], [height-1,0], [height-1,width-1]], dtype="float32")
        # get the rotation-matrix
        M = cv.getPerspectiveTransform(src_pts, dst_pts)
        # multiply img-matix with rotation-matrix to obtain corrected image
        img_rot = cv.warpPerspective(img_copy, M, (height, width))
        square = False
    else:
        # if the roi is square, any orientation could be possible
        # any rotation must be checked later in order to recognize the text
        dst_pts = np.array([[0,0], [width-1,0], [width-1,height-1], [0,height-1]], dtype="float32")
        # get the rotation-matrix
        M = cv.getPerspectiveTransform(src_pts, dst_pts)
        # multiply img-matix with rotation-matrix to obtain corrected image
        img_rot = cv.warpPerspective(img_copy, M, (width, height))
        square = True
    return img_rot, square, box