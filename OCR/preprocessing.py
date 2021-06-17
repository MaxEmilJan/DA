import cv2 as cv

# function to preprocess the image
def preprocessing(img_roi):
    # blur the image to reduce noise (low pass filter)
    img_blur = cv.GaussianBlur(img_roi, (11,11), 0)
    return img_blur