import cv2 as cv
import time

# function to load an image (will be replaced by the frame from the neoAPI later)
def load_image(name_image):
    startTime = time.time()
    # loading grayscaled image
    img_raw = cv.imread(name_image)[...,0]
    # select ROI and only keep this part
    img_cut = img_raw[300:1075, 150:1790]
    print("load_image: " + str(time.time()-startTime))
    return img_cut

#img = load_image("images/Dataset_Stripe/1,5ms_k2_7.jpg")
#cv.imwrite("test_roi.jpg", img)