
import sys
import cv2
import numpy as np
import datetime
from numpy import *
starttime =datetime.datetime.now()
if len(sys.argv)<2:
    print "please specify video file name"

path = sys.argv[1]
print path
cameraCapture = cv2.VideoCapture(path)
FPS = cameraCapture.get(cv2.cv.CV_CAP_PROP_FPS)
num_frame = cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

## save image quality, 1 ~ 100
## 1: lowest, 100: highest
save_img_quality = 50

## save image path
##   this path MUST EXIST before using!!! otherwise images cannot be saved
img_path = "./frame_with_target/"

## counting frames with target
max_target_digit = 6 # max 999999 frames
target_frame_cnt = 0
frame_no=0
n=5
timeToStart =30
frameToStart = timeToStart*25
frameToStop  = num_frame

cameraCapture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,frameToStart)

## video processing loop
while(cameraCapture.isOpened()):
  success, img = cameraCapture.read()

  if (n!=5):
  	n += 1
  	continue
  
  n=1

  if not(success):
    break

  frame_no=cameraCapture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)+1  
  #print frame_no
  
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
      if len(contour_red)>0 and len(contour_red)<10:
        ## reject contour if they are too large or too small
        for cnt in contour_red:
            area = cv2.contourArea(cnt)
            if area < img.size / 5000 and area > 50:
              found_red = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(50)
              cv2.circle(img,center,radius,(0,0,255),3)
              target_text += "red: " + str(cx) + ", " + str(cy) + "\n"
      
  ## blue		
  if (cr_avg - cr_min)>30:
      thresh = (cr_avg-cr_min)*0.45 + cr_min
      img_cr_thresh_blue = cv2.inRange(img_cr, thresh, 255)

      ## contour
      contour_blue, hier = cv2.findContours(img_cr_thresh_blue.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      if len(contour_blue)>0 and len(contour_blue)<10:
        ## reject contour if they are too large or too small
        for cnt in contour_blue:
            area = cv2.contourArea(cnt)
            if area < img.size / 5000 and area > 50:
              found_blue = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(50)
              cv2.circle(img,center,radius,(255,0,0),3)
              target_text += "blue: " + str(cx) + ", " + str(cy) + "\n"
       
  ## save everything if targets are identified
  if found_red == 1 or found_blue == 1:
    ## save img
    index = str(int(frame_no))#.zfill(max_target_digit)    
    img_name = img_path + "target_frame_" + index + ".jpg"
    img_param = [cv2.cv.CV_IMWRITE_JPEG_QUALITY, save_img_quality]
    cv2.imwrite(img_name, img, img_param)
    target_frame_cnt = target_frame_cnt + 1
  
  if frame_no > frameToStop:
  	break

print "done!"
endtime = datetime.datetime.now()
print (endtime - starttime)
