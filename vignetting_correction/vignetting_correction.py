import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# loading image with object to test the vignetting correction
img_test = cv.imread("test_4.jpg")[:,:,0]
# get the resolution of the image (1920x1200 in this case); has to be the same as the resolution used in the file "create_correction_mask.py"
height, width = img_test.shape

# load vignetting_correction_mask.npy to work with this array
img_mask = np.load("vignetting_correction_mask.npy")

# devide the vignetted picture by the correction mask to get rid of the vignetting
img_result = img_test/img_mask

for i in range(height):
    for j in range(width):
        if (img_result[i,j] >= 255):
            img_result[i,j] = 255
        else:
            pass

plt.imshow(img_result, cmap="gray")
plt.colorbar()
plt.show()