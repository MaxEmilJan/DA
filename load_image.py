import cv2 as cv

# function to load an image (will be replaced by the frame from the neoAPI later)
def load_image(name_image):
    # loading grayscaled image
    img_raw = cv.imread(name_image)[...,0]
    # select ROI and only keep this part
    img_cut = img_raw[0:1200, 150:1790]
    height, width = img_cut.shape
    return img_cut, height, width

#img, height, width = load_image("images/Streifen_2,8/3ms_2,8_1.jpg")
#cv.imwrite("test_roi.jpg", img)