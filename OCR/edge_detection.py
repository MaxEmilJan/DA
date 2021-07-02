import cv2 as cv
import numpy as np
import time

# function to detect closed edges in the image by applying the canny edge detection methode
def canny_edge_detection(img_preprocessed, filter_close, filter_dil):
    startTime = time.time()
    # basic canny edge detection
    img_preprocessed = np.uint8(img_preprocessed)
    img_canny = cv.Canny(img_preprocessed, 150, 200, apertureSize=3, L2gradient=True)
    # mellow closing the image to close edges with small gaps
    img_close_1 = cv.morphologyEx(img_canny, cv.MORPH_CLOSE, filter_close)
    img_cnt_delete = img_close_1.copy()    
    # find contours and their hierarchy
    contours, hierarchy = cv.findContours(img_close_1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # check if contours is not None
    if len(contours) != 0:
        cnt_detected = True
        # check if a contour has more then 3 child contours
        for i in range(len(hierarchy[0])):
            count_children = 0
            index_child = 0
            if hierarchy[0][i][2] != -1:
                count_children += 1
                index_child = hierarchy[0][i][2]
                while hierarchy[0][index_child][0] != -1:
                    count_children += 1
                    index_child = hierarchy[0][index_child][0]
                else:
                    pass
            if count_children > 5:
                cnt_delete = contours[i]
                for j in cnt_delete:
                    img_cnt_delete[j[0][1], j[0][0]] = 0
            else:
                pass
        # only keep closed edges
        # make a copy of the previous image
        img_fill = img_cnt_delete.copy()
        # get its shape
        h_img, w_img = img_fill.shape[:2]
        # create a mask which is slightly larger
        mask_fill = np.zeros((h_img + 2, w_img + 2), dtype=np.uint8)
        # flood the image with only white (255) pixels from top left pixel
        cv.floodFill(img_fill, mask_fill, (0,0), 255)
        # invert the image to obtain the original image but with closed contours only
        img_fill_inv = cv.bitwise_not(img_fill)
        
        # -----OPTIONAL----- 
        # open image to remove very small parts
        #filter_open = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
        #img_open = cv.morphologyEx(img_fill_inv, cv.MORPH_OPEN, filter_open)
        # -----OPTIONAL-----
        
        # dilation (thicken the edges)
        img_dil = cv.dilate(img_fill_inv, filter_dil, iterations=1)
        # close image to fill holes inside the edges
        #img_close_2 = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, filter_close)
        # plot the result
        #cv.imshow("Canny", img_canny)
        #cv.imshow("closed", img_close_1)
        #cv.imshow("filtered", img_cnt_delete)
        #cv.imshow("flooded", img_fill_inv)
        #cv.imshow("boxes", img_close_2)
        #cv.waitKey(0)
        #cv.destroyAllWindows()
    else:
        cnt_detected = False
        img_dil = None
    print("edge_detection: " + str(time.time()-startTime))
    return img_dil, cnt_detected

#img_blur = cv.imread("vignetting_correction/test_blur.jpg")[...,0]
#img_edge, contours, hierarchy, roi_candidate = canny_edge_detection(img_blur)
#cv.imwrite("vignetting_correction/test_edge.jpg", img_edge)