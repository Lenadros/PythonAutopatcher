'''
Created on Jun 24, 2015

@author: ilya
'''
import numpy as np
import cv2

if __name__ == '__main__':
    img = cv2.imread('../../../testData/img_000000000__031.tif', cv2.IMREAD_ANYDEPTH)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    