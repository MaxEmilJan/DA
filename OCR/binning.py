from numba import jit
#import numpy as np
#import cv2 as cv

# use a just-in-time compilation to speed up the binning
jit(nopython=True)
def binning(array, new_shape):
    print(array.shape)
    array = array[:(array.shape[0] // 2)*2, :(array.shape[1] // 2)*2]
    print(array.shape)
    shape = (new_shape[0], array.shape[0] // new_shape[0],
             new_shape[1], array.shape[1] // new_shape[1])
    return array.reshape(shape).mean(-1).mean(1)

# load image and greyscale (1200, 1920)
#img = cv.imread("roi.jpg")[...,0]
# 2x2 binning by reshaping the numpy array and calculate the mean along the reshaped axes
#img_bin = np.uint8(binning(img, ((img.shape[0]//2), (img.shape[1]//2))))

#cv.imshow("original", img)
#cv.imshow("binned", img_bin)
#cv.waitKey(0)
#cv.destroyAllWindows()