


import sys
import cv2
import numpy as np
from numpy import *

if len(sys.argv)<2:
    print "please specify video file name"

path = sys.argv[1]
print path
cameraCapture = cv2.VideoCapture(path)
FPS = cameraCapture.get(cv2.cv.CV_CAP_PROP_FPS)
cv2.namedWindow('window')

## save image quality, 1 ~ 100
## 1: lowest, 100: highest
save_img_quality = 50

## save image path
##   this path MUST EXIST before using!!! otherwise images cannot be saved
img_path = "./frame_with_target/"

## video writer
# fps = FPS
# size = (int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
# videoWriter = cv2.VideoWriter( 'try.avi', cv2.cv.CV_FOURCC('P','I','M','1'), fps, size)

## counting frames with target
max_target_digit = 6 # max 999999 frames
target_frame_cnt = 0



## video processing loop
while(cameraCapture.isOpened()):
  success, img = cameraCapture.read()

  if not(success):
    break

  ## convert to YCrCb, extract Y channel
  img_crcrcb = cv2.cvtColor(img, cv2.cv.CV_BGR2YCrCb)
  img_cr = img_crcrcb[:,:,1]

  ## Y-axis max, min, mean
  cr_max = img_cr.max()
  cr_min = img_cr.min()
  cr_avg = img_cr.mean()

  ## initialize some variables
  found_red = 0
  found_blue = 0
  target_text = ""

  ## red
  if (cr_max - cr_avg)>30:
      thresh = cr_max - (cr_max - cr_avg)*0.1
      img_cr_thresh_red = cv2.inRange(img_cr, thresh, 255)

      ## contour
      contour_red, hier = cv2.findContours(img_cr_thresh_red.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      if len(contour_red)>10:
        continue

      if len(contour_red)>0:
        ## reject contour if they are too large or too small
        for cnt in contour_red:
            area = cv2.contourArea(cnt)
            if area < img.size / 1000 and area > 50:
              found_red = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(10)
              cv2.circle(img,center,radius,(0,0,0),3)
              cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
              target_text += "red: " + str(cx) + ", " + str(cy) + "\n"
      
      if found_red == 1:
        print "   found red"

  ## blue		
  if (cr_avg - cr_min)>30:
      thresh = (cr_avg-cr_min)*0.45 + cr_min
      img_cr_thresh_blue = cv2.inRange(img_cr, thresh, 255)

      ## contour
      contour_blue, hier = cv2.findContours(img_cr_thresh_blue.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      if len(contour_blue)>10:
        continue

      if len(contour_blue)>0:
        ## reject contour if they are too large or too small
        for cnt in contour_blue:
            area = cv2.contourArea(cnt)
            if area < img.size / 1000 and area > 50:
              found_blue = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(10)
              cv2.circle(img,center,radius,(0,0,0),3)
              cv2.drawContours(img, [cnt], -1, (255,0,0), 2)
              target_text += "blue: " + str(cx) + ", " + str(cy) + "\n"
       
      if found_blue == 1:
        print "   found blue"

  ## if too many target, then reject
  if len(contour_blue) + len(contour_red) >15:
    continue

  ## save everything if targets are identified
  if found_red == 1 or found_blue == 1:
    ## save img
    index = str(target_frame_cnt).zfill(max_target_digit)    
    img_name = img_path + "target_frame_" + index + ".jpg"
    img_param = [cv2.cv.CV_IMWRITE_JPEG_QUALITY, save_img_quality]
    cv2.imwrite(img_name, img, img_param)

    ## save target information in a file
    f_name = img_path + "target_frame_" + index + ".txt"
    f = open(f_name, "w")
    f.write(target_text)
    f.close()

  cv2.imshow('window',img)
  #videoWriter.write(img)
  #cv2.waitKey(20)
  #cv2.waitKey((int)(1000/FPS))


cv2.waitKey(0)
cv2.destroyAllWindows()


