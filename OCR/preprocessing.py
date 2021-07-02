import cv2 as cv
import time

# function to preprocess the image
def preprocessing(img):
    startTime = time.time()
    # blur the image to reduce noise (low pass filter)
    img_blur = cv.GaussianBlur(img, (11,11), 0)
    print("preprocessing: " + str(time.time()-startTime))
    return img_blur

#img_corrected = cv.imread("vignetting_correction/test_corrected.jpg")[...,0]
#img_blur = preprocessing(img_corrected)
#cv.imwrite("vignetting_correction/test_blur.jpg", img_blur)