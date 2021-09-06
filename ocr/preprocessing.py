import cv2 as cv
import logging
import sys

logger = logging.getLogger(__name__)

# function to preprocess the image
def gaussian_blur(img):
    try:
        # blur the image to reduce noise (low pass filter)
        img_gauss = cv.GaussianBlur(img, (11,11), 0)
        logger.info("preprocessing done")
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    return img_gauss

def median_blur(img):
    try:
        img_median = cv.medianBlur(img, 7)
        logger.info("preprocessing done")
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    return img_median

def bilateral_blur(img):
    try:
        img_bil = cv.bilateralFilter(img, 20, 75, 75)
        logger.info("preprocessing done")
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    return img_bil
        
def canny(img_blur):
    try:
        img_canny = cv.Canny(img_blur, 150, 200, apertureSize=3, L2gradient=True)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    return img_canny

if __name__ == '__main__':
    img = cv.imread("beispiel_cut.jpg")[...,0]
    img_gauss = gaussian_blur(img)
    img_median = median_blur(img)
    img_bil = bilateral_blur(img)
    
    img_canny = canny(img)
    img_gauss_canny = canny(img_gauss)
    img_median_canny = canny(img_median)
    img_bil_canny = canny(img_bil)

    #cv.imshow("without blur", img)
    cv.imshow("gaussian blur", img_gauss)
    #cv.imshow("median blur", img_median)
    #cv.imshow("bilateral blur", img_bil)
    
    #cv.imshow("canny without blur", img_canny)
    #cv.imshow("canny gaussian blur", img_gauss_canny)
    #cv.imshow("canny median blur", img_median_canny)
    #cv.imshow("canny bilateral blur", img_bil_canny)
    
    cv.waitKey(0)
    cv.destroyAllWindows()
