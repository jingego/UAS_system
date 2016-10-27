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
from numpy import *
from gps import *
from time import *
from datetime import datetime

cameraCapture = cv2.VideoCapture(0)

cameraCapture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cameraCapture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)


#cv2.namedWindow('window')
success, img = cameraCapture.read()

dropbox_sync_script = "/home/odroid/detect/dropbox/py-script/dropbox_sync.py"
img_save_path  =  "/home/odroid/detect/opencv-version/"
video_name = img_save_path + "try.avi"

## video writer
## CV_FOURCC compression codes can be found at http://www.fourcc.org/codecs.php
#fps = 24
#size = (int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(cameraCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
#videoWriter = cv2.VideoWriter(video_name, cv2.cv.CV_FOURCC('P','I','M','1'), fps, size)

## save image quality, 1 ~ 100
## 1: lowest, 100: highest
save_img_quality = 40

## save image path
##   this path MUST EXIST before using!!! otherwise images cannot be saved
img_path = img_save_path + "frame_with_target/"

## counting frames with target
max_target_digit = 8 # max  frames
target_frame_cnt = 0
frame_cnt = 0


## list of files to be synced to dropbox
dropbox_sync_arg_list_init = ["python", dropbox_sync_script]
dropbox_sync_arg_list = dropbox_sync_arg_list_init
sync_t_old = datetime.now()
sync_t_now = 0


###################################
## GPS initialization script
###################################
gpsd = None #seting the global variable
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 

gpsp = GpsPoller() # create the thread

try:
 ## start GPS monitor thread
 gpsp.start()

 ## video processing loop
 while success and cv2.waitKey(1) != 27:

  ## initialize some variables
  found_red = 0
  found_blue = 0
  target_text = ""
  contour_red = []
  contour_blue = []
  img_lon = 0
  img_lat = 0
  img_alt = 0

  ## read image
  success, img = cameraCapture.read()

  if not(success):
    time.sleep(1)
    continue

  sync_t_now = datetime.now()
  frame_cnt = frame_cnt + 1

  ## convert to YCrCb, extract Y channel
  img_crcrcb = cv2.cvtColor(img, cv2.cv.CV_BGR2YCrCb)
  img_cr = img_crcrcb[:,:,1]

  ## Y-axis max, min, mean
  cr_max = img_cr.max()
  cr_min = img_cr.min()
  cr_avg = img_cr.mean()

  ## get GPS location
#  if len(gpsd.satellites)<1:
#    print "GPS not fixed. number of sat: ", len(gpsd.satellites)
  
  img_lon = gpsd.fix.longitude
  img_lat = gpsd.fix.latitude
  img_alt = gpsd.fix.altitude
#  print img_lon, img_lat, img_alt

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
            if area < img.size / 1000 and area > 50:
              found_red = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(60)
              cv2.circle(img,center,radius,(255,255,255),2)
              #cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
      
      if found_red == 1:
        print "   found red"

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
            if area < img.size / 1000 and area > 50:
              found_blue = 1
              M = cv2.moments(cnt)
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              center = (cx, cy)
              radius = int(60)
              cv2.circle(img,center,radius,(255,255,255),2)
              #cv2.drawContours(img, [cnt], -1, (255,0,0), 2)
       
      if found_blue == 1:
        print "   found blue"

  ## write a video
  #videoWriter.write(img)
  #cv2.imshow('window',img)

  ## if too many target, then reject
  if len(contour_blue) + len(contour_red) >15:
    continue

  ## save everything if targets are identified
  if found_red == 1 or found_blue == 1:
    ## save img
    index = str(frame_cnt).zfill(max_target_digit)    
    img_name = img_path + "target_frame_" + index + ".jpg"
    img_param = [cv2.cv.CV_IMWRITE_JPEG_QUALITY, save_img_quality]
    cv2.imwrite(img_name, img, img_param)

#    img_name = img_path + "target_frame_" + index + "_red.jpg"
#    img_param = [cv2.cv.CV_IMWRITE_JPEG_QUALITY, save_img_quality]
#    cv2.imwrite(img_name, img_cr_thresh_red, img_param)

#    img_name = img_path + "target_frame_" + index + "_blue.jpg"
#    img_param = [cv2.cv.CV_IMWRITE_JPEG_QUALITY, save_img_quality]
#    cv2.imwrite(img_name, img_cr_thresh_blue, img_param)

    target_frame_cnt = target_frame_cnt + 1

    ## save target information in a file
    f_name = img_path + "target_frame_"+index+"GPS.txt"
    f = open(f_name, "w")
    target_text =  "target_frame_" + index + ":"
    target_text += " lon=" + str(img_lon) + " lat=" + str(img_lat) + " alt=" + str(img_alt) + "\n"
    f.write(target_text)
    f.close()

    dropbox_sync_arg_list.append("target_frame_"+index+"GPS.txt")
    dropbox_sync_arg_list.append("target_frame_" + index + ".jpg")

    

  ## upload to dropbox every 50 sec
  delta_t = sync_t_now - sync_t_old
  if delta_t.total_seconds()>50:
    print dropbox_sync_arg_list
    subprocess.Popen(dropbox_sync_arg_list)
    dropbox_sync_arg_list = ["python", dropbox_sync_script]
    sync_t_old = sync_t_now

  #cv2.waitKey(5)
  
  #cv2.waitKey(20)
  #cv2.waitKey((int)(1000/FPS))
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing

print "done"
#cv2.destroyWindow('window')


