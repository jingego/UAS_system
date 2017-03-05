##
## detecting red and blue objects from video stream, report GPS coordinates
## developed for TAIWAN INNOVATIVE UAV DESIGN COMPETITION 2016
##
## platform: Odroid
## -------------------------------------------------------------------------------
##      Jiang Yifan
##      jiang.uhrmacher@gmail.com
##

import cv2, os, time, subprocess, threading
import numpy as np
from time import *
from datetime import datetime

#*****************************Parameter Setting***************************#
#Critial Setting
##Size Setting, in Pixels
CritialSizeMax=20
CritialSizeMin=2
CritialNum=10

ThreshRed=0.35
ThreshBlue=0.45
#Camera Setting
CamIndex=1

#Processing Parameters
FrameJumpNumber=15
SkipFlag=1
VideoRecordFlag=1
#*********************************Setting End*****************************#

#******************************Initialise Camera**************************#
cameraCapture = cv2.VideoCapture(CamIndex)
cameraCapture.set(3,1920)
cameraCapture.set(4,1080)

success, img = cameraCapture.read()

#video writer
## CV_FOURCC compression codes can be found at http://www.fourcc.org/codecs.php
if (VideoRecordFlag):
	video_name = "try.avi"
	fps = 24
	size = (1920,1080)
	videoWriter = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('P','I','M','1'), fps, size)

## save image quality, 1 ~ 100
## 1: lowest, 100: highest
save_img_quality = 100

## save image path
##   this path MUST EXIST before using!!! otherwise images cannot be saved
img_path = "./frame_with_target/"


## counting frames with target
max_target_digit = 8 # max  frames
target_frame_cnt = 0
frame_cnt = 0
SkipCount=1
SizeMax=CritialSizeMax*CritialSizeMax*3
SizeMin=CritialSizeMin*CritialSizeMin*3
try:
 ## video processing loop
 while success and cv2.waitKey(1) != 27:
  
  ## initialize some variables
  found_red = 0
  found_blue = 0
  target_text = ""
  contour_red = []
  contour_blue = []
  
  ## read image
  success, img1 = cameraCapture.read()

  ## Skip frames to reduce the identification rate. Use 'SkipFlag' to start/stop frames jumping 
  ## Numbers of jumped frames was set bt 'FrameJumpNumber'.

  if (SkipFlag) and (SkipCount<FrameJumpNumber):
    SkipCount=SkipCount+1
    continue

  SkipCount=1;

  img=img1[160:950,325:1560]

  if (VideoRecordFlag):
    videoWriter.write(img1)

  if not(success):
    time.sleep(1)
    continue

  sync_t_now = datetime.now()
  frame_cnt = frame_cnt + 1

  ## convert to YCrCb, extract Y channel
  img_crcrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
  img_cr = img_crcrcb[:,:,1]

  ## Y-axis max, min, mean
  cr_max = img_cr.max()
  cr_min = img_cr.min()
  cr_avg = img_cr.mean()

  ## red
  if (cr_max - cr_avg)>30:
      thresh = cr_max - (cr_max - cr_avg)*ThreshRed
      img_cr_thresh_red = cv2.inRange(img_cr, thresh, 255)
      #
      ## contour
      im2,contour_red, hier = cv2.findContours(img_cr_thresh_red.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      if len(contour_red)>0 and len(contour_red) < CritialNum:
        ## reject contour if they are too large or too small
        for cnt in contour_red:
            area = cv2.contourArea(cnt)
            if area < SizeMax and area > SizeMin:
              found_red = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(25)
              cv2.circle(img,center,radius,(0,0,255),2)

  ## blue		
  if (cr_avg - cr_min)>30:
      thresh = (cr_avg-cr_min)*ThreshBlue + cr_min
      img_cr_thresh_blue = cv2.inRange(img_cr, thresh, 255)
      ## contour
      im3, contour_blue, hier = cv2.findContours(img_cr_thresh_blue.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      if len(contour_blue)>0 and len(contour_blue) < CritialNum:
        ## reject contour if they are too large or too small
        for cnt in contour_blue:
            area = cv2.contourArea(cnt)
            if area < SizeMax and area > SizeMin:
              found_blue = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(25)
              cv2.circle(img,center,radius,(255,0,0),2)
              
  
# open and close live video
  cv2.imshow('frame',img)     
    
  ## if too many target, then reject
  if len(contour_blue) + len(contour_red) >15:
    continue

  ## save everything if targets are identified
  if found_red == 1 or found_blue == 1:
    ## save img
    index = str(frame_cnt).zfill(max_target_digit)    
    img_name = img_path + "target_frame_" + index + ".jpg"
    #img_param = [cv2.CV_IMWRITE_JPEG_QUALITY, save_img_quality]
    cv2.imwrite(img_name, img1)

    target_frame_cnt = target_frame_cnt + 1

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."

print "done"
cameraCapture.release()
cv2.destroyAllWindows()


