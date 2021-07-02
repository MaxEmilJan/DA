import numpy as np
import time

def vignetting_correction(img_vignett, correction_mask):
    startTime = time.time()
    # get the size of the image (1920x1200 in this application)
    height, width = img_vignett.shape
    # vignetting-correction by deviding the vignetted image by the correction mask
    img_corrected = img_vignett/correction_mask
    # set every pixel with an intensity above 255 to 255
    for i in range(height):
        for j in range(width):
            if (img_corrected[i,j] >= 255):
                img_corrected[i,j] = 255
            else:
                pass
    print("vignetting_correction: " + str(time.time()-startTime))
    # return the corrected image without vignetting
    return np.uint8(img_corrected)

#vignett_mask = np.load("vignetting_correction_mask.npy")
#img_roi = cv.imread("test_roi.jpg")[...,0]
#img_corrected = vignetting_correction(img_roi, vignett_mask)
#cv.imwrite("test_corrected.jpg", img_corrected)
