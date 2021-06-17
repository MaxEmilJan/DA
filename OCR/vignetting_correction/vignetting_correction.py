# import cv2 as cv
import numpy as np
# from matplotlib import pyplot as plt

def vignetting_correction(img_vignett, correction_mask):
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
    # return the corrected image without vignetting
    return np.uint8(img_corrected)

# # input of image which the vignetting should get removed from
# number_img = "5"

# # loading image with object to test the vignetting correction
# img_test = cv.imread("test_" + number_img + ".jpg")[:,:,0]
# # get the resolution of the image (1920x1200 in this case); has to be the same as the resolution used in the file "create_correction_mask.py"
# height, width = img_test.shape

# # load vignetting_correction_mask.npy to work with this array
# img_mask = np.load("vignetting_correction_mask.npy")

# # devide the vignetted picture by the correction mask to get rid of the vignetting
# img_result = img_test/img_mask

# for i in range(height):
#     for j in range(width):
#         if (img_result[i,j] >= 255):
#             img_result[i,j] = 255
#         else:
#             pass

# cv.imwrite("test_" + number_img + "_corrected.jpg", img_result)

# plt.imshow(img_result, cmap="gray")
# plt.show()