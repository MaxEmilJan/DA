import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# loading plain image (white background) to measure vignetting
img_vignett = cv.imread("vignett_500µs.jpg")[:,:,0]
# get the resolution of the image (1920x1200 in this case)
height, width = img_vignett.shape

# normalize each pixel by deviding it by 255
img_mask = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        if (img_vignett[i,j] >= 60):
            img_mask[i,j] = (img_vignett[i,j]/255)
        else:
            img_mask[i,j] = 1

# plot the correction mask
plt.imshow(img_mask, cmap="gray")
plt.colorbar()
plt.show()

# save the mask as an numpy array
np.save('vignetting_correction_mask.npy', img_mask)