import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# loading plain image (white background) to measure vignetting
img_vignett = cv.imread("vignett_1,5ms.jpg")[:,:,0]
# select ROI and only keep this part
img_roi = img_vignett[300:1075, 150:1790]
# get the resolution of the image (1920x1200 in this case)
height, width = img_roi.shape

# normalize each pixel by deviding it by 255
img_mask = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        if (img_roi[i,j] >= 60):
            img_mask[i,j] = (img_roi[i,j]/255)
        else:
            img_mask[i,j] = 1

# plot the correction mask
plt.imshow(img_mask, cmap="gray")
plt.colorbar()
plt.show()
# save the mask as an numpy array
#np.save('vignetting_correction_mask.npy', img_mask)