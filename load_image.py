import cv2 as cv

# function to load an image (will be replaced by the frame from the neoAPI later)
def load_image(name_image):
    # loading grayscaled image
    img_raw = cv.imread(name_image)[...,0]
    # select ROI and only keep this part
    img_cut = img_raw[300:1075, 150:1790]
    return img_cut

#img = load_image("OCR/1,5ms_k2_7.jpg")
#cv.imwrite("OCR/test_roi.jpg", img)