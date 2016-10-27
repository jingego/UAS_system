


import sys
import cv2
import numpy as np
from numpy import *

if len(sys.argv)<2:
    print "please specify img file name"


path = sys.argv[1]
print path
img = cv2.imread(path)

cv2.namedWindow('window', cv2.WINDOW_NORMAL)


## convert to YCrCb, extract Y channel
img_crcrcb = cv2.cvtColor(img, cv2.cv.CV_BGR2YCrCb)
img_cr = img_crcrcb[:,:,1]

## Y-axis max, min, mean
cr_max = img_cr.max()
cr_min = img_cr.min()
cr_avg = img_cr.mean()

## red
if (cr_max - cr_avg)>30:
      thresh = cr_max - (cr_max - cr_avg)*0.1
      img_cr_thresh_red = cv2.inRange(img_cr, thresh, 255)

      ## contour
      contour, hier = cv2.findContours(img_cr_thresh_red.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      found_red = 0
      if len(contour)>0:
        ## reject contour if they are too large or too small
        for cnt in contour:
            area = cv2.contourArea(cnt)
            if area < img.size / 20 and area > 50:
              found_red = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(10)
              cv2.circle(img,center,radius,(0,0,0),3)
              cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
      
      if found_red == 1:
        print "    found red"

## blue		
if (cr_avg - cr_min)>30:
      thresh = (cr_avg-cr_min)*0.45 + cr_min
      img_cr_thresh_blue = cv2.inRange(img_cr, thresh, 255)

      ## contour
      contour, hier = cv2.findContours(img_cr_thresh_blue.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      found_blue = 0
      if len(contour)>0:
        cnt_max_area = cv2.contourArea(contour[0])
        cnt_max = contour[0]
        ## reject contour if they are too large or too small
        for cnt in contour:
            area = cv2.contourArea(cnt)
            print "area: ", area
            if area < img.size / 20 and area > 50:
              found_blue = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(10)
              cv2.circle(img,center,radius,(0,0,0),3)
              cv2.drawContours(img, [cnt], -1, (255,0,0), 2)

      if found_blue == 1:
        print "   found blue"


cv2.imshow('window',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


